"""
LangGraph simulation workflow - FIXED VERSION
"""
from typing import TypedDict, List, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import asyncio

from llm.service import LLMService
from vector_store.chroma_client import ChromaClient
from beads.engine import BeadEngine
from config import settings


# === State Definition ===

class SimulationState(TypedDict):
    """State for the simulation workflow."""
    heroine_soul: Dict[str, Any]
    current_scene: Optional[Dict[str, Any]]
    active_npcs: List[Dict[str, Any]]
    player_action: str
    conversation_history: Annotated[List[Dict[str, Any]], lambda a, b: a + b]
    retrieved_memories: List[Dict[str, Any]]
    npc_responses: List[Dict[str, Any]]
    updated_relationships: Dict[str, float]
    bead_data: Dict[str, Any]
    new_bead_id: Optional[str]


# === Node Functions (using injected services) ===

async def retrieve_context(state: SimulationState, chroma: ChromaClient) -> SimulationState:
    """
    Retrieve relevant memories from ChromaDB.
    Uses injected chroma client (singleton).
    """
    query = state['player_action']
    if state['conversation_history']:
        recent = state['conversation_history'][-3:]
        query += " " + " ".join(str(turn) for turn in recent)

    results = chroma.search_conversations(query, k=5)

    # Placeholder: get NPC backstories (would load from files)
    generic_memories = [
        {"content": f"{npc['name']} character trait", "metadata": {"npc_id": npc['id']}}
        for npc in state['active_npcs']
    ]

    return {
        **state,
        "retrieved_memories": results + generic_memories
    }


async def process_player_action(state: SimulationState) -> SimulationState:
    """Parse player action (simplified pass-through)."""
    return {
        **state,
        "parsed_action": {
            "text": state['player_action'],
            "intent": "dialogue",
            "target": None,
            "emotion_hint": "neutral"
        }
    }


async def generate_npc_responses(state: SimulationState, llm: LLMService) -> SimulationState:
    """
    Generate NPC responses in parallel.
    Uses injected LLM service singleton.
    """
    tasks = []
    for npc in state['active_npcs']:
        context_str = "\n".join(
            f"{turn.get('speaker', '?')}: {turn.get('text', '')}"
            for turn in state['conversation_history'][-5:]
        )
        task = llm.simulate_npc_response(
            npc=npc,
            context=context_str,
            player_action=state['player_action']
        )
        tasks.append((npc['id'], task))

    results = await asyncio.gather(*[t[1] for t in tasks], return_exceptions=True)

    responses = []
    for (npc_id, _), result in zip(tasks, results):
        if isinstance(result, Exception):
            responses.append({
                "npc_id": npc_id,
                "dialogue": f"(Error: {result})",
                "emotion": "neutral",
                "relationship_delta": 0.0
            })
        else:
            responses.append({
                "npc_id": npc_id,
                "dialogue": result.get("dialogue", "..."),
                "emotion": result.get("emotion", "neutral"),
                "relationship_delta": result.get("relationship_delta", 0.0)
            })

    return {
        **state,
        "npc_responses": responses
    }


async def update_relationship_state(state: SimulationState) -> SimulationState:
    """Compute relationship score updates."""
    updates: Dict[str, float] = {}
    for resp in state['npc_responses']:
        current = updates.get(resp['npc_id'], 0.0)
        updates[resp['npc_id']] = current + resp.get('relationship_delta', 0.0)

    # Clamp to [-1, 1]
    for npc_id in updates:
        updates[npc_id] = max(-1.0, min(1.0, updates[npc_id]))

    return {
        **state,
        "updated_relationships": updates
    }


async def commit_bead(state: SimulationState, bead_engine: BeadEngine, llm: LLMService) -> SimulationState:
    """
    Create a new Bead to record this turn.
    Uses injected bead_engine singleton.
    """
    # Get current HEAD as parent
    head = await bead_engine.get_head("main")

    bead_content = {
        "player_action": state['player_action'],
        "npc_responses": state['npc_responses'],
        "scene_id": state['current_scene'].get('id') if state['current_scene'] else None,
        "relationships_delta": state['updated_relationships']
    }

    # Generate bead ID using engine (simplified)
    import json, hashlib
    hash_input = json.dumps(bead_content, sort_keys=True) + (head.id if head else "")
    bead_id = hashlib.sha1(hash_input.encode()).hexdigest()

    bead_data = {
        "id": bead_id,
        "parent_id": head.id if head else None,
        "branch_name": "main",
        "action": "turn",
        "emotion_tag": state['npc_responses'][0]['emotion'] if state['npc_responses'] else "neutral",
        "content": bead_content,
        "timestamp": "2025-03-15T00:00:00"  # TODO: use actual time
    }

    # Actually persist the bead
    await bead_engine.create_bead(
        action=bead_data["action"],
        content=bead_data["content"],
        parent_id=bead_data["parent_id"],
        branch_name=bead_data["branch_name"],
        emotion_tag=bead_data["emotion_tag"]
    )

    return {
        **state,
        "bead_data": bead_data,
        "new_bead_id": bead_id
    }


# === Graph Construction ===

def build_graph(bead_engine: BeadEngine, llm: LLMService, chroma: ChromaClient):
    """
    Build and compile the simulation graph with injected dependencies.
    """
    workflow = StateGraph(SimulationState)

    # Add nodes with partial application of dependencies
    workflow.add_node("retrieve_context", lambda s: retrieve_context(s, chroma))
    workflow.add_node("process_action", process_player_action)
    workflow.add_node("generate_responses", lambda s: generate_npc_responses(s, llm))
    workflow.add_node("update_relationships", update_relationship_state)
    workflow.add_node("commit_bead", lambda s: commit_bead(s, bead_engine, llm))

    # Set entry point and edges
    workflow.set_entry_point("retrieve_context")
    workflow.add_edge("retrieve_context", "process_action")
    workflow.add_edge("process_action", "generate_responses")
    workflow.add_edge("generate_responses", "update_relationships")
    workflow.add_edge("update_relationships", "commit_bead")
    workflow.add_edge("commit_bead", END)

    # Compile with memory checkpointing
    memory = MemorySaver()
    return workflow.compile(checkpointer=memory)


class SimulationGraph:
    """
    Wrapper for the compiled LangGraph simulation workflow.
    Now uses persistent service instances.
    """
    def __init__(self, bead_engine: BeadEngine, llm: LLMService, chroma: ChromaClient):
        """
        Initialize with injected service singletons.
        """
        self.bead_engine = bead_engine
        self.llm = llm
        self.chroma = chroma
        self.graph = build_graph(bead_engine, llm, chroma)

    async def arun(self, input_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the simulation graph asynchronously.
        """
        # Provide default state values
        default_state: SimulationState = {
            "heroine_soul": {},
            "current_scene": None,
            "active_npcs": [],
            "player_action": "",
            "conversation_history": [],
            "retrieved_memories": [],
            "npc_responses": [],
            "updated_relationships": {},
            "bead_data": {},
            "new_bead_id": None
        }

        full_state = {**default_state, **input_state}

        # Invoke graph
        result = await self.graph.ainvoke(full_state)
        return result

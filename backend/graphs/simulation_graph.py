"""LangGraph simulation workflow for turn-based conversations."""

from typing import Annotated, Any, Dict, List, Optional, Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


def merge_conversations(existing: List[Dict], new: List[Dict]) -> List[Dict]:
    """Merge conversation entries."""
    result = existing.copy()
    for item in new:
        if item not in result:
            result.append(item)
    return result


class SimulationState(TypedDict):
    """State for the simulation workflow."""

    heroine_soul: Dict[str, Any]
    current_scene: Optional[Dict[str, Any]]
    active_npcs: List[Dict[str, Any]]
    player_action: str
    conversation_history: Annotated[List[Dict], merge_conversations]
    retrieved_memories: List[Dict[str, Any]]
    npc_responses: List[Dict[str, Any]]
    updated_relationships: Dict[str, float]
    bead_data: Dict[str, Any]
    new_bead_id: Optional[str]


async def retrieve_context(state: SimulationState) -> Dict[str, Any]:
    """Retrieve semantic memories from vector store."""
    return {"retrieved_memories": []}


async def process_player_action(state: SimulationState) -> Dict[str, Any]:
    """Process player action (currently passthrough)."""
    return {}


async def generate_npc_responses(state: SimulationState) -> Dict[str, Any]:
    """Generate NPC responses using LLM service."""
    responses = []
    for npc in state.get("active_npcs", []):
        responses.append(
            {
                "npc_id": npc.get("id", ""),
                "npc_name": npc.get("name", "Unknown"),
                "message": f"Response from {npc.get('name', 'Character')}",
                "emotion": "neutral",
            }
        )
    return {"npc_responses": responses}


async def update_relationships(state: SimulationState) -> Dict[str, Any]:
    """Update relationship scores based on responses."""
    relationships = {}
    for npc in state.get("active_npcs", []):
        relationships[npc.get("id", "")] = 0.1
    return {"updated_relationships": relationships}


async def commit_bead(state: SimulationState) -> Dict[str, Any]:
    """Commit new bead to Beads DAG."""
    import uuid

    bead_id = f"bead_{uuid.uuid4().hex[:16]}"

    bead_data = {
        "action": "simulation_turn",
        "player_action": state.get("player_action", ""),
        "npc_responses": state.get("npc_responses", []),
        "relationships": state.get("updated_relationships", {}),
        "scene": state.get("current_scene"),
    }

    return {
        "new_bead_id": bead_id,
        "bead_data": bead_data,
        "conversation_history": [
            {
                "player_action": state.get("player_action", ""),
                "npc_responses": state.get("npc_responses", []),
            }
        ],
    }


def should_commit_bead(state: SimulationState) -> Literal["commit_bead", "__end__"]:
    """Determine if we should commit a bead."""
    if state.get("player_action"):
        return "commit_bead"
    return "__end__"


def build_simulation_workflow() -> Any:
    """Build the simulation workflow graph."""
    builder = StateGraph(SimulationState)

    # Add nodes
    builder.add_node("retrieve_context", retrieve_context)
    builder.add_node("process_action", process_player_action)
    builder.add_node("generate_responses", generate_npc_responses)
    builder.add_node("update_relationships", update_relationships)
    builder.add_node("commit_bead", commit_bead)

    # Wire edges - sequential flow
    builder.add_edge(START, "retrieve_context")
    builder.add_edge("retrieve_context", "process_action")
    builder.add_edge("process_action", "generate_responses")
    builder.add_edge("generate_responses", "update_relationships")

    # Conditional edge to commit or end
    builder.add_conditional_edges(
        "update_relationships",
        should_commit_bead,
        {"commit_bead": "commit_bead", "__end__": END},
    )

    builder.add_edge("commit_bead", END)

    # Compile with checkpointer
    checkpointer = MemorySaver()
    return builder.compile(checkpointer=checkpointer)


# Create the workflow instance
simulation_workflow = build_simulation_workflow()


async def run_simulation_turn(
    state: SimulationState,
    thread_id: str = "default",
) -> SimulationState:
    """Run a single simulation turn."""
    config = {"configurable": {"thread_id": thread_id}}
    return await simulation_workflow.ainvoke(state, config)

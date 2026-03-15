"""
Simulation API endpoints - FIXED VERSION
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from database import get_session, Bead, Character, Relationship, Scene, ActionType, EmotionTag
from api.schemas import (
    SimulationTurnRequest, SimulationTurnResponse,
    SimulationStateResponse, NPCResponse
)
from graphs.simulation_graph import SimulationGraph
from config import get_bead_engine, get_llm_service, get_chroma_client
import json

router = APIRouter()

# Global graph instance (initialized on startup)
simulation_graph: Optional[SimulationGraph] = None


@router.on_event("startup")
async def init_graphs():
    """Initialize global graph instance with singleton services."""
    global simulation_graph

    try:
        # Get singleton services (lazy initialized)
        bead_engine = get_bead_engine()
        llm_service = get_llm_service()
        chroma_client = get_chroma_client()

        # Build graph with injected dependencies
        simulation_graph = SimulationGraph(
            bead_engine=bead_engine,
            llm=llm_service,
            chroma=chroma_client
        )

        print("✅ Simulation graph initialized")
        print(f"   - LLM: {llm_service.__class__.__name__}")
        print(f"   - ChromaDB: {chroma_client.client.list_collections()}")
    except Exception as e:
        print(f"❌ Failed to initialize simulation graph: {e}")
        import traceback
        traceback.print_exc()
        raise


@router.get("/state", response_model=SimulationStateResponse)
async def get_simulation_state(
    session: AsyncSession = Depends(get_session)
):
    """Get current simulation state."""
    try:
        bead_engine = get_bead_engine()

        # Get current HEAD bead for main branch
        head_bead = await bead_engine.get_head("main")

        # Get heroine
        heroine_stmt = select(Character).where(Character.role == "heroine")
        heroine_result = await session.execute(heroine_stmt)
        heroine = heroine_result.scalar_one_or_none()

        if not heroine:
            return SimulationStateResponse(
                current_scene=None,
                active_npcs=[],
                relationships={},
                current_bead_id=None,
                available_branches=[]
            )

        # Get all NPCs
        npc_stmt = select(Character).where(Character.role.in_(["protector", "competitor", "shadow"]))
        npc_result = await session.execute(npc_stmt)
        npcs = npc_result.scalars().all()

        # Get relationships (heroine to NPCs)
        relationships = {}
        for npc in npcs:
            rel_stmt = select(Relationship).where(
                Relationship.character_id == heroine.id,
                Relationship.target_character_id == npc.id
            )
            rel_result = await session.execute(rel_stmt)
            rel = rel_result.scalar_one_or_none()
            if rel:
                relationships[npc.id] = rel.trust_score
            else:
                relationships[npc.id] = 0.0

        # Get current scene (from latest bead content)
        current_scene = None
        if head_bead and "scene_id" in head_bead.content:
            scene_stmt = select(Scene).where(Scene.id == head_bead.content["scene_id"])
            scene_result = await session.execute(scene_stmt)
            scene = scene_result.scalar_one_or_none()
            if scene:
                current_scene = SimulationStateResponse(
                    id=scene.id,
                    name=scene.name,
                    description=scene.description,
                    config=scene.config,
                    image_path=scene.image_path,
                    created_at=scene.created_at
                )

        npc_responses = [
            NPCResponse(
                id=npc.id,
                name=npc.name,
                role=npc.role,
                relationship_to_heroine=npc.role,
                soul=npc.cached_soul,
                identity=npc.cached_identity,
                voice=npc.cached_voice,
                created_at=npc.created_at
            )
            for npc in npcs
        ]

        return SimulationStateResponse(
            current_scene=current_scene,
            active_npcs=npc_responses,
            relationships=relationships,
            current_bead_id=head_bead.id if head_bead else None,
            available_branches=[]  # TODO: implement branch listing
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn", response_model=SimulationTurnResponse)
async def take_turn(
    request: SimulationTurnRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Process a player action and generate NPC responses.
    Core simulation loop using LangGraph.
    """
    try:
        global simulation_graph, bead_engine

        if not simulation_graph or not bead_engine:
            raise HTTPException(status_code=500, detail="Simulation graph not initialized")

        # Build current state
        state = await build_simulation_state(session)

        # Execute LangGraph
        result = await simulation_graph.arun({
            "heroine_soul": state["heroine_soul"],
            "current_scene": state["current_scene"],
            "active_npcs": state["active_npcs"],
            "player_action": request.player_action,
            "conversation_history": state["history"]
        })

        # Extract results
        responses = result.get("npc_responses", [])
        relationship_updates = result.get("updated_relationships", {})
        new_bead_id = result.get("new_bead_id")

        # Persist relationship updates to database
        for npc_id, delta in relationship_updates.items():
            await update_relationship(session, state["heroine_id"], npc_id, delta)

        await session.commit()

        return SimulationTurnResponse(
            bead_id=new_bead_id or "",
            responses=responses,
            updated_relationships=relationship_updates,
            next_beads=[]
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Simulation error: {str(e)}")


async def build_simulation_state(session: AsyncSession) -> dict:
    """
    Build initial simulation state from database.
    """
    bead_engine = get_bead_engine()

    # Get heroine
    heroine_stmt = select(Character).where(Character.role == "heroine")
    heroine_result = await session.execute(heroine_stmt)
    heroine = heroine_result.scalar_one_or_none()

    if not heroine:
        raise HTTPException(status_code=400, detail="No heroine created")

    # Get NPCs
    npc_stmt = select(Character).where(Character.role.in_(["protector", "competitor", "shadow"]))
    npc_result = await session.execute(npc_stmt)
    npcs = npc_result.scalars().all()

    active_npcs = []
    for npc in npcs:
        active_npcs.append({
            "id": npc.id,
            "name": npc.name,
            "role": npc.role,
            "soul": npc.cached_soul,
            "identity": npc.cached_identity,
            "voice": npc.cached_voice
        })

    # Get recent conversation history (from beads)
    try:
        bead_stmt = select(Bead).where(
            Bead.action == ActionType.TURN
        ).order_by(Bead.timestamp.desc()).limit(10)
        bead_result = await session.execute(bead_stmt)
        beads = bead_result.scalars().all()

        history = []
        for bead in reversed(beads):
            history.append({
                "role": "user" if "player_action" in bead.content else "assistant",
                "content": bead.content.get("player_action") or bead.content.get("npc_responses", [])
            })
    except Exception as e:
        print(f"Error loading bead history: {e}")
        history = []

    # Get current scene
    current_scene = None
    try:
        head_bead = await bead_engine.get_head("main")
        if head_bead and "scene_id" in head_bead.content:
            scene_stmt = select(Scene).where(Scene.id == head_bead.content["scene_id"])
            scene_result = await session.execute(scene_stmt)
            scene = scene_result.scalar_one_or_none()
            if scene:
                current_scene = {
                    "id": scene.id,
                    "name": scene.name,
                    "config": scene.config
                }
    except Exception as e:
        print(f"Error loading current scene: {e}")

    return {
        "heroine_id": heroine.id,
        "heroine_soul": heroine.cached_soul,
        "active_npcs": active_npcs,
        "current_scene": current_scene,
        "history": history
    }


async def update_relationship(
    session: AsyncSession,
    character_id: str,
    target_id: str,
    delta: float
):
    """
    Update trust score between character and target.
    Creates record if doesn't exist.
    """
    stmt = select(Relationship).where(
        Relationship.character_id == character_id,
        Relationship.target_character_id == target_id
    )
    result = await session.execute(stmt)
    rel = result.scalar_one_or_none()

    if not rel:
        rel = Relationship(
            character_id=character_id,
            target_character_id=target_id,
            relationship_type="dynamic",
            trust_score=0.0
        )
        session.add(rel)

    # Apply delta with clamping [-1, 1]
    rel.trust_score = max(-1.0, min(1.0, rel.trust_score + delta))

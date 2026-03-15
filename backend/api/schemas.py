"""
Shared Pydantic schemas for API request/response validation.
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


# === Common ===
class BaseResponse(BaseModel):
    """Base response model."""
    pass


class ErrorResponse(BaseModel):
    """Error response model."""
    detail: str
    status_code: int


# === Beads ===
class BeadCreate(BaseModel):
    """Request to create a new Bead."""
    parent_id: Optional[str] = None
    branch_name: str = "main"
    action: str  # ActionType value
    emotion_tag: Optional[str] = None
    content: Dict[str, Any] = Field(default_factory=dict)
    signature: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "parent_id": "abc123...",
                "branch_name": "main",
                "action": "turn",
                "emotion_tag": "joy",
                "content": {
                    "player_action": "Hello!",
                    "npc_responses": [{"npc_id": "npc_1", "dialogue": "Hi!", "emotion": "joy"}]
                }
            }
        }


class BeadResponse(BaseModel):
    """Full Bead response."""
    id: str
    parent_id: Optional[str]
    branch_name: str
    timestamp: datetime
    action: str
    emotion_tag: Optional[str]
    content: Dict[str, Any]
    signature: Optional[str]

    class Config:
        from_attributes = True


class BeadSummary(BaseModel):
    """Simplified Bead for timeline listing."""
    id: str
    parent_id: Optional[str]
    branch_name: str
    timestamp: datetime
    action: str
    emotion_tag: Optional[str]
    content_preview: Optional[str] = None  # Truncated content snippet

    @classmethod
    def from_bead(cls, bead):
        """Create summary from Bead model."""
        content_str = str(bead.content)
        preview = (content_str[:100] + "...") if len(content_str) > 100 else content_str
        return cls(
            id=bead.id,
            parent_id=bead.parent_id,
            branch_name=bead.branch_name,
            timestamp=bead.timestamp,
            action=bead.action.value if hasattr(bead.action, 'value') else bead.action,
            emotion_tag=bead.emotion_tag.value if bead.emotion_tag else None,
            content_preview=preview
        )


class BranchCreate(BaseModel):
    """Request to create a branch."""
    branch_name: str
    from_bead_id: str


class BranchResponse(BaseModel):
    """Response after branch creation."""
    branch_name: str
    head_bead_id: str
    message: str


class BeadDiffChange(BaseModel):
    """Single change in a diff."""
    field: str
    from_val: Any = Field(alias="from")
    to_val: Any = Field(alias="to")


class BeadDiffResponse(BaseModel):
    """Diff between two beads."""
    bead_id_earlier: str
    bead_id_later: str
    changes: List[BeadDiffChange]


# === Heroine ===
class SoulStructure(BaseModel):
    """Soul structure extracted from user description."""
    core_traumas: List[Dict[str, Any]] = Field(default_factory=list)
    defense_mechanisms: List[str] = Field(default_factory=list)
    ideal_type: Dict[str, List[str]] = Field(default_factory=dict)
    scene_preferences: List[str] = Field(default_factory=list)


class Identity(BaseModel):
    """Heroine identity data."""
    name: str
    age: int
    appearance: str
    personality: str
    backstory: str


class VoiceConfig(BaseModel):
    """Voice configuration."""
    speech_patterns: Dict[str, Any] = Field(default_factory=dict)
    vocabulary: Dict[str, Any] = Field(default_factory=dict)
    emotional_tone: Dict[str, str] = Field(default_factory=dict)


class HeroineCreateRequest(BaseModel):
    """Request to create a heroine."""
    description: str = Field(..., min_length=10, description="Free-form description")
    input_mode: str = Field("free_description", pattern="^(free_description|questionnaire|reality_import)$")


class HeroineResponse(BaseModel):
    """Heroine data response."""
    id: str
    soul: SoulStructure
    identity: Identity
    voice: VoiceConfig
    created_at: datetime

    class Config:
        from_attributes = True


# === NPCs ===
class NPCResponse(BaseModel):
    """NPC data response."""
    id: str
    name: str
    role: str  # "protector", "competitor", "shadow"
    relationship_to_heroine: str
    soul: Dict[str, Any]
    identity: Dict[str, Any]
    voice: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class NPCRefineRequest(BaseModel):
    """Request to refine an NPC."""
    feedback: str = Field(..., min_length=5, description="User feedback for refinement")


class NPCRefineResponse(BaseModel):
    """Response with suggested changes."""
    original: Dict[str, Any]
    suggested: Dict[str, Any]
    diff: List[Dict[str, Any]]


# === Scenes ===
class SceneConfig(BaseModel):
    """Scene configuration."""
    name: str
    description: str
    environment: Dict[str, Any] = Field(default_factory=dict)
    mood: str
    triggers: List[str] = Field(default_factory=list)
    npc_presences: List[Dict[str, Any]] = Field(default_factory=list)
    background_music: Optional[str] = None
    lighting: Optional[str] = None


class SceneResponse(BaseModel):
    """Scene response."""
    id: str
    name: str
    description: str
    config: Dict[str, Any]
    image_path: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# === Simulation ===
class SimulationTurnRequest(BaseModel):
    """Request to take a simulation turn."""
    player_action: str = Field(..., min_length=1)
    bead_id: Optional[str] = None  # Optional: if branching from specific point


class SimulationTurnResponse(BaseModel):
    """Response containing NPC reactions and new state."""
    bead_id: str
    responses: List[Dict[str, Any]]  # npc_id, dialogue, emotion
    updated_relationships: Dict[str, float]
    next_beads: List[str]  # Potential branch points


class SimulationStateResponse(BaseModel):
    """Current simulation state."""
    current_scene: Optional[SceneResponse]
    active_npcs: List[NPCResponse]
    relationships: Dict[str, float]  # npc_id -> trust_score
    current_bead_id: Optional[str]
    available_branches: List[str]

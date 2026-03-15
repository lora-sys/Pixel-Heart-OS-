"""
Database models for Pixel Heart OS using SQLAlchemy.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlalchemy import (
    Column, String, DateTime, Enum as SQLEnum, JSON, Text, ForeignKey, Index
)
from sqlalchemy.orm import declarative_base, relationship, Mapped, mapped_column
import enum

Base = declarative_base()


class ActionType(str, enum.Enum):
    """Types of actions that can create a Bead."""
    CREATE_HEROINE = "create_heroine"
    NPC_INTERACTION = "npc_interaction"
    SCENE_CHANGE = "scene_change"
    BRANCH = "branch"
    MERGE = "merge"
    NPC_REFINE = "npc_refine"
    TURN = "turn"


class EmotionTag(str, enum.Enum):
    """Emotion tags for color coding timeline nodes."""
    NEUTRAL = "neutral"
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"
    COMFORTING = "comforting"
    HOSTILE = "hostile"
    DEFIANT = "defiant"
    MYSTERIOUS = "mysterious"


class Bead(Base):
    """
    A Bead represents a single narrative event in the Beads DAG.
    Similar to a Git commit, it forms a directed acyclic graph.
    """
    __tablename__ = "beads"

    # Primary Key: SHA-1 hash of content + parent_id
    id: Mapped[str] = mapped_column(String(40), primary_key=True)

    # DAG structure
    parent_id: Mapped[Optional[str]] = mapped_column(
        String(40),
        ForeignKey("beads.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    parent: Mapped[Optional["Bead"]] = relationship(
        "Bead",
        remote_side=[id],
        backref="children"
    )

    # Branch management
    branch_name: Mapped[str] = mapped_column(
        String(100),
        default="main",
        index=True
    )

    # Metadata
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        index=True
    )
    action: Mapped[ActionType] = mapped_column(SQLEnum(ActionType), nullable=False)
    emotion_tag: Mapped[EmotionTag] = mapped_column(SQLEnum(EmotionTag), nullable=True)

    # Structured payload (JSON)
    content: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Integrity verification (LLM signature or HMAC)
    signature: Mapped[Optional[str]] = mapped_column(String(128))

    # Indexes for common queries
    __table_args__ = (
        Index('idx_beads_branch_timestamp', 'branch_name', 'timestamp'),
        Index('idx_beads_action', 'action'),
    )

    def __repr__(self) -> str:
        return f"<Bead(id={self.id[:8]}, action={self.action}, branch={self.branch_name})>"


class Character(Base):
    """
    Base character model - both Heroine and NPCs.
    """
    __tablename__ = "characters"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50))  # "heroine", "protector", "competitor", "shadow"

    # File references
    soul_file_path: Mapped[str] = mapped_column(String(500))
    identity_file_path: Mapped[str] = mapped_column(String(500))
    voice_file_path: Mapped[Optional[str]] = mapped_column(String(500))

    # Cached fields for quick access
    cached_soul: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    cached_identity: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    cached_voice: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    relationships: Mapped[List["Relationship"]] = relationship(
        "Relationship",
        back_populates="character",
        cascade="all, delete-orphan"
    )


class Relationship(Base):
    """
    Relationship between two characters (heroine ↔ NPC or NPC ↔ NPC).
    Stores dynamic emotional scores and history.
    """
    __tablename__ = "relationships"

    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("characters.id", ondelete="CASCADE"),
        index=True
    )
    target_character_id: Mapped[str] = mapped_column(
        String(100),
        ForeignKey("characters.id", ondelete="CASCADE"),
        index=True
    )

    character: Mapped["Character"] = relationship(
        foreign_keys=[character_id],
        back_populates="relationships"
    )
    target_character: Mapped["Character"] = relationship(
        foreign_keys=[target_character_id]
    )

    # Relationship type and scores
    relationship_type: Mapped[str] = mapped_column(
        String(50)
    )  # "protector", "competitor", "shadow", "friend", etc.

    trust_score: Mapped[float] = mapped_column(default=0.0)  # -1.0 to 1.0
    emotional_intimacy: Mapped[float] = mapped_column(default=0.0)  # 0.0 to 1.0
    conflict_level: Mapped[float] = mapped_column(default=0.0)  # 0.0 to 1.0

    # History tracking (list of bead IDs that affected this relationship)
    history: Mapped[List[str]] = mapped_column(JSON, default=list)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        # Unique constraint: each pair has one relationship record
        # (enforced at application level for bi-directional access)
        Index('idx_relationship_pair', 'character_id', 'target_character_id'),
    )


class Scene(Base):
    """
    Scene configuration - environment, mood, and NPC presence.
    """
    __tablename__ = "scenes"

    id: Mapped[str] = mapped_column(String(100), primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text)

    # Scene data (reconstructed from TOML/JSON)
    config: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)

    # Thumbnail/preview (optional)
    image_path: Mapped[Optional[str]] = mapped_column(String(500))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

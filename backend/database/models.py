from sqlalchemy import Column, String, DateTime, ForeignKey, Index, JSON, func
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Bead(Base):
    __tablename__ = "beads"

    id = Column(String(40), primary_key=True)  # SHA-1 hash
    parent_id = Column(String(40), ForeignKey("beads.id"), nullable=True)
    branch_name = Column(String(50), nullable=False, default="main")
    action = Column(String(50), nullable=False)
    emotion_tag = Column(String(50), nullable=True)
    content = Column(JSON, nullable=False)
    timestamp = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    # Indexes for common queries
    __table_args__ = (
        Index("ix_beads_branch_name", "branch_name"),
        Index("ix_beads_timestamp", "timestamp"),
        Index("ix_beads_parent_id", "parent_id"),
    )


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String(40), primary_key=True)  # SHA-1 hash
    thread_id = Column(String(40), nullable=False)
    branch_name = Column(String(50), nullable=False, default="main")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Indexes
    __table_args__ = (Index("ix_sessions_thread_branch", "thread_id", "branch_name"),)

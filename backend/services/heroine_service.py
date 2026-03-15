"""
HeroineService - Business logic for heroine creation and management.
"""
from typing import Optional, Dict, Any

from llm.service import LLMService
from infrastructure.database.repositories.character_repo import CharacterRepository
from services.storage_service import StorageService


class HeroineService:
    """Service for heroine-related operations."""

    def __init__(
        self,
        llm_service: LLMService,
        character_repo: CharacterRepository,
        storage: StorageService
    ):
        self.llm_service = llm_service
        self.character_repo = character_repo
        self.storage = storage

    async def create_heroine(
        self,
        description: str,
        input_mode: str = "text"
    ) -> Dict[str, Any]:
        """
        Create a new heroine from user description.

        Args:
            description: User's free-form description
            input_mode: "text", "questionnaire", or "import"

        Returns:
            Complete heroine data with soul, identity, voice
        """
        # Parse description into structured soul data via LLM
        soul_data = await self.llm_service.parse_heroine(description)

        # Generate identity and voice based on soul
        # For now, combine everything into a single character record
        heroine_data = {
            "id": self._generate_heroine_id(),
            "name": self._extract_name_from_soul(soul_data) or "Heroine",
            "role": "heroine",
            "soul_file_path": "",
            "identity_file_path": "",
            "voice_file_path": None,
            "cached_soul": soul_data,
            "cached_identity": {},  # TODO: generate via LLM
            "cached_voice": {}      # TODO: generate via LLM
        }

        # Persist to database
        heroine = await self.character_repo.create(heroine_data)

        # Write to files (for editability and version control)
        await self._write_heroine_files(heroine)

        return self._character_to_dict(heroine)

    async def get_heroine(self, heroine_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Retrieve heroine.
        If heroine_id is provided, fetch by ID.
        Otherwise, fetch the first heroine (assumes single heroine system).
        """
        if heroine_id:
            heroine = await self.character_repo.get_by_id(heroine_id)
        else:
            heroine = await self.character_repo.get_first_by_role("heroine")

        return self._character_to_dict(heroine) if heroine else None

    async def update_heroine(
        self,
        heroine_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Update heroine data."""
        heroine = await self.character_repo.update(heroine_id, updates)
        if heroine:
            await self._write_heroine_files(heroine)
        return self._character_to_dict(heroine) if heroine else None

    async def refine_heroine(
        self,
        heroine_id: str,
        feedback: str
    ) -> Dict[str, Any]:
        """
        AI-assisted refinement of heroine based on user feedback.
        """
        heroine = await self.character_repo.get_by_id(heroine_id)
        if not heroine:
            raise ValueError(f"Heroine {heroine_id} not found")

        # Use LLM to refine soul structure
        refined_soul = await self.llm_service.refine_npc(
            heroine.cached_soul,
            feedback
        )

        # Update heroine
        heroine.cached_soul = refined_soul
        await self.character_repo.update(heroine_id, {"cached_soul": refined_soul})
        await self._write_heroine_files(heroine)

        return self._character_to_dict(heroine)

    def _generate_heroine_id(self) -> str:
        """Generate unique heroine ID."""
        import uuid
        return f"heroine_{uuid.uuid4().hex[:12]}"

    def _extract_name_from_soul(self, soul_data: Dict[str, Any]) -> Optional[str]:
        """
        Try to extract name from soul data.
        Soul data may or may not contain a name field.
        """
        # Check for explicit name field
        if "name" in soul_data:
            return soul_data["name"]

        # Could infer from identity later
        return None

    async def _write_heroine_files(self, heroine) -> None:
        """
        Write heroine data to soul.md, identity.md, voice.toml files.
        """
        heroine_id = heroine.id
        data_dir = self.storage.data_dir / "heroines" / heroine_id

        # Write soul.md
        soul_content = self._format_soul_md(heroine.cached_soul)
        await self.storage.write_file(
            data_dir / "soul.md",
            soul_content
        )

        # Write identity.md
        identity_content = self._format_identity_md(heroine.cached_identity)
        await self.storage.write_file(
            data_dir / "identity.md",
            identity_content
        )

        # Write voice.toml if voice exists
        if heroine.cached_voice:
            voice_content = self._format_voice_toml(heroine.cached_voice)
            await self.storage.write_file(
                data_dir / "voice.toml",
                voice_content
            )

    def _format_soul_md(self, soul_data: Dict[str, Any]) -> str:
        """Format soul data as Markdown."""
        lines = ["# Soul Structure\n"]
        if "core_traumas" in soul_data:
            lines.append("## Core Traumas\n")
            for trauma in soul_data["core_traumas"]:
                lines.append(f"- **Event**: {trauma.get('event', 'N/A')}")
                lines.append(f"  - Emotional Impact: {trauma.get('emotional_impact', 'N/A')}\n")
        if "defense_mechanisms" in soul_data:
            lines.append("## Defense Mechanisms\n")
            for mech in soul_data["defense_mechanisms"]:
                lines.append(f"- {mech}\n")
        if "ideal_type" in soul_data:
            lines.append("## Ideal Type\n")
            ideal = soul_data["ideal_type"]
            if "attraction_traits" in ideal:
                lines.append("### Attraction Traits")
                for trait in ideal["attraction_traits"]:
                    lines.append(f"- {trait}")
            if "aversion_traits" in ideal:
                lines.append("### Aversion Traits")
                for trait in ideal["aversion_traits"]:
                    lines.append(f"- {trait}")
        if "scene_preferences" in soul_data:
            lines.append("## Scene Preferences\n")
            for pref in soul_data["scene_preferences"]:
                lines.append(f"- {pref}")
        return "\n".join(lines)

    def _format_identity_md(self, identity_data: Dict[str, Any]) -> str:
        """Format identity data as Markdown."""
        lines = ["# Identity\n"]
        for key, value in identity_data.items():
            lines.append(f"## {key.replace('_', ' ').title()}\n")
            if isinstance(value, dict):
                for k, v in value.items():
                    lines.append(f"- **{k}**: {v}")
            elif isinstance(value, list):
                for item in value:
                    lines.append(f"- {item}")
            else:
                lines.append(str(value))
            lines.append("")
        return "\n".join(lines)

    def _format_voice_toml(self, voice_data: Dict[str, Any]) -> str:
        """Format voice data as TOML."""
        import toml
        return toml.dumps(voice_data)

    def _character_to_dict(self, character) -> Dict[str, Any]:
        """Convert Character model to API response dict."""
        return {
            "id": character.id,
            "name": character.name,
            "role": character.role,
            "soul": character.cached_soul,
            "identity": character.cached_identity,
            "voice": character.cached_voice,
            "created_at": character.created_at.isoformat() if hasattr(character, 'created_at') else None,
            "updated_at": character.updated_at.isoformat() if hasattr(character, 'updated_at') else None
        }

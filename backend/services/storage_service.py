"""
StorageService - File system operations for character and scene data.
"""
from pathlib import Path
from typing import Dict, Any, Optional
import aiofiles
import toml
import yaml
from config import settings


class StorageService:
    """Service for file system storage operations."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(settings.data_dir)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Ensure required directories exist (sync version for init)."""
        # Create directories if not exist
        (self.data_dir / "heroine").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "npcs").mkdir(parents=True, exist_ok=True)
        (self.data_dir / "scenes").mkdir(parents=True, exist_ok=True)

    async def save_heroine_data(
        self,
        soul: Dict[str, Any],
        identity: Dict[str, Any],
        voice: Dict[str, Any],
        heroine_id: Optional[str] = None
    ) -> str:
        """Save heroine data to files."""
        if not heroine_id:
            from datetime import datetime
            heroine_id = f"heroine_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

        heroine_dir = self.data_dir / "heroine" / heroine_id
        await self._ensure_dir_async(heroine_dir)

        # Save files
        await self._write_file(
            heroine_dir / "soul.md",
            self._format_soul_md(soul)
        )
        await self._write_file(
            heroine_dir / "identity.md",
            self._format_identity_md(identity)
        )
        await self._write_file(
            heroine_dir / "voice.toml",
            self._format_voice_toml(voice)
        )

        return heroine_id

    async def load_heroine_data(self, heroine_id: str) -> Optional[Dict[str, Any]]:
        """Load heroine data from files."""
        heroine_dir = self.data_dir / "heroine" / heroine_id

        if not await self._exists(heroine_dir):
            return None

        try:
            soul_md = await self._read_file(heroine_dir / "soul.md")
            soul = self._parse_soul_md(soul_md)

            identity_md = await self._read_file(heroine_dir / "identity.md")
            identity = self._parse_identity_md(identity_md)

            voice_toml = await self._read_file(heroine_dir / "voice.toml")
            voice = toml.loads(voice_toml)

            return {"soul": soul, "identity": identity, "voice": voice}
        except Exception as e:
            print(f"Error loading heroine {heroine_id}: {e}")
            return None

    async def save_npc_data(self, npc_id: str, npc_data: Dict[str, Any]) -> None:
        """Save NPC data to files."""
        npc_dir = self.data_dir / "npcs" / npc_id
        await self._ensure_dir_async(npc_dir)

        await self._write_file(
            npc_dir / "soul.md",
            self._format_soul_md(npc_data["soul"])
        )
        await self._write_file(
            npc_dir / "identity.md",
            self._format_identity_md(npc_data["identity"])
        )
        await self._write_file(
            npc_dir / "voice.toml",
            self._format_voice_toml(npc_data["voice"])
        )

    async def load_npc_data(self, npc_id: str) -> Optional[Dict[str, Any]]:
        """Load NPC data from files."""
        npc_dir = self.data_dir / "npcs" / npc_id

        if not await self._exists(npc_dir):
            return None

        try:
            soul_md = await self._read_file(npc_dir / "soul.md")
            soul = self._parse_soul_md(soul_md)

            identity_md = await self._read_file(npc_dir / "identity.md")
            identity = self._parse_identity_md(identity_md)

            voice_toml = await self._read_file(npc_dir / "voice.toml")
            voice = toml.loads(voice_toml)

            return {"soul": soul, "identity": identity, "voice": voice}
        except Exception as e:
            print(f"Error loading NPC {npc_id}: {e}")
            return None

    async def save_scene_data(self, scene_id: str, scene_data: Dict[str, Any]) -> None:
        """Save scene configuration to TOML file."""
        scenes_dir = self.data_dir / "scenes"
        await self._ensure_dir_async(scenes_dir)

        scene_path = scenes_dir / f"{scene_id}.toml"
        await self._write_file(scene_path, toml.dumps(scene_data))

    async def load_scene_data(self, scene_id: str) -> Optional[Dict[str, Any]]:
        """Load scene configuration."""
        scene_path = self.data_dir / "scenes" / f"{scene_id}.toml"

        if not await self._exists(scene_path):
            return None

        try:
            content = await self._read_file(scene_path)
            return toml.loads(content)
        except Exception as e:
            print(f"Error loading scene {scene_id}: {e}")
            return None

    # Helper methods

    async def _ensure_dir_async(self, path: Path) -> None:
        """Ensure directory exists asynchronously."""
        await aiofiles.os.makedirs(path, exist_ok=True)

    async def _write_file(self, path: Path, content: str) -> None:
        """Write file asynchronously."""
        async with aiofiles.open(path, "w") as f:
            await f.write(content)

    async def _read_file(self, path: Path) -> str:
        """Read file asynchronously."""
        async with aiofiles.open(path, "r") as f:
            return await f.read()

    async def _exists(self, path: Path) -> bool:
        """Check if path exists asynchronously."""
        try:
            await aiofiles.os.stat(path)
            return True
        except FileNotFoundError:
            return False

    def _format_soul_md(self, soul: Dict[str, Any]) -> str:
        """Format soul as Markdown with YAML frontmatter."""
        yaml_content = f"""---
core_traumas: {yaml.dump(soul.get('core_traumas', []))}
defense_mechanisms: {yaml.dump(soul.get('defense_mechanisms', []))}
ideal_type: {yaml.dump(soul.get('ideal_type', {}))}
scene_preferences: {yaml.dump(soul.get('scene_preferences', []))}
---

# Soul Structure

## Core Traumas
{chr(10).join(f'- {t}' for t in soul.get('core_traumas', []))}

## Defense Mechanisms
{chr(10).join(f'- {m}' for m in soul.get('defense_mechanisms', []))}

## Ideal Type
- Attraction: {', '.join(soul.get('ideal_type', {}).get('attraction_traits', []))}
- Aversion: {', '.join(soul.get('ideal_type', {}).get('aversion_traits', []))}

## Scene Preferences
{chr(10).join(f'- {p}' for p in soul.get('scene_preferences', []))}
"""
        return yaml_content

    def _parse_soul_md(self, content: str) -> Dict[str, Any]:
        """Parse soul from Markdown YAML frontmatter."""
        import re
        match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        yaml_str = match.group(1)
        data = yaml.safe_load(yaml_str)
        return data or {}

    def _format_identity_md(self, identity: Any) -> str:
        """Format identity as Markdown."""
        if isinstance(identity, dict):
            name = identity.get('name', 'Unknown')
            age = identity.get('age', 'Unknown')
            appearance = identity.get('appearance', '')
            personality = identity.get('personality', '')
            backstory = identity.get('backstory', '')
        else:
            name = getattr(identity, 'name', 'Unknown')
            age = getattr(identity, 'age', 'Unknown')
            appearance = getattr(identity, 'appearance', '')
            personality = getattr(identity, 'personality', '')
            backstory = getattr(identity, 'backstory', '')

        return f"""---
name: {name}
age: {age}
---

# {name}

## Appearance
{appearance}

## Personality
{personality}

## Backstory
{backstory}
"""

    def _parse_identity_md(self, content: str) -> Dict[str, Any]:
        """Parse identity from Markdown."""
        import re
        match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return {}

        yaml_str = match.group(1)
        data = yaml.safe_load(yaml_str)
        return data or {}

    def _format_voice_toml(self, voice: Dict[str, Any]) -> str:
        """Format voice config as TOML."""
        return toml.dumps(voice)

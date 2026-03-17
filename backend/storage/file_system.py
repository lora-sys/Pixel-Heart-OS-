"""
Storage Service for file system operations.
Handles Markdown and TOML file I/O for character data.
"""

import os
import json
from typing import Dict, Any, Optional
from pathlib import Path


class FileSystemService:
    """Service for file system storage operations."""

    def __init__(self, data_dir: str = "data"):
        """Initialize FileSystemService.

        Args:
            data_dir: Base directory for data storage
        """
        self.data_dir = Path(data_dir)
        self.heroine_dir = self.data_dir / "heroine"
        self.npcs_dir = self.data_dir / "npcs"
        self.scenes_dir = self.data_dir / "scenes"

        self._ensure_directories()

    def _ensure_directories(self):
        """Create necessary directories if they don't exist."""
        self.heroine_dir.mkdir(parents=True, exist_ok=True)
        self.npcs_dir.mkdir(parents=True, exist_ok=True)
        self.scenes_dir.mkdir(parents=True, exist_ok=True)

    async def write_file(self, relative_path: str, content: str) -> str:
        """Write content to a file.

        Args:
            relative_path: Path relative to data_dir
            content: Content to write

        Returns:
            Full path to the file
        """
        full_path = self.data_dir / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return str(full_path)

    async def read_file(self, relative_path: str) -> Optional[str]:
        """Read content from a file.

        Args:
            relative_path: Path relative to data_dir

        Returns:
            File content or None if not found
        """
        full_path = self.data_dir / relative_path

        if not full_path.exists():
            return None

        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    async def write_heroine_soul(self, soul_data: Dict[str, Any]) -> str:
        """Write heroine soul data.

        Args:
            soul_data: Soul data dictionary

        Returns:
            Path to the file
        """
        content = self._dict_to_markdown(soul_data, "Soul")
        return await self.write_file("heroine/soul.md", content)

    async def write_heroine_identity(self, identity_data: Dict[str, Any]) -> str:
        """Write heroine identity data.

        Args:
            identity_data: Identity data dictionary

        Returns:
            Path to the file
        """
        content = self._dict_to_markdown(identity_data, "Identity")
        return await self.write_file("heroine/identity.md", content)

    async def write_heroine_voice(self, voice_data: Dict[str, Any]) -> str:
        """Write heroine voice config.

        Args:
            voice_data: Voice data dictionary

        Returns:
            Path to the file
        """
        content = json.dumps(voice_data, indent=2)
        return await self.write_file("heroine/voice.json", content)

    async def load_heroine_soul(self) -> Optional[Dict[str, Any]]:
        """Load heroine soul data.

        Returns:
            Soul data or None
        """
        content = await self.read_file("heroine/soul.md")
        if content:
            return self._markdown_to_dict(content)
        return None

    async def load_heroine_identity(self) -> Optional[Dict[str, Any]]:
        """Load heroine identity data.

        Returns:
            Identity data or None
        """
        content = await self.read_file("heroine/identity.md")
        if content:
            return self._markdown_to_dict(content)
        return None

    async def load_heroine_voice(self) -> Optional[Dict[str, Any]]:
        """Load heroine voice config.

        Returns:
            Voice data or None
        """
        content = await self.read_file("heroine/voice.json")
        if content:
            return json.loads(content)
        return None

    async def write_npc_data(self, npc_id: str, npc_data: Dict[str, Any]) -> str:
        """Write NPC data.

        Args:
            npc_id: NPC identifier
            npc_data: NPC data dictionary

        Returns:
            Path to the file
        """
        content = self._dict_to_markdown(npc_data, f"NPC {npc_id}")
        return await self.write_file(f"npcs/{npc_id}.md", content)

    async def load_npc_data(self, npc_id: str) -> Optional[Dict[str, Any]]:
        """Load NPC data.

        Args:
            npc_id: NPC identifier

        Returns:
            NPC data or None
        """
        content = await self.read_file(f"npcs/{npc_id}.md")
        if content:
            return self._markdown_to_dict(content)
        return None

    def _dict_to_markdown(self, data: Dict[str, Any], title: str) -> str:
        """Convert dictionary to markdown format.

        Args:
            data: Dictionary to convert
            title: Title for the markdown

        Returns:
            Markdown string
        """
        lines = [f"# {title}", ""]

        def format_value(key: str, value: Any, indent: int = 0) -> list:
            prefix = "  " * indent
            if isinstance(value, dict):
                result = [f"{prefix}## {key}", ""]
                for k, v in value.items():
                    result.extend(format_value(k, v, indent + 1))
                return result
            elif isinstance(value, list):
                result = [f"{prefix}### {key}", ""]
                for item in value:
                    result.append(f"{prefix}- {item}")
                return result
            else:
                return [f"{prefix}**{key}**: {value}"]

        for key, value in data.items():
            lines.extend(format_value(key, value))
            lines.append("")

        return "\n".join(lines)

    def _markdown_to_dict(self, content: str) -> Dict[str, Any]:
        """Parse markdown back to dictionary (simplified).

        Args:
            content: Markdown content

        Returns:
            Parsed dictionary
        """
        result = {}
        current_key = None

        for line in content.split("\n"):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("**") and "**:" in line:
                parts = line.split("**:", 1)
                if len(parts) == 2:
                    key = parts[0].replace("**", "").strip()
                    value = parts[1].strip()
                    result[key] = value

        return result

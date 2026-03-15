"""
File system storage for markdown/toml character and scene files.
"""
import os
import json
import toml
from pathlib import Path
from typing import Dict, Any, Optional
import aiofiles
from datetime import datetime
from config import settings


DATA_DIR = Path(settings.data_dir)


async def ensure_dir(path: Path) -> None:
    """Ensure directory exists."""
    await aiofiles.os.makedirs(path, exist_ok=True)


async def save_heroine_data(
    soul: Any,
    identity: Any,
    voice: Any,
    heroine_id: Optional[str] = None
) -> str:
    """
    Save heroine data to files.
    Returns heroine_id.
    """
    if not heroine_id:
        heroine_id = f"heroine_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"

    heroine_dir = DATA_DIR / "heroine" / heroine_id
    await ensure_dir(heroine_dir)

    # Save soul.md (YAML frontmatter + Markdown)
    soul_content = format_soul_md(soul)
    async with aiofiles.open(heroine_dir / "soul.md", "w") as f:
        await f.write(soul_content)

    # Save identity.md
    identity_content = format_identity_md(identity)
    async with aiofiles.open(heroine_dir / "identity.md", "w") as f:
        await f.write(identity_content)

    # Save voice.toml
    voice_content = format_voice_toml(voice)
    async with aiofiles.open(heroine_dir / "voice.toml", "w") as f:
        await f.write(voice_content)

    return heroine_id


async def load_heroine_data(heroine_id: str) -> Optional[Dict[str, Any]]:
    """Load heroine data from files."""
    heroine_dir = DATA_DIR / "heroine" / heroine_id

    if not await aiofiles.os.path.exists(heroine_dir):
        return None

    try:
        async with aiofiles.open(heroine_dir / "soul.md", "r") as f:
            soul_md = await f.read()
            soul = parse_soul_md(soul_md)

        async with aiofiles.open(heroine_dir / "identity.md", "r") as f:
            identity_md = await f.read()
            identity = parse_identity_md(identity_md)

        async with aiofiles.open(heroine_dir / "voice.toml", "r") as f:
            voice_toml = await f.read()
            voice = toml.loads(voice_toml)

        return {"soul": soul, "identity": identity, "voice": voice}
    except Exception as e:
        print(f"Error loading heroine {heroine_id}: {e}")
        return None


async def save_npc_data(npc_id: str, npc_data: Dict[str, Any]) -> None:
    """Save NPC data to files."""
    npc_dir = DATA_DIR / "npcs" / npc_id
    await ensure_dir(npc_dir)

    # soul.md
    soul_content = format_soul_md(npc_data["soul"])
    async with aiofiles.open(npc_dir / "soul.md", "w") as f:
        await f.write(soul_content)

    # identity.md
    identity_content = format_identity_md(npc_data["identity"])
    async with aiofiles.open(npc_dir / "identity.md", "w") as f:
        await f.write(identity_content)

    # voice.toml
    voice_content = format_voice_toml(npc_data["voice"])
    async with aiofiles.open(npc_dir / "voice.toml", "w") as f:
        await f.write(voice_content)


async def load_npc_data(npc_id: str) -> Optional[Dict[str, Any]]:
    """Load NPC data from files."""
    npc_dir = DATA_DIR / "npcs" / npc_id

    if not await aiofiles.os.path.exists(npc_dir):
        return None

    try:
        async with aiofiles.open(npc_dir / "soul.md", "r") as f:
            soul_md = await f.read()
            soul = parse_soul_md(soul_md)

        async with aiofiles.open(npc_dir / "identity.md", "r") as f:
            identity_md = await f.read()
            identity = parse_identity_md(identity_md)

        async with aiofiles.open(npc_dir / "voice.toml", "r") as f:
            voice_toml = await f.read()
            voice = toml.loads(voice_toml)

        return {"soul": soul, "identity": identity, "voice": voice}
    except Exception as e:
        print(f"Error loading NPC {npc_id}: {e}")
        return None


async def save_scene_data(scene_id: str, scene_data: Dict[str, Any]) -> None:
    """Save scene configuration to TOML file."""
    scenes_dir = DATA_DIR / "scenes"
    await ensure_dir(scenes_dir)

    scene_path = scenes_dir / f"{scene_id}.toml"
    content = toml.dumps(scene_data)

    async with aiofiles.open(scene_path, "w") as f:
        await f.write(content)


async def load_scene_data(scene_id: str) -> Optional[Dict[str, Any]]:
    """Load scene configuration."""
    scene_path = DATA_DIR / "scenes" / f"{scene_id}.toml"

    if not await aiofiles.os.path.exists(scene_path):
        return None

    try:
        async with aiofiles.open(scene_path, "r") as f:
            content = await f.read()
            return toml.loads(content)
    except Exception as e:
        print(f"Error loading scene {scene_id}: {e}")
        return None


# === Formatting helpers ===

def format_soul_md(soul: Dict[str, Any]) -> str:
    """Format soul as Markdown with YAML frontmatter."""
    yaml_content = f"""---
core_traumas: {json.dumps(soul.get('core_traumas', []), ensure_ascii=False)}
defense_mechanisms: {json.dumps(soul.get('defense_mechanisms', []), ensure_ascii=False)}
ideal_type: {json.dumps(soul.get('ideal_type', {}), ensure_ascii=False)}
scene_preferences: {json.dumps(soul.get('scene_preferences', []), ensure_ascii=False)}
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


def parse_soul_md(content: str) -> Dict[str, Any]:
    """Parse soul from Markdown YAML frontmatter."""
    import re
    match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    yaml_str = match.group(1)
    import yaml
    data = yaml.safe_load(yaml_str)
    return data or {}


def format_identity_md(identity: Any) -> str:
    """Format identity as Markdown."""
    if isinstance(identity, dict):
        name = identity.get('name', 'Unknown')
        age = identity.get('age', 'Unknown')
        appearance = identity.get('appearance', '')
        personality = identity.get('personality', '')
        backstory = identity.get('backstory', '')
    else:
        # Assume it's a Pydantic model
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


def parse_identity_md(content: str) -> Dict[str, Any]:
    """Parse identity from Markdown."""
    import re
    match = re.search(r'---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}

    yaml_str = match.group(1)
    import yaml
    data = yaml.safe_load(yaml_str)
    return data or {}


def format_voice_toml(voice: Dict[str, Any]) -> str:
    """Format voice config as TOML."""
    return toml.dumps(voice)


# Initialize data directory on module import
import asyncio
asyncio.create_task(ensure_dir(DATA_DIR))
asyncio.create_task(ensure_dir(DATA_DIR / "heroine"))
asyncio.create_task(ensure_dir(DATA_DIR / "npcs"))
asyncio.create_task(ensure_dir(DATA_DIR / "scenes"))

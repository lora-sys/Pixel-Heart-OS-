"""
LLM Service for Anthropic API integration.
Provides methods for heroine parsing, NPC generation, and dialogue generation.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from anthropic import Anthropic

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"


class LLMService:
    """Service for LLM interactions using Anthropic API."""

    def __init__(self, use_mock: bool = False):
        """Initialize LLM service.

        Args:
            use_mock: If True, return mock responses instead of calling API
        """
        self.use_mock = use_mock or os.getenv("USE_MOCK_LLM", "false").lower() == "true"
        self.client = (
            None if self.use_mock else Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        )
        self.model = os.getenv("ANTHROPIC_MODEL", "claude-3-haiku-20240307")
        self._prompts: Dict[str, str] = {}
        self._load_prompts()

    def _load_prompts(self):
        """Load all prompt templates from files."""
        prompt_files = {
            "heroine_parsing": "heroine_parsing.txt",
            "npc_generation": "npc_generation.txt",
            "dialogue_generation": "dialogue_generation.txt",
            "scene_generation": "scene_generation.txt",
        }

        for key, filename in prompt_files.items():
            prompt_path = PROMPTS_DIR / filename
            if prompt_path.exists():
                self._prompts[key] = prompt_path.read_text(encoding="utf-8")
            else:
                print(f"Warning: Prompt file {filename} not found")
                self._prompts[key] = ""

    async def parse_heroine_description(self, description: str) -> Dict[str, Any]:
        """Parse natural language description into soul, identity, and voice."""
        if self.use_mock:
            return self._mock_heroine_parsing(description)

        prompt = self._prompts.get("heroine_parsing", "").format(
            description=description
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    async def generate_npc_personality(
        self, archetype: str, context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate NPC personality based on archetype."""
        if self.use_mock:
            return self._mock_npc_generation(archetype)

        heroine_name = context.get("heroine_name", "the heroine")
        prompt = self._prompts.get("npc_generation", "").format(
            archetype=archetype, heroine_name=heroine_name
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    async def generate_dialogue(
        self, npc: Dict[str, Any], context: Dict[str, Any], player_action: str
    ) -> str:
        """Generate NPC dialogue response."""
        if self.use_mock:
            return f"[{npc.get('name', 'NPC')}] I understand your action: {player_action[:50]}..."

        npc_name = npc.get("name", "NPC")
        npc_personality = npc.get("personality", {})
        dialogue_style = npc.get("dialogue_style", {})
        tone = dialogue_style.get("tone", "neutral")
        history = json.dumps(context.get("history", [])[-3:])

        prompt = self._prompts.get("dialogue_generation", "").format(
            npc_name=npc_name,
            npc_personality=npc_personality,
            tone=tone,
            history=history,
            player_action=player_action,
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        return message.content[0].text.strip()

    async def generate_scene_description(
        self, location: str, participants: List[str], atmosphere: str
    ) -> Dict[str, Any]:
        """Generate scene description."""
        if self.use_mock:
            return {
                "title": f"Scene at {location}",
                "description": f"The characters meet in {location}. The atmosphere is {atmosphere}.",
                "sensory_details": [
                    "The air feels still",
                    "Sounds echo in the distance",
                ],
                "mood": atmosphere,
            }

        prompt = self._prompts.get("scene_generation", "").format(
            location=location,
            participants=", ".join(participants),
            atmosphere=atmosphere,
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        response_text = message.content[0].text
        return json.loads(response_text)

    def _mock_heroine_parsing(self, description: str) -> Dict[str, Any]:
        """Mock response for heroine parsing."""
        import hashlib

        hash_val = hashlib.md5(description.encode()).hexdigest()[:8]

        return {
            "soul": {
                "core_personality": f"Determined and compassionate individual inspired by: {description[:50]}...",
                "motivations": [
                    "To protect loved ones",
                    "To find truth",
                    "To overcome adversity",
                ],
                "fears": ["Failure", "Losing control", "Being powerless"],
                "values": ["Honesty", "Courage", "Compassion"],
                "quirks": [
                    "Tends to bite lip when thinking",
                    "Always carries a small token",
                ],
                "internal_conflict": "Balancing personal desires with responsibility to others",
            },
            "identity": {
                "name": f"Heroine_{hash_val}",
                "age": 20,
                "appearance": {
                    "hair_color": "blonde",
                    "eye_color": "green",
                    "height": "157cm",
                    "build": "athletic",
                },
                "background": {
                    "hometown": "A small coastal village",
                    "family": "Raised by grandparents after parents disappeared",
                    "education": "Self-taught through observation and experience",
                    "occupation": "Explorer and protector of the realm",
                },
            },
            "voice": {
                "speech_pattern": "Thoughtful and measured, chooses words carefully",
                "tone": "warm",
                "vocabulary": "formal",
                "catchphrase": "I will not back down from what is right",
                "language_quirks": [
                    "Uses metaphors from nature",
                    "Speaks in proverbs when thoughtful",
                ],
            },
        }

    def _mock_npc_generation(self, archetype: str) -> Dict[str, Any]:
        """Mock response for NPC generation."""
        personalities = {
            "Protector": {"trait1": "brave", "trait2": "loyal", "trait3": "protective"},
            "Competitor": {
                "trait1": "ambitious",
                "trait2": "driven",
                "trait3": "competitive",
            },
            "Shadow": {
                "trait1": "mysterious",
                "trait2": "enigmatic",
                "trait3": "secretive",
            },
            "Ally": {"trait1": "kind", "trait2": "supportive", "trait3": "trustworthy"},
            "Mentor": {"trait1": "wise", "trait2": "experienced", "trait3": "patient"},
        }

        return {
            "name": f"{archetype}_{hash(archetype) % 100}",
            "personality": personalities.get(archetype, {"trait1": "neutral"}),
            "backstory": f"A {archetype.lower()} who has seen much in their time.",
            "dialogue_style": {
                "tone": "measured",
                "mannerisms": ["Pauses before speaking", "Uses hand gestures"],
                "vocabulary_level": "moderate",
            },
            "relationship_to_heroine": "complicated",
        }

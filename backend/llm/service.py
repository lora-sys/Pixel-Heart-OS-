"""
LLM service with multiple provider support (Anthropic, StepFun, Mock).
"""
import os
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from anthropic import AsyncAnthropic
import httpx
import yaml
import json
from config import settings


class BaseLLMProvider(ABC):
    """Abstract base for LLM providers."""

    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Generate text from prompt."""
        pass

    @abstractmethod
    async def parse_heroine(self, description: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_npc(self, heroine_soul: Dict[str, Any], role: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_scene(self, preferences: List[str]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def simulate_npc_response(
        self,
        npc: Dict[str, Any],
        context: str,
        player_action: str
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def refine_npc(self, npc_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        pass


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude API provider."""

    def __init__(self, api_key: str, model: str, temperature: float, max_tokens: int):
        self.client = AsyncAnthropic(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", self.max_tokens),
            temperature=kwargs.get("temperature", self.temperature),
            messages=messages
        )
        return response.content[0].text

    async def parse_heroine(self, description: str) -> Dict[str, Any]:
        prompt = f"""You are a narrative psychologist. Analyze this character description and extract structured information.

User description:
```
{description}
```

Return a YAML document with this exact structure:
```yaml
core_traumas:
  - event: "brief description"
    emotional_impact: "emotion word"
defense_mechanisms:
  - "mechanism name"
ideal_type:
  attraction_traits:
    - "trait"
  aversion_traits:
    - "trait"
scene_preferences:
  - "scene type like rainy_window, midnight_store"
```

Be concise and extract only from the description. If information is missing, use empty lists/dicts.
"""
        content = await self.generate(prompt, temperature=0.5)
        return self._extract_yaml(content)

    async def generate_npc(self, heroine_soul: Dict[str, Any], role: str) -> Dict[str, Any]:
        role_desc = self._get_role_description(role)
        prompt = f"""Based on this heroine's soul structure:

Soul:
- Core traumas: {heroine_soul.get('core_traumas', [])}
- Defense mechanisms: {heroine_soul.get('defense_mechanisms', [])}
- Ideal type: {heroine_soul.get('ideal_type', {})}
- Scene preferences: {heroine_soul.get('scene_preferences', [])}

{role_desc}

Generate the NPC's complete data as a YAML document with this structure:

```yaml
soul:
  key_traits:
    - "list of defining personality traits"
  backstory: "brief backstory explaining why they are this way"
  connection_to_heroine: "how they relate to heroine's traumas/ideals"
identity:
  name: "NPC name"
  age: 25
  appearance: "visual description for pixel art"
  personality: "summary"
  backstory: "fuller narrative"
voice:
  speech_patterns:
    filler_words: ["um", "like"]
    sentence_ends: ["...", "!"]
  vocabulary:
    level: "colloquial"
    quirks: ["specific phrases"]
  emotional_tone:
    primary: "dominant emotion"
    secondary: "secondary emotion"
```

Be creative but ensure the NPC is clearly a {role} derived from the heroine's psychology.
"""
        content = await self.generate(prompt, temperature=0.8)
        return self._extract_yaml(content)

    async def generate_scene(self, preferences: List[str]) -> Dict[str, Any]:
        pref_str = ", ".join(preferences) if preferences else "any atmospheric setting"
        prompt = f"""Generate a scene configuration for a pixel art visual novel. Heroine prefers: {pref_str}.

Return JSON with this structure:
{{
  "name": "Scene Name",
  "description": "Brief atmospheric description",
  "environment": {{
    "location_type": "indoor/outdoor",
    "time_of_day": "evening",
    "weather": "rainy",
    "lighting": "neon/soft"
  }},
  "mood": "emotional atmosphere (melancholy, cozy, tense)",
  "triggers": ["list of narrative triggers"],
  "npc_presences": [
    {{"npc_role": "protector", "probability": 0.7, "position": "left"}}
  ],
  "background_music": "ambient description",
  "lighting": "color palette description"
}}

Make it visually striking and emotionally resonant. Output only JSON, no extra text.
"""
        content = await self.generate(prompt, temperature=0.7, max_tokens=2000)
       return self._extract_json(content)

    async def simulate_npc_response(
        self,
        npc: Dict[str, Any],
        context: str,
        player_action: str
    ) -> Dict[str, Any]:
        prompt = f"""You are roleplaying as {npc['identity']['name']}.

NPC Profile:
- Soul: {npc['soul']}
- Personality: {npc['identity']['personality']}
- Voice: {npc['voice']}

Context (recent conversation):
{context}

Player says: "{player_action}"

Generate:
1. NPC dialogue (2-3 sentences, in character)
2. Primary emotion expressed
3. Relationship change delta (-0.1 to +0.3) based on interaction quality

Output as JSON:
{{
  "dialogue": "string",
  "emotion": "emotion_word",
  "relationship_delta": 0.15,
  "justification": "brief reason for delta"
}}

Stay in character. Be emotionally authentic.
"""
        content = await self.generate(prompt, temperature=0.8, max_tokens=500)
        return self._extract_json(content)

    async def refine_npc(self, npc_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        prompt = f"""Current NPC data:

Soul: {npc_data.get('soul', {})}
Identity: {npc_data.get('identity', {})}
Voice: {npc_data.get('voice', {})}

User feedback: "{feedback}"

Revise the NPC's soul, identity, and voice to address the feedback. Make it more nuanced, complex, or aligned with user's vision.

Return updated YAML structure (same format as input):
```yaml
soul:
  ...
identity:
  ...
voice:
  ...
```
"""
        content = await self.generate(prompt, temperature=0.6, max_tokens=3000)
        return self._extract_yaml(content)

    def _get_role_description(self, role: str) -> str:
        descriptions = {
            "protector": "A protector NPC reflects the heroine's trauma and defense mechanisms. They are overly protective, possibly to the point of smothering. They represent the urge to keep the heroine safe from perceived threats.",
            "competitor": "A competitor NPC embodies conflicts with the heroine's ideal type. They challenge the heroine's desires and represent what she finds intimidating or undesirable in potential partners.",
            "shadow": "A shadow NPC represents the heroine's repressed traits and hidden aspects. They are mysterious, possibly dark, and reveal what the heroine refuses to acknowledge in herself."
        }
        return descriptions.get(role, f"A {role} NPC")

    def _extract_yaml(self, content: str) -> Dict[str, Any]:
        """Extract YAML from response."""
        yaml_match = content.find('```yaml')
        if yaml_match != -1:
            yaml_end = content.find('```', yaml_match + 7)
            yaml_str = content[yaml_match+7:yaml_end].strip()
        else:
            yaml_str = content
        try:
            return yaml.safe_load(yaml_str) or {}
        except yaml.YAMLError:
            return {}

    def _extract_json(self, content: str) -> Dict[str, Any]:
        """Extract JSON from response."""
        json_match = content.find('{')
        if json_match != -1:
            json_end = content.rfind('}') + 1
            json_str = content[json_match:json_end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        return {}


class StepFunProvider(BaseLLMProvider):
    """StepFun (阶跃星辰) API provider - compatible with OpenAI format."""

    def __init__(self, api_key: str, base_url: str, model: str, temperature: float, max_tokens: int):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = httpx.AsyncClient(
            timeout=60.0,
            headers={"Authorization": f"Bearer {api_key}"}
        )

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", self.temperature),
            "max_tokens": kwargs.get("max_tokens", self.max_tokens)
        }

        resp = await self.client.post(f"{self.base_url}/v1/chat/completions", json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]

    async def parse_heroine(self, description: str) -> Dict[str, Any]:
        prompt = f"""Analyze this character description and extract structured YAML:

{description}

Return YAML:
```yaml
core_traumas:
  - event: "..."
    emotional_impact: "..."
defense_mechanisms: []
ideal_type:
  attraction_traits: []
  aversion_traits: []
scene_preferences: []
```
"""
        content = await self.generate(prompt, temperature=0.5)
        return self._extract_yaml(content)

    async def generate_npc(self, heroine_soul: Dict[str, Any], role: str) -> Dict[str, Any]:
        role_desc = self._get_role_description(role)
        prompt = f"""Heroine soul: {heroine_soul}

{role_desc}

Generate NPC as YAML:
```yaml
soul:
  key_traits: []
  backstory: "..."
  connection_to_heroine: "..."
identity:
  name: "..."
  age: 25
  appearance: "..."
  personality: "..."
  backstory: "..."
voice:
  speech_patterns: {{}}
  vocabulary: {{}}
  emotional_tone: {{}}
```
"""
        content = await self.generate(prompt, temperature=0.8)
        return self._extract_yaml(content)

    async def generate_scene(self, preferences: List[str]) -> Dict[str, Any]:
        prompt = f"""Preferences: {preferences}

Generate scene as JSON:
{{
  "name": "...",
  "description": "...",
  "environment": {{}},
  "mood": "...",
  "triggers": [],
  "npc_presences": []
}}
"""
        content = await self.generate(prompt, temperature=0.7)
        return self._extract_json(content)

    async def simulate_npc_response(
        self,
        npc: Dict[str, Any],
        context: str,
        player_action: str
    ) -> Dict[str, Any]:
        prompt = f"""You are {npc['identity']['name']}. Context: {context}. Player: {player_action}

Output JSON:
{{"dialogue": "...", "emotion": "...", "relationship_delta": 0.0}}
"""
        content = await self.generate(prompt, temperature=0.8)
        return self._extract_json(content)

    async def refine_npc(self, npc_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        prompt = f"Current: {npc_data}\n\nFeedback: {feedback}\n\nRevise and return YAML:"
        content = await self.generate(prompt, temperature=0.6)
        return self._extract_yaml(content)

    def _get_role_description(self, role: str) -> str:
        # Same as AnthropicProvider
        descriptions = {
            "protector": "A protector NPC reflects the heroine's trauma and defense mechanisms. They are overly protective, possibly to the point of smothering.",
            "competitor": "A competitor NPC embodies conflicts with the heroine's ideal type. They challenge the heroine's desires.",
            "shadow": "A shadow NPC represents the heroine's repressed traits and hidden aspects. They are mysterious."
        }
        return descriptions.get(role, f"A {role} NPC")

    def _extract_yaml(self, content: str) -> Dict[str, Any]:
        yaml_match = content.find('```yaml')
        if yaml_match != -1:
            yaml_end = content.find('```', yaml_match + 7)
            yaml_str = content[yaml_match+7:yaml_end].strip()
        else:
            yaml_str = content
        try:
            return yaml.safe_load(yaml_str) or {}
        except yaml.YAMLError:
            return {}

    def _extract_json(self, content: str) -> Dict[str, Any]:
        json_match = content.find('{')
        if json_match != -1:
            json_end = content.rfind('}') + 1
            json_str = content[json_match:json_end]
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        return {}


class MockLLMProvider(BaseLLMProvider):
    """Mock provider for testing without API key - returns preset data."""

    async def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        return "Mock response"

    async def parse_heroine(self, description: str) -> Dict[str, Any]:
        # Extract keywords from description to make it feel dynamic
        keywords = []
        for word in ["abandonment", "trauma", "anxiety", "protect", "shy", "librarian", "rockstar"]:
            if word.lower() in description.lower():
                keywords.append(word)
        return {
            "core_traumas": [
                {"event": "Mock trauma", "emotional_impact": "mock_impact"}
            ],
            "defense_mechanisms": ["mock_defense"],
            "ideal_type": {
                "attraction_traits": ["kind", "understanding"],
                "aversion_traits": ["cruel", "dismissive"]
            },
            "scene_preferences": ["rainy_window", "quiet_cafe", "library"]
        }

    async def generate_npc(self, heroine_soul: Dict[str, Any], role: str) -> Dict[str, Any]:
        names = {"protector": "Guardian", "competitor": "Rival", "shadow": "Shade"}
        return {
            "soul": {
                "key_traits": [f"{role}_trait1", f"{role}_trait2"],
                "backstory": f"A {role} who serves as {names[role]}",
                "connection_to_heroine": f"Connected via {role} archetype"
            },
            "identity": {
                "name": names[role],
                "age": 30,
                "appearance": f"Pixel art {role} character",
                "personality": f"Typical {role} personality",
                "backstory": f"Backstory for {role}"
            },
            "voice": {
                "speech_patterns": {"filler_words": ["..."], "sentence_ends": ["!"]},
                "vocabulary": {"level": "normal"},
                "emotional_tone": {"primary": role}
            }
        }

    async def generate_scene(self, preferences: List[str]) -> Dict[str, Any]:
        return {
            "name": "Mock Scene",
            "description": "A placeholder scene",
            "environment": {"location_type": "indoor", "time_of_day": "evening"},
            "mood": "neutral",
            "triggers": [],
            "npc_presences": []
        }

    async def simulate_npc_response(
        self,
        npc: Dict[str, Any],
        context: str,
        player_action: str
    ) -> Dict[str, Any]:
        return {
            "dialogue": f"[{npc['identity']['name']}] Hello, I'm a mock response!",
            "emotion": "neutral",
            "relationship_delta": 0.1
        }

    async def refine_npc(self, npc_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        # Return slightly modified version
        refined = npc_data.copy()
        if "identity" in refined:
            refined["identity"]["backstory"] += " (Refined with feedback)"
        return refined


class LLMService:
    """
    Unified LLM service with provider abstraction.
    Supports: Anthropic, StepFun, Mock (for testing)
    """

    def __init__(self):
        provider = settings.llm_provider

        if settings.use_mock_llm:
            self.provider = MockLLMProvider()
        elif provider == "anthropic":
            if not settings.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY is required when provider=anthropic")
            self.provider = AnthropicProvider(
                api_key=settings.anthropic_api_key,
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )
        elif provider == "stepfun":
            if not settings.stepfun_api_key:
                raise ValueError("STEPFUN_API_KEY is required when provider=stepfun")
            self.provider = StepFunProvider(
                api_key=settings.stepfun_api_key,
                base_url=settings.stepfun_base_url,
                model=settings.llm_model,
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )
        else:
            raise ValueError(f"Unknown LLM provider: {provider}")

    # Delegate all methods to provider
    async def parse_heroine(self, description: str) -> Dict[str, Any]:
        return await self.provider.parse_heroine(description)

    async def generate_npc(self, heroine_soul: Dict[str, Any], role: str) -> Dict[str, Any]:
        return await self.provider.generate_npc(heroine_soul, role)

    async def generate_scene(self, preferences: List[str]) -> Dict[str, Any]:
        return await self.provider.generate_scene(preferences)

    async def simulate_npc_response(
        self,
        npc: Dict[str, Any],
        context: str,
        player_action: str
    ) -> Dict[str, Any]:
        return await self.provider.simulate_npc_response(npc, context, player_action)

    async def refine_npc(self, npc_data: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        return await self.provider.refine_npc(npc_data, feedback)

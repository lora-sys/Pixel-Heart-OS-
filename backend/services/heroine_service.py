"""
Heroine Service for creating and managing heroine data.
Handles heroine creation from natural language descriptions using LLM parsing
and persists heroine data (soul, identity, voice) to storage.
"""

from typing import Dict, Optional, Any


class HeroineService:
    """
    Service for creating and managing heroine data.

    Responsibilities:
    - Create heroine from free-form natural language descriptions using LLM
    - Parse description into soul, identity, and voice components
    - Persist heroine data to storage system
    - Create bead records for heroine creation events
    - Retrieve current heroine data
    """

    def __init__(
        self,
        llm_service: Any = None,
        bead_service: Any = None,
        storage_service: Any = None,
    ):
        """
        Initialize HeroineService with dependencies (optional for development).

        Args:
            llm_service: Service for LLM interactions (parsing descriptions)
            bead_service: Service for creating bead records (DAG operations)
            storage_service: Service for persisting heroine data (MD/TOML files)
        """
        self.llm_service = llm_service
        self.bead_service = bead_service
        self.storage_service = storage_service
        self._heroine_data: Optional[Dict[str, Any]] = None

    async def create_heroine(self, description: str) -> Dict[str, Any]:
        """
        Create a heroine from a natural language description.

        For development, returns mock heroine data instead of calling LLM service.
        In production, this would:
        1. Use LLM to parse description into soul, identity, and voice
        2. Persist heroine data to storage (soul.md, identity.md, voice.toml)
        3. Create a bead record for the heroine creation event
        4. Return the created heroine data

        Args:
            description: Natural language description of the heroine

        Returns:
            Dictionary containing heroine data with keys:
            - soul: Dict with heroine's core personality and motivations
            - identity: Dict with heroine's background, appearance, etc.
            - voice: Dict with heroine's speech patterns and communication style

        Raises:
            Exception: If heroine creation fails at any step
        """
        try:
            # For development, return mock heroine data if LLM service is not available
            if self.llm_service is None:
                # Generate mock heroine data based on the description
                import hashlib

                description_hash = hashlib.md5(description.encode()).hexdigest()

                mock_soul = {
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
                }

                mock_identity = {
                    "name": f"Heroine_{description_hash[:8]}",
                    "age": 20
                    + (int(description_hash[0], 16) % 10),  # Age between 20-29
                    "appearance": {
                        "hair_color": ["black", "brown", "blonde", "red"][
                            int(description_hash[1], 16) % 4
                        ],
                        "eye_color": ["blue", "green", "brown", "hazel"][
                            int(description_hash[2], 16) % 4
                        ],
                        "height": f"{150 + (int(description_hash[3], 16) % 20)}cm",
                        "build": ["slender", "athletic", "curvy", "strong"][
                            int(description_hash[4], 16) % 4
                        ],
                    },
                    "background": {
                        "hometown": "A small coastal village",
                        "family": "Raised by grandparents after parents disappeared",
                        "education": "Self-taught through observation and experience",
                        "occupation": "Explorer and protector of the realm",
                    },
                }

                mock_voice = {
                    "speech_pattern": "Thoughtful and measured, chooses words carefully",
                    "tone": ["warm", "determined", "gentle", "resolute"][
                        int(description_hash[5], 16) % 4
                    ],
                    "vocabulary": ["formal", "casual", "poetic", "direct"][
                        int(description_hash[6], 16) % 4
                    ],
                    "catchphrase": "I will not back down from what is right",
                    "language_quirks": [
                        "Uses metaphors from nature",
                        "Speaks in proverbs when thoughtful",
                    ],
                }

                heroine_data = {
                    "soul": mock_soul,
                    "identity": mock_identity,
                    "voice": mock_voice,
                }

                # Store in instance variable for get_heroine to retrieve
                self._heroine_data = heroine_data
                return heroine_data

            # Step 1: Parse description using LLM
            # The LLM service should return structured data for soul, identity, voice
            parsed_data = await self.llm_service.parse_heroine_description(description)

            # Extract components - assuming LLM returns structured data
            soul = parsed_data.get("soul", {})
            identity = parsed_data.get("identity", {})
            voice = parsed_data.get("voice", {})

            # Step 2: Persist heroine data to storage
            await self.storage_service.write_heroine_soul(soul)
            await self.storage_service.write_heroine_identity(identity)
            await self.storage_service.write_heroine_voice(voice)

            # Step 3: Create bead record for heroine creation
            heroine_data = {"soul": soul, "identity": identity, "voice": voice}

            bead_content = {
                "action": "create_heroine",
                "description": description,
                "heroine_data": heroine_data,
            }

            # Create bead with create_heroine action (parent_id=None for root node)
            bead_id = await self.bead_service.create_bead(
                parent_id=None,
                content=bead_content,
                action="create_heroine",
                branch_name="main",  # Heroine creation happens on main branch
            )

            # Step 4: Store heroine data and return
            self._heroine_data = heroine_data
            return heroine_data

        except Exception as e:
            # Re-raise with context
            raise Exception(f"Failed to create heroine: {str(e)}") from e

    async def get_heroine(self) -> Optional[Dict[str, Any]]:
        """
        Retrieve the current heroine data from storage.

        For development, returns the heroine data stored in instance variable.
        In production, this would load from storage.

        Returns:
            Dictionary containing heroine data (soul, identity, voice) if found,
            None if no heroine exists
        """
        # For development, return the heroine data stored in instance variable
        # In a real implementation, we would check if heroine data exists in storage
        return self._heroine_data

#!/usr/bin/env python3
"""
Generate sample heroine and universe for testing.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('ANTHROPIC_API_KEY', 'dummy')  # Will fail without real key

from storage.file_system import save_heroine_data, save_npc_data, save_scene_data
from llm.service import LLMService
from database import init_db, get_session, Character

async def main():
    print("Initializing database...")
    await init_db()

    print("Generating sample heroine...")
    llm = LLMService()

    # Sample description
    description = """
    A 25-year-old librarian named Elara who lost her parents in a car accident at age 12.
    She has abandonment anxiety and uses perfectionism as a defense mechanism.
    She secretly dreams of being a rockstar but fears audience judgment.
    She prefers rainy window scenes, late-night cafes, and quiet libraries.
    """

    soul = await llm.parse_heroine(description)

    identity = {
        "name": "Elara",
        "age": 25,
        "appearance": "Long dark hair, sharp eyes, always wears a choker",
        "personality": "Introverted, meticulous, secretly passionate",
        "backstory": "Orphaned at 12, raised by strict aunt, found solace in books and music"
    }

    voice = {
        "speech_patterns": {
            "filler_words": ["um", "actually"],
            "sentence_ends": ["...", "."]
        },
        "vocabulary": {
            "level": "academic",
            "quirks": ["quotes literature"]
        },
        "emotional_tone": {
            "primary": "warm",
            "secondary": "guarded"
        }
    }

    heroine_id = await save_heroine_data(soul, identity, voice)
    print(f"Heroine saved: {heroine_id}")

    # Create NPCs (simplified without LLM)
    npcs = [
        {
            "role": "protector",
            "soul": {"key_traits": ["overprotective", "paternalistic"], "backstory": "Lost someone close, now overcompensates"},
            "identity": {"name": "Marcus", "age": 35, "appearance": "Broad shoulders, stern look", "personality": "Guardian", "backstory": "Former soldier turned bodyguard"},
            "voice": {"speech_patterns": {}, "vocabulary": {}, "emotional_tone": {}}
        },
        {
            "role": "competitor",
            "soul": {"key_traits": ["confident", "dismissive"], "backstory": "Always won, can't handle loss"},
            "identity": {"name": "Jax", "age": 28, "appearance": "Flashy clothes, smug smile", "personality": "Rivalrous", "backstory": "Child prodigy, never faced real failure"},
            "voice": {"speech_patterns": {}, "vocabulary": {}, "emotional_tone": {}}
        },
        {
            "role": "shadow",
            "soul": {"key_traits": ["mysterious", "manipulative"], "backstory": "Was rejected for being too intense"},
            "identity": {"name": "Vesper", "age": 30, "appearance": "Shadowy, sharp features", "personality": "Enigmatic", "backstory": "Lived in shadows, knows the heroine's secrets"},
            "voice": {"speech_patterns": {}, "vocabulary": {}, "emotional_tone": {}}
        }
    ]

    for npc in npcs:
        npc_id = f"npc_{npc['role']}_{heroine_id[:8]}"
        await save_npc_data(npc_id, npc)
        print(f"NPC saved: {npc_id}")

    # Create scene
    scene = {
        "name": "Rainy Library Window",
        "description": "Old library, rain on window, warm lamplight",
        "environment": {"location_type": "indoor", "time_of_day": "evening", "weather": "rainy"},
        "mood": "melancholic",
        "triggers": ["abandonment_fear", "comfort_seeking"],
        "npc_presences": [{"npc_role": "protector", "probability": 0.7}]
    }
    await save_scene_data(f"scene_{heroine_id[:8]}_0", scene)
    print("Scene saved")

    print("✅ Sample data generated!")

if __name__ == "__main__":
    asyncio.run(main())

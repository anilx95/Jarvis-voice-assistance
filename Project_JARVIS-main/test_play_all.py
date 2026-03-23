#!/usr/bin/env python
"""Comprehensive test of play/search functionality"""
import os
os.environ['GROQ_API_KEY'] = 'test'

from core.registry import SkillRegistry
from core.engine import JarvisEngine
import json

print("=" * 70)
print("TESTING PLAY FUNCTIONALITY FOR ALL TYPES OF CONTENT")
print("=" * 70)

registry = SkillRegistry()
registry.load_skills('skill')
engine = JarvisEngine(registry)

# Test cases covering all types of content
test_cases = [
    ("play nache nache", "Bollywood song"),
    ("play shape of you", "Popular song"),
    ("play avengers endgame trailer", "Movie trailer"),
    ("play python tutorial", "Educational content"),
    ("play despacito music video", "Music video"),
    ("find coldplay yellow", "Find + song"),
    ("search for titanic movie", "Search + movie"),
    ("play death note anime opening", "Anime opening"),
    ("play funny cat videos", "Funny videos"),
]

for query, description in test_cases:
    print(f"\n[{description}]")
    print(f"Command: {query}")
    try:
        result = engine.run_conversation(query)
        # Parse the JSON response
        if isinstance(result, str):
            if result.startswith('{'):
                result_dict = json.loads(result)
                message = result_dict.get('message', result)
            else:
                message = result
        else:
            message = result
        print(f"✓ {message}")
    except Exception as e:
        print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("TEST COMPLETE - All content types should open in YouTube!")
print("=" * 70)

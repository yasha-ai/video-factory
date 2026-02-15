#!/usr/bin/env python3
"""
Script Processor - Parse text and generate scenes with visual prompts

Converts raw text into structured scenes using Gemini API for intelligent segmentation.
"""

import os
import json
from dataclasses import dataclass, asdict
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

@dataclass
class Scene:
    """Represents a video scene"""
    id: str
    text: str          # Narration text
    visual_prompt: str # AI image generation prompt
    duration: float    # Estimated seconds


def process_script(text: str, style: str = "default") -> List[Scene]:
    """
    Process input text into structured scenes
    
    Args:
        text: Raw text input (prompt or script)
        style: Video style template (affects visual prompts)
    
    Returns:
        List of Scene objects
    """
    
    # Initialize Gemini API
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-latest')
    
    # System prompt for scene generation
    system_prompt = f"""You are a video script processor. Your task is to:

1. Analyze the input text
2. Split it into logical scenes (each 5-10 seconds)
3. For each scene:
   - Extract the narration text (what will be spoken)
   - Create a detailed visual prompt for AI image generation
   - Estimate duration in seconds

Style guidelines: {style}
- Modern, premium tech-focused aesthetic
- 1920x1080 resolution
- Clean, professional visuals

Return JSON array with this exact structure:
[
  {{
    "id": "scene-001",
    "text": "narration text here",
    "visual_prompt": "detailed image generation prompt",
    "duration": 5.5
  }}
]

Important:
- Each scene should be 5-10 seconds
- Visual prompts should be detailed and specific
- Include mood, lighting, composition in visual prompts
- Keep narration text concise and clear
"""

    user_prompt = f"""Process this text into video scenes:

{text}

Generate scenes with narration and visual prompts. Return ONLY valid JSON array, no other text."""

    print("🤖 Processing script with Gemini...")
    
    try:
        # Call Gemini API
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        response = model.generate_content(
            full_prompt,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 4000,
            }
        )
        
        # Extract response text
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        # Parse JSON
        scenes_data = json.loads(response_text)
        
        # Convert to Scene objects
        scenes = []
        for i, scene_dict in enumerate(scenes_data, 1):
            scene = Scene(
                id=scene_dict.get("id", f"scene-{i:03d}"),
                text=scene_dict["text"],
                visual_prompt=scene_dict["visual_prompt"],
                duration=float(scene_dict["duration"])
            )
            scenes.append(scene)
        
        print(f"✅ Generated {len(scenes)} scenes")
        return scenes
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON response: {e}")
        print(f"Response was: {response_text}")
        raise
    except Exception as e:
        print(f"❌ Error processing script: {e}")
        raise


def save_scenes(scenes: List[Scene], output_path: str):
    """Save scenes to JSON file"""
    scenes_dict = [asdict(scene) for scene in scenes]
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scenes_dict, f, indent=2, ensure_ascii=False)
    print(f"💾 Scenes saved to: {output_path}")


def load_scenes(input_path: str) -> List[Scene]:
    """Load scenes from JSON file"""
    with open(input_path, 'r', encoding='utf-8') as f:
        scenes_data = json.load(f)
    
    scenes = [Scene(**scene_dict) for scene_dict in scenes_data]
    print(f"📂 Loaded {len(scenes)} scenes from: {input_path}")
    return scenes


if __name__ == "__main__":
    # Test script processing
    test_prompt = """Create a 30-second video about AI breakthroughs in 2026. 
    Show futuristic tech visuals and explain how AI is changing the world."""
    
    scenes = process_script(test_prompt)
    
    # Print results
    print("\n📋 Generated Scenes:")
    print("=" * 80)
    for scene in scenes:
        print(f"\n{scene.id} ({scene.duration}s)")
        print(f"Text: {scene.text}")
        print(f"Visual: {scene.visual_prompt[:80]}...")
    print("=" * 80)

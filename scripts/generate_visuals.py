#!/usr/bin/env python3
"""
Visual Generator - Generate images for each scene using Gemini Image

Creates 1920x1080 images based on scene visual prompts.
"""

import os
import time
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from google import genai

from process_script import Scene

# Load environment variables
load_dotenv()


def generate_visuals(scenes: List[Scene], output_dir: str):
    """
    Generate images for all scenes using Gemini 2.5 Flash Image
    
    Args:
        scenes: List of Scene objects with visual prompts
        output_dir: Directory to save generated images
    """
    print(f"🎨 Generating visuals for {len(scenes)} scenes...")
    
    # Get API key
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment")
    
    # Initialize Gemini client
    client = genai.Client(api_key=api_key)
    
    # Create scenes directory
    scenes_dir = Path(output_dir) / "scenes"
    scenes_dir.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    
    for i, scene in enumerate(scenes, 1):
        print(f"\n[{i}/{len(scenes)}] {scene.id}")
        
        output_path = scenes_dir / f"{scene.id}.png"
        
        # Enhanced prompt with style guidelines
        enhanced_prompt = f"""Create a professional, high-quality image with these specifications:

Resolution: 1920x1080 (16:9 aspect ratio)
Style: Modern, premium, tech-focused, cinematic
Lighting: Professional, well-balanced
Composition: Centered, rule of thirds
Quality: Ultra high definition

Scene description:
{scene.visual_prompt}"""
        
        print(f"  📝 Prompt: {scene.visual_prompt[:80]}...")
        
        try:
            # Generate image using Gemini 2.5 Flash Image
            response = client.models.generate_content(
                model="gemini-2.5-flash-image",
                contents=[enhanced_prompt],
            )
            
            # Extract and save image from response
            image_saved = False
            for part in response.parts:
                if part.inline_data is not None:
                    # Convert to PIL Image and save
                    image = part.as_image()
                    image.save(str(output_path))
                    print(f"  ✅ Image saved: {output_path.name}")
                    success_count += 1
                    image_saved = True
                    break
            
            if not image_saved:
                print(f"  ⚠️  No image generated in response")
                
        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue
        
        # Rate limiting: wait between requests
        if i < len(scenes):
            time.sleep(2)
    
    print(f"\n✅ Generated {success_count}/{len(scenes)} images")
    
    if success_count == 0:
        raise Exception("Failed to generate any images")


if __name__ == "__main__":
    # Test image generation
    from process_script import Scene
    
    test_scene = Scene(
        id="test-001",
        text="Testing image generation",
        visual_prompt="Futuristic AI cityscape with neon lights, cyberpunk style, high tech",
        duration=5.0
    )
    
    generate_visuals([test_scene], "output/test")

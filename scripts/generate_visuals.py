#!/usr/bin/env python3
"""
Visual Generator - Generate images for each scene using Gemini 3 Pro Image

Creates 1920x1080 images based on scene visual prompts.
"""

import os
import time
from pathlib import Path
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

from process_script import Scene

# Load environment variables
load_dotenv()


def setup_gemini():
    """Initialize Gemini API"""
    api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY not found in environment")
    
    genai.configure(api_key=api_key)
    print("✅ Gemini API configured")


def generate_image(prompt: str, output_path: str, aspect_ratio: str = "16:9") -> bool:
    """
    Generate image using Gemini imagen model
    
    Args:
        prompt: Image generation prompt
        output_path: Where to save the image
        aspect_ratio: Image aspect ratio (16:9 for 1920x1080)
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Use Imagen 3 model for image generation
        model = genai.GenerativeModel('imagen-3.0-generate-001')
        
        # Enhanced prompt with style guidelines
        enhanced_prompt = f"""Premium quality, professional, modern aesthetic.
Resolution: 1920x1080
Style: Clean, tech-focused, cinematic
Lighting: Professional, well-balanced
Composition: Centered, rule of thirds

{prompt}"""
        
        print(f"  🎨 Generating image...")
        print(f"     Prompt: {prompt[:100]}...")
        
        # Generate image
        response = model.generate_images(
            prompt=enhanced_prompt,
            number_of_images=1,
            aspect_ratio=aspect_ratio,
            safety_settings={
                "block_none": True
            }
        )
        
        # Save the first image
        if response.images:
            image_data = response.images[0]
            
            # Save to file
            with open(output_path, 'wb') as f:
                f.write(image_data._image_bytes)
            
            print(f"  ✅ Image saved: {output_path}")
            return True
        else:
            print(f"  ⚠️ No image generated")
            return False
            
    except Exception as e:
        print(f"  ❌ Error generating image: {e}")
        # Create fallback placeholder
        create_placeholder(output_path, prompt)
        return False


def create_placeholder(output_path: str, text: str):
    """Create a placeholder image with text"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create black image with text
    img = Image.new('RGB', (1920, 1080), color='#1a1a2e')
    draw = ImageDraw.Draw(img)
    
    # Try to use a nice font, fallback to default
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
        small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
    except:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw placeholder text
    draw.text((960, 400), "Placeholder", fill='#ffffff', anchor='mm', font=font)
    
    # Draw scene description (wrapped)
    wrapped_text = '\n'.join([text[i:i+60] for i in range(0, len(text[:180]), 60)])
    draw.text((960, 600), wrapped_text, fill='#888888', anchor='mm', font=small_font)
    
    img.save(output_path)
    print(f"  📝 Placeholder created: {output_path}")


def generate_visuals(scenes: List[Scene], output_dir: str, delay: float = 2.0):
    """
    Generate images for all scenes
    
    Args:
        scenes: List of Scene objects
        output_dir: Directory to save images
        delay: Delay between API calls (seconds)
    """
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🎨 Generating visuals for {len(scenes)} scenes...")
    print(f"📁 Output directory: {output_dir}\n")
    
    # Setup Gemini
    setup_gemini()
    
    # Generate images for each scene
    success_count = 0
    for i, scene in enumerate(scenes, 1):
        print(f"\n[{i}/{len(scenes)}] Processing {scene.id}...")
        
        # Output path for this scene
        image_path = output_path / f"{scene.id}.png"
        
        # Skip if already exists
        if image_path.exists():
            print(f"  ⏭️  Image already exists, skipping")
            success_count += 1
            continue
        
        # Generate image
        success = generate_image(scene.visual_prompt, str(image_path))
        if success:
            success_count += 1
        
        # Rate limiting delay (except for last image)
        if i < len(scenes):
            print(f"  ⏳ Waiting {delay}s before next generation...")
            time.sleep(delay)
    
    print(f"\n✅ Generated {success_count}/{len(scenes)} images")
    return success_count == len(scenes)


if __name__ == "__main__":
    # Test visual generation
    from process_script import Scene
    
    test_scenes = [
        Scene(
            id="scene-001",
            text="Welcome to the future of AI",
            visual_prompt="Futuristic AI cityscape with holographic displays, neon lights, modern architecture, cyberpunk aesthetic, high-tech atmosphere",
            duration=5.0
        ),
        Scene(
            id="scene-002", 
            text="Technology is evolving rapidly",
            visual_prompt="Advanced robotics laboratory, AI researchers working with holographic interfaces, clean modern design, blue and white color scheme",
            duration=5.0
        )
    ]
    
    # Generate visuals
    generate_visuals(test_scenes, "test_output/scenes")

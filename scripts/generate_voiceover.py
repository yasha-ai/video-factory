#!/usr/bin/env python3
"""
Voiceover Generator - Generate TTS audio using Gemini TTS

Uses existing gemini-tts.sh script for voice generation.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv

from process_script import Scene

# Load environment variables
load_dotenv()


def generate_voiceover(
    scenes: List[Scene],
    output_path: str,
    voice: str = "fenrir",
    lang: str = "ru"
) -> Dict:
    """
    Generate voiceover audio from scenes
    
    Args:
        scenes: List of Scene objects
        output_path: Path for output audio file
        voice: Voice name (fenrir, kore, charon, aoede)
        lang: Language code (ru or en)
    
    Returns:
        Dict with audio_path and timing_data
    """
    
    print(f"\n🎙️  Generating voiceover...")
    print(f"   Voice: {voice} ({lang})")
    print(f"   Scenes: {len(scenes)}")
    
    # Combine all scene text
    full_text = " ".join(scene.text for scene in scenes)
    print(f"   Text length: {len(full_text)} chars\n")
    
    # Path to gemini-tts script
    tts_script = Path.home() / "clawd" / "scripts" / "gemini-tts.sh"
    
    if not tts_script.exists():
        raise FileNotFoundError(f"TTS script not found: {tts_script}")
    
    # Create output directory
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Model selection based on language
    model = "gemini-2.5-flash-preview-tts"
    
    # Call gemini-tts.sh
    cmd = [
        "bash",
        str(tts_script),
        full_text,
        str(output_file),
        model,
        voice
    ]
    
    print(f"🎬 Running TTS: {' '.join(cmd[:3])}...")
    
    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            env={**os.environ, "NO_PLAY": "1"}  # Don't play audio
        )
        
        if output_file.exists():
            print(f"✅ Voiceover generated: {output_file}")
            
            # Generate timing data (simple version based on scene durations)
            timing_data = generate_timing_markers(scenes)
            
            return {
                "audio_path": str(output_file),
                "timing_data": timing_data,
                "duration": sum(scene.duration for scene in scenes)
            }
        else:
            raise FileNotFoundError(f"Output file not created: {output_file}")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ TTS failed: {e}")
        print(f"   stdout: {e.stdout}")
        print(f"   stderr: {e.stderr}")
        raise


def generate_timing_markers(scenes: List[Scene]) -> List[Dict]:
    """
    Generate timing markers for subtitles
    
    Args:
        scenes: List of Scene objects
    
    Returns:
        List of timing markers with start, end, text
    """
    markers = []
    current_time = 0.0
    
    for scene in scenes:
        markers.append({
            "start": current_time,
            "end": current_time + scene.duration,
            "text": scene.text
        })
        current_time += scene.duration
    
    return markers


if __name__ == "__main__":
    # Test voiceover generation
    from process_script import Scene
    
    test_scenes = [
        Scene(
            id="scene-001",
            text="Добро пожаловать в будущее искусственного интеллекта",
            visual_prompt="...",
            duration=5.0
        ),
        Scene(
            id="scene-002",
            text="Технологии развиваются невероятно быстро",
            visual_prompt="...",
            duration=5.0
        )
    ]
    
    result = generate_voiceover(
        test_scenes,
        "test_output/voiceover.wav",
        voice="fenrir",
        lang="ru"
    )
    
    print(f"\n📊 Result:")
    print(f"   Audio: {result['audio_path']}")
    print(f"   Duration: {result['duration']}s")
    print(f"   Timing markers: {len(result['timing_data'])}")

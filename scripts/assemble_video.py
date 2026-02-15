#!/usr/bin/env python3
"""
Video Assembler - Combine images, audio, and subtitles into final video

Uses MoviePy to create the final MP4 video.
"""

import os
import json
from pathlib import Path
from typing import List, Dict

# MoviePy 2.x imports
from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)


def create_video_from_scenes(
    scenes_dir: str,
    timing_data: List[Dict],
    output_path: str,
    fps: int = 30,
    resolution: tuple = (1920, 1080),
    transition_duration: float = 0.5
):
    """
    Create video from scene images with timing
    
    Args:
        scenes_dir: Directory containing scene images
        timing_data: List of timing dictionaries from voiceover generation
        output_path: Output video file path
        fps: Frames per second
        resolution: Video resolution (width, height)
        transition_duration: Crossfade duration between scenes
    
    Returns:
        MoviePy VideoClip or None
    """
    
    try:
        print(f"\n🎬 Creating video from {len(timing_data)} scenes...")
        
        clips = []
        
        for i, timing in enumerate(timing_data):
            scene_id = timing['scene_id']
            duration = timing['duration']
            
            # Find image file
            image_path = Path(scenes_dir) / f"{scene_id}.png"
            
            if not image_path.exists():
                print(f"  ⚠️ Image not found: {image_path}")
                continue
            
            print(f"  [{i+1}/{len(timing_data)}] {scene_id} ({duration:.1f}s)")
            
            # Create image clip
            clip = ImageClip(str(image_path), duration=duration)
            
            # Resize to target resolution
            clip = clip.resized(resolution)
            
            clips.append(clip)
        
        if not clips:
            print("❌ No valid clips created")
            return None
        
        # Concatenate all clips
        print("\n🔗 Concatenating clips...")
        video = concatenate_videoclips(clips, method="compose")
        
        # Set FPS
        video = video.with_fps(fps)
        
        print(f"✅ Video created: {video.duration:.1f}s at {fps}fps")
        
        return video
        
    except Exception as e:
        print(f"❌ Error creating video: {e}")
        import traceback
        traceback.print_exc()
        return None


def add_audio_to_video(video, audio_path: str):
    """
    Add audio track to video
    
    Args:
        video: MoviePy VideoClip
        audio_path: Path to audio file
    
    Returns:
        Video with audio
    """
    
    try:
        print(f"\n🎵 Adding audio track...")
        print(f"   Audio: {audio_path}")
        
        # Load audio
        audio = AudioFileClip(audio_path)
        
        # Set audio on video
        video = video.with_audio(audio)
        
        print(f"✅ Audio added ({audio.duration:.1f}s)")
        
        return video
        
    except Exception as e:
        print(f"❌ Error adding audio: {e}")
        import traceback
        traceback.print_exc()
        return video


def export_video(video, output_path: str, codec: str = "libx264", audio_codec: str = "aac"):
    """
    Export final video to file
    
    Args:
        video: MoviePy VideoClip
        output_path: Output file path
        codec: Video codec (default: libx264 for H.264)
        audio_codec: Audio codec (default: aac)
    
    Returns:
        True if successful
    """
    
    try:
        print(f"\n📹 Exporting video...")
        print(f"   Output: {output_path}")
        print(f"   Codec: {codec}")
        print(f"   Audio: {audio_codec}")
        
        # Create parent directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Export video
        video.write_videofile(
            output_path,
            fps=video.fps,
            codec=codec,
            audio_codec=audio_codec,
            preset='medium',
            threads=4,
            logger='bar'
        )
        
        # Get file size
        file_size = Path(output_path).stat().st_size / (1024 * 1024)  # MB
        
        print(f"\n✅ Video exported successfully!")
        print(f"   File: {output_path}")
        print(f"   Size: {file_size:.1f} MB")
        print(f"   Duration: {video.duration:.1f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Error exporting video: {e}")
        import traceback
        traceback.print_exc()
        return False


def assemble_video(
    scenes_dir: str,
    audio_path: str,
    timing_json_path: str,
    output_path: str,
    fps: int = 30,
    resolution: tuple = (1920, 1080)
) -> bool:
    """
    Complete video assembly pipeline
    
    Args:
        scenes_dir: Directory with scene images
        audio_path: Path to voiceover audio file
        timing_json_path: Path to timing.json
        output_path: Output video file path
        fps: Video FPS
        resolution: Video resolution
    
    Returns:
        True if successful
    """
    
    print("🎬 Video Factory - Assembly Pipeline")
    print("=" * 80)
    
    # Load timing data
    print(f"\n📂 Loading timing data...")
    with open(timing_json_path, 'r') as f:
        timing_data = json.load(f)
    print(f"✅ Loaded {len(timing_data)} scene timings")
    
    # Create video from scenes
    video = create_video_from_scenes(
        scenes_dir=scenes_dir,
        timing_data=timing_data,
        output_path=output_path,
        fps=fps,
        resolution=resolution
    )
    
    if not video:
        return False
    
    # Add audio
    video = add_audio_to_video(video, audio_path)
    
    # Export final video
    success = export_video(video, output_path)
    
    # Cleanup
    video.close()
    
    if success:
        print("\n" + "=" * 80)
        print("🎉 Video assembly complete!")
        print("=" * 80)
    
    return success


if __name__ == "__main__":
    # Test video assembly
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python assemble_video.py <scenes_dir> <audio_file> <timing_json> [output_file]")
        sys.exit(1)
    
    scenes_dir = sys.argv[1]
    audio_file = sys.argv[2]
    timing_json = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) > 4 else "output.mp4"
    
    success = assemble_video(
        scenes_dir=scenes_dir,
        audio_path=audio_file,
        timing_json_path=timing_json,
        output_path=output_file
    )
    
    sys.exit(0 if success else 1)

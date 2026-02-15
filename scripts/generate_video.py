#!/usr/bin/env python3

"""
Video Factory - Main CLI Entry Point

Generates videos from text prompts using AI pipeline:
Script → Visuals → Voiceover → Assembly
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
import json

# Import our modules
from process_script import process_script, save_scenes
from generate_visuals import generate_visuals
from generate_voiceover import generate_voiceover
from assemble_video import assemble_video


def create_output_dir(prompt_text: str) -> Path:
    """Create timestamped output directory"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Create slug from prompt (first 30 chars, safe filename)
    slug = "".join(c if c.isalnum() or c in (' ', '-') else '' for c in prompt_text[:30])
    slug = slug.strip().replace(' ', '-').lower()
    
    dir_name = f"{timestamp}-{slug}"
    output_dir = Path("output") / dir_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def main():
    parser = argparse.ArgumentParser(
        description="Video Factory - AI-powered video generation",
        epilog="Example: python scripts/generate_video.py --prompt 'Create a video about AI'"
    )
    parser.add_argument("-p", "--prompt", type=str, help="Text prompt for video generation")
    parser.add_argument("-s", "--script", type=str, help="Path to script file")
    parser.add_argument("--voice", type=str, default="Fenrir", help="Voice name (default: Fenrir)")
    parser.add_argument("--lang", type=str, default="ru", choices=["ru", "en"], help="Language (default: ru)")
    parser.add_argument("--style", type=str, default="default", help="Video style template (default: default)")
    parser.add_argument("--no-subtitles", action="store_true", help="Disable subtitles")
    parser.add_argument("-o", "--output", type=str, help="Output file path (optional)")
    
    args = parser.parse_args()
    
    print("🎬 Video Factory - AI Video Generation")
    print("=" * 80)
    
    # Validate input
    if not args.prompt and not args.script:
        print("❌ Error: Either --prompt or --script is required")
        sys.exit(1)
    
    # Load script
    if args.script:
        print(f"📄 Loading script from: {args.script}")
        script_content = Path(args.script).read_text()
    else:
        print(f"💭 Using prompt: {args.prompt}")
        script_content = args.prompt
    
    print(f"\n📋 Configuration:")
    print(f"   Script length: {len(script_content)} chars")
    print(f"   Voice: {args.voice} ({args.lang})")
    print(f"   Style: {args.style}")
    print(f"   Subtitles: {'disabled' if args.no_subtitles else 'enabled'}")
    print("=" * 80)
    
    # Create output directory
    output_dir = create_output_dir(script_content)
    print(f"\n📁 Output directory: {output_dir}")
    
    try:
        # Step 1: Process script into scenes
        print("\n" + "=" * 80)
        print("STEP 1: Processing script → scenes")
        print("=" * 80)
        
        scenes = process_script(script_content, style=args.style)
        
        # Save scenes to JSON
        scenes_file = output_dir / "script.json"
        save_scenes(scenes, str(scenes_file))
        
        print(f"\n✅ Script processing complete!")
        print(f"   Generated: {len(scenes)} scenes")
        print(f"   Estimated duration: {sum(s.duration for s in scenes):.1f}s")
        
        # Step 2: Generate visuals
        print("\n" + "=" * 80)
        print("STEP 2: Generating visuals (AI images)")
        print("=" * 80)
        
        scenes_dir = output_dir / "scenes"
        success = generate_visuals(scenes, str(scenes_dir), delay=2.0)
        
        if not success:
            print("⚠️  Some images failed to generate (using placeholders)")
        
        # Step 3: Generate voiceover
        print("\n" + "=" * 80)
        print("STEP 3: Generating voiceover (TTS)")
        print("=" * 80)
        
        audio_dir = output_dir / "audio"
        voiceover_result = generate_voiceover(
            scenes=scenes,
            output_dir=str(audio_dir),
            voice=args.voice,
            lang=args.lang,
            combine=True
        )
        
        voiceover_file = audio_dir / "voiceover.wav"
        timing_file = audio_dir / "timing.json"
        
        print(f"\n✅ Voiceover complete!")
        print(f"   Audio: {voiceover_file}")
        print(f"   Duration: {voiceover_result['total_duration']:.1f}s")
        
        # Step 4: Assemble final video
        print("\n" + "=" * 80)
        print("STEP 4: Assembling final video")
        print("=" * 80)
        
        # Determine output path
        if args.output:
            final_video_path = Path(args.output)
        else:
            final_video_path = output_dir / "final-video.mp4"
        
        success = assemble_video(
            scenes_dir=str(scenes_dir),
            audio_path=str(voiceover_file),
            timing_json_path=str(timing_file),
            output_path=str(final_video_path),
            fps=30,
            resolution=(1920, 1080)
        )
        
        if not success:
            print("❌ Video assembly failed")
            return 1
        
        # Success!
        print("\n" + "=" * 80)
        print("🎉 VIDEO GENERATION COMPLETE!")
        print("=" * 80)
        print(f"\n📹 Final video: {final_video_path}")
        print(f"📁 Project files: {output_dir}")
        print(f"\n🎬 Ready for YouTube/Telegram!")
        
        # Print summary
        print("\n📊 Summary:")
        print(f"   Scenes: {len(scenes)}")
        print(f"   Duration: {voiceover_result['total_duration']:.1f}s")
        print(f"   Resolution: 1920x1080")
        print(f"   FPS: 30")
        print(f"   Audio: {args.voice} ({args.lang})")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Generation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

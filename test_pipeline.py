#!/usr/bin/env python3
"""
Quick pipeline test - checks that all modules import correctly
"""

import sys
sys.path.insert(0, 'scripts')

print("Testing imports...")

try:
    print("  ✓ process_script...", end='')
    from process_script import Scene, process_script
    print(" OK")
    
    print("  ✓ generate_visuals...", end='')
    from generate_visuals import generate_visuals
    print(" OK")
    
    print("  ✓ generate_voiceover...", end='')
    from generate_voiceover import generate_voiceover
    print(" OK")
    
    print("  ✓ assemble_video...", end='')
    from assemble_video import assemble_video
    print(" OK")
    
    print("\n✅ All modules imported successfully!")
    print("\nTest scene creation...")
    
    test_scene = Scene(
        id="test-001",
        text="This is a test",
        visual_prompt="A test image",
        duration=5.0
    )
    
    print(f"✅ Scene created: {test_scene.id}")
    print(f"   Text: {test_scene.text}")
    print(f"   Duration: {test_scene.duration}s")
    
    print("\n🎉 Pipeline test successful!")
    print("\nReady to generate videos with:")
    print("  python scripts/generate_video.py --prompt 'Your prompt here'")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

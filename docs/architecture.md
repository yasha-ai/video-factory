# Architecture

## System Overview

Video Factory follows a **modular pipeline architecture** where each step is independent and testable.

```
┌──────────────┐
│ User Input   │
│ (prompt/file)│
└──────┬───────┘
       │
       v
┌──────────────────────┐
│ Script Processor     │
│ - Parse input        │
│ - Split into scenes  │
│ - Generate prompts   │
└──────┬───────────────┘
       │
       v
┌──────────────────────┐     ┌──────────────────┐
│ Visual Generator     │────→│ Gemini 3 Pro     │
│ - Scene prompts      │     │ Image API        │
│ - Image generation   │     └──────────────────┘
└──────┬───────────────┘
       │
       v
┌──────────────────────┐     ┌──────────────────┐
│ Voiceover Generator  │────→│ Gemini TTS /     │
│ - Text to speech     │     │ Deepgram Aura    │
│ - Timing markers     │     └──────────────────┘
└──────┬───────────────┘
       │
       v
┌──────────────────────┐
│ Subtitle Generator   │
│ - Sync with audio    │
│ - Format .srt        │
└──────┬───────────────┘
       │
       v
┌──────────────────────┐     ┌──────────────────┐
│ Video Assembler      │────→│ FFmpeg           │
│ - Combine assets     │     │ - Encode video   │
│ - Apply effects      │     │ - Burn subtitles │
│ - Add music          │     │ - Export MP4     │
└──────┬───────────────┘     └──────────────────┘
       │
       v
┌──────────────┐
│ Final Video  │
│ (.mp4 file)  │
└──────────────┘
```

---

## Module Responsibilities

### 1. Script Processor (`scripts/process-script.ts`)
**Input:** Raw text (prompt or file)  
**Output:** Structured scene data

**Responsibilities:**
- Parse input text
- Identify natural scene breaks
- Generate visual prompts for each scene
- Estimate timing per scene
- Output: `Scene[]` array

**Data Structure:**
```typescript
interface Scene {
  id: string;
  text: string;          // Narration text
  visualPrompt: string;  // AI image generation prompt
  duration: number;      // Estimated seconds
}
```

---

### 2. Visual Generator (`scripts/generate-visuals.ts`)
**Input:** `Scene[]` with visual prompts  
**Output:** Image files per scene

**Responsibilities:**
- Call Gemini 3 Pro Image API
- Generate images matching scene prompts
- Apply consistent style/theme
- Save images with scene IDs
- Output: `{sceneId}.png` files

**AI Prompt Template:**
```
Style: Premium tech-focused, modern, clean
Resolution: 1920x1080
Subject: {visualPrompt}
Mood: {mood}
Color scheme: {colorScheme}
```

---

### 3. Voiceover Generator (`scripts/generate-voiceover.ts`)
**Input:** Script text  
**Output:** Audio file (.mp3 or .wav)

**Responsibilities:**
- Split text into TTS-friendly chunks
- Call Gemini TTS / Deepgram API
- Combine audio chunks
- Generate timing markers for subtitles
- Output: `voiceover.mp3` + `timing.json`

**Timing Data:**
```typescript
interface TimingMarker {
  start: number;   // seconds
  end: number;     // seconds
  text: string;    // spoken text
}
```

---

### 4. Subtitle Generator (`scripts/generate-subtitles.ts`)
**Input:** Script text + timing markers  
**Output:** Subtitle file (.srt)

**Responsibilities:**
- Format subtitles with timing
- Apply styling (position, font, color)
- Sync with voiceover markers
- Output: `subtitles.srt`

**SRT Format:**
```
1
00:00:00,000 --> 00:00:03,500
First subtitle line

2
00:00:03,500 --> 00:00:07,200
Second subtitle line
```

---

### 5. Video Assembler (`scripts/assemble-video.ts`)
**Input:** Images + audio + subtitles + music  
**Output:** Final video (.mp4)

**Responsibilities:**
- Combine images into video sequence
- Overlay audio tracks (voiceover + music)
- Burn subtitles into video
- Apply transitions between scenes
- Encode to MP4 (H.264 + AAC)
- Output: `final-video.mp4`

**FFmpeg Pipeline:**
```bash
# 1. Create video from images
ffmpeg -framerate 30 -pattern_type glob -i 'scene-*.png' -c:v libx264 video.mp4

# 2. Add voiceover
ffmpeg -i video.mp4 -i voiceover.mp3 -c copy -map 0:v:0 -map 1:a:0 video-audio.mp4

# 3. Burn subtitles
ffmpeg -i video-audio.mp4 -vf "subtitles=subtitles.srt" video-subs.mp4

# 4. Add background music
ffmpeg -i video-subs.mp4 -i music.mp3 -filter_complex "[1:a]volume=0.2[bg];[0:a][bg]amix=inputs=2" final.mp4
```

---

## Data Flow

### File System Organization

```
output/
└── {timestamp}-{slug}/
    ├── script.json           # Processed scenes
    ├── scenes/
    │   ├── scene-001.png
    │   ├── scene-002.png
    │   └── scene-003.png
    ├── voiceover.mp3         # Combined audio
    ├── timing.json           # Subtitle timing
    ├── subtitles.srt         # Formatted subtitles
    ├── music.mp3             # Background music
    └── final-video.mp4       # Output
```

### Processing Steps

1. **Input** → `script.json` (scenes with prompts)
2. **Visual Gen** → `scenes/*.png` (images per scene)
3. **TTS** → `voiceover.mp3` + `timing.json`
4. **Subtitles** → `subtitles.srt` (synced with timing)
5. **Assembly** → `final-video.mp4` (all combined)

---

## Configuration System

### Template Files (`templates/*.json`)

```json
{
  "name": "tech-news",
  "video": {
    "resolution": "1920x1080",
    "fps": 30,
    "codec": "libx264",
    "preset": "medium"
  },
  "visuals": {
    "style": "modern tech-focused premium",
    "colorScheme": "dark blue gradient with gold accents",
    "transitionType": "fade",
    "transitionDuration": 0.5
  },
  "audio": {
    "voice": "fenrir",
    "musicVolume": 0.2,
    "voiceVolume": 1.0
  },
  "subtitles": {
    "font": "Montserrat",
    "fontSize": 48,
    "color": "#FFD700",
    "position": "bottom-center",
    "outline": true
  }
}
```

---

## Error Handling

### Retry Strategy
- API calls: 3 retries with exponential backoff
- File operations: Single retry with 1s delay
- FFmpeg errors: Detailed logging + graceful exit

### Validation
- Check API keys before starting
- Validate input script format
- Verify FFmpeg installation
- Check disk space for output

---

## Performance Considerations

### Parallel Processing
- Generate all scene images concurrently (Promise.all)
- TTS can run in parallel with image generation
- Subtitle generation waits for timing data

### Caching
- Cache generated images (reuse if prompt matches)
- Cache TTS output (reuse if text matches)
- Store intermediate files for debugging

---

## Future Enhancements

- **Real-time preview** during generation
- **Web UI** for non-CLI users
- **Cloud rendering** for faster processing
- **Video editing** capabilities (trim, split, merge)
- **AI script enhancement** (improve prompts automatically)

---

*Last updated: 2026-02-15*

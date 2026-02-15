# Video Factory - Technical Specification

## Overview

**Video Factory** — AI-powered video generation pipeline for automated content creation.

**Goal:** Transform text prompts into publication-ready videos with AI-generated visuals, voiceover, subtitles, and music.

**Target use case:** Educational content, tech news, tutorials, explainers.

---

## Core Features (MVP)

### 1. Input → Output
- **Input:** Text prompt or script
- **Output:** MP4 video file ready for YouTube/Telegram

### 2. Generation Pipeline
1. **Script Processing**
   - Parse input text
   - Split into scenes/segments
   - Generate visual prompts per scene

2. **Visual Generation**
   - Generate images per scene (Gemini 3 Pro Image / Stable Diffusion)
   - Optional: B-roll stock footage integration

3. **Voiceover**
   - Text-to-Speech (Gemini TTS / Deepgram Aura)
   - Russian + English support
   - Multiple voice options

4. **Subtitles**
   - Auto-generate from script
   - Timing sync with voiceover
   - Styled subtitles (premium look)

5. **Assembly**
   - Combine: images + voiceover + subtitles + background music
   - Transitions between scenes
   - Export as MP4

### 3. Quality Standards
- **Resolution:** 1920x1080 (Full HD)
- **Frame rate:** 30fps
- **Audio:** 48kHz stereo
- **Subtitles:** Burned-in or separate .srt
- **Style:** Premium, modern, tech-focused aesthetic

---

## Tech Stack (Proposed)

### Video Processing
- **FFmpeg** — video assembly, encoding, effects
- **Remotion** (optional) — programmatic video creation with React
- **MoviePy** (Python alternative)

### AI Services
- **Visuals:** Gemini 3 Pro Image, Stable Diffusion XL, Midjourney API
- **TTS:** Gemini TTS (Russian), Deepgram Aura (English)
- **Script enhancement:** Claude Opus 4.6 / GPT-5.3

### Storage & Assets
- **Local:** `~/clawd/video-factory/output/`
- **Cloud:** (future) S3 / Cloudflare R2
- **Stock footage:** Pexels API, Pixabay API

---

## Project Structure

```
video-factory/
├── SPEC.md                    # This file
├── README.md                  # User-facing docs
├── package.json               # Dependencies
├── scripts/
│   ├── generate-video.ts      # Main CLI entry point
│   ├── process-script.ts      # Script → scenes
│   ├── generate-visuals.ts    # Scenes → images
│   ├── generate-voiceover.ts  # Script → audio
│   ├── generate-subtitles.ts  # Script → .srt
│   └── assemble-video.ts      # Combine all → MP4
├── templates/
│   ├── default.json           # Default video template
│   └── tech-news.json         # Tech news style
├── assets/
│   ├── fonts/                 # Subtitle fonts
│   ├── music/                 # Background music tracks
│   └── transitions/           # Video transitions
├── output/                    # Generated videos
└── docs/
    ├── architecture.md
    ├── api-reference.md
    ├── user-flows.md
    └── testing.md
```

---

## User Flow (MVP)

### CLI Usage

```bash
# Basic generation
npm run generate -- --prompt "Create a 2-minute video about Claude Opus 4.6 release"

# With custom script file
npm run generate -- --script ./scripts/claude-opus-4.6.txt --voice fenrir --lang ru

# Advanced options
npm run generate -- \
  --script ./my-script.txt \
  --voice fenrir \
  --lang ru \
  --style tech-news \
  --music ambient \
  --subtitles on \
  --output ./my-video.mp4
```

### Output
- `output/{timestamp}-{slug}.mp4` — final video
- `output/{timestamp}-{slug}/` — intermediate files (images, audio, .srt)

---

## Implementation Phases

### Phase 1: Foundation (Week 1)
- [ ] Project setup (TypeScript, FFmpeg, dependencies)
- [ ] Script parser (text → scenes)
- [ ] Image generation (Gemini API integration)
- [ ] TTS integration (Gemini TTS)
- [ ] Basic video assembly (images + audio → MP4)

### Phase 2: Enhancement (Week 2)
- [ ] Subtitle generation & sync
- [ ] Background music integration
- [ ] Transitions between scenes
- [ ] Template system (customizable styles)

### Phase 3: Polish (Week 3)
- [ ] Multiple voice support
- [ ] Stock footage integration
- [ ] Advanced effects (zoom, pan, fade)
- [ ] Batch processing

### Phase 4: Production (Week 4)
- [ ] CI/CD pipeline
- [ ] Automated testing
- [ ] Documentation
- [ ] Public release

---

## Configuration

### Environment Variables
```env
# AI Services
GOOGLE_GEMINI_API_KEY=<key>          # Gemini TTS + Image
DEEPGRAM_API_KEY=<key>               # Alternative TTS
OPENAI_API_KEY=<key>                 # Script enhancement (optional)

# Assets
PEXELS_API_KEY=<key>                 # Stock footage (optional)
MUSIC_LIBRARY_PATH=/path/to/music   # Background music

# Output
OUTPUT_DIR=./output
VIDEO_QUALITY=high                   # low | medium | high
```

---

## Design Principles

1. **Spec-driven development** — This document is the single source of truth
2. **Modular architecture** — Each step is independent, testable
3. **CLI-first** — Command-line interface, scriptable, automatable
4. **Quality over speed** — Premium output, worth the wait
5. **Extensible** — Easy to add new voices, styles, effects

---

## Success Metrics

**MVP Success:**
- Generate 2-minute video in < 5 minutes
- Zero manual editing required
- Publication-ready quality
- Russian + English support

**Future Goals:**
- Support 10+ languages
- Real-time video generation (< 1 minute)
- Web UI for non-technical users
- Integration with YouTube/Telegram auto-publishing

---

## Questions & Decisions

### Open Questions
- [ ] Remotion vs FFmpeg vs MoviePy?
- [ ] Burn subtitles or separate .srt?
- [ ] Voice cloning support? (ElevenLabs)
- [ ] Video hosting strategy?

### Decisions Made
- ✅ TypeScript for scripting (consistency with other projects)
- ✅ Gemini for visuals + TTS (already integrated)
- ✅ CLI-first approach (automation-friendly)
- ✅ Local-first storage (cloud later)

---

## Related Projects
- **yasha-learn-code** — Educational platform (potential content source)
- **yasha-dashboard** — Task management (tracks video production tasks)
- **OpenClaw** — Automation framework (runs generation jobs)

---

**Status:** 📝 Specification phase  
**Next Step:** Create `docs/architecture.md` and start Phase 1 implementation

---

*Last updated: 2026-02-15*

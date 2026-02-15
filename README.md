# 🎬 Video Factory

**AI-powered video generation pipeline** for automated content creation.

Transform text prompts into publication-ready videos with AI-generated visuals, voiceover, subtitles, and music.

---

## Features

- 🎨 **AI-Generated Visuals** — Gemini 3 Pro Image / Stable Diffusion
- 🎙️ **Natural Voiceover** — Gemini TTS (Russian) + Deepgram (English)
- 📝 **Auto Subtitles** — Synchronized, styled, burned-in
- 🎵 **Background Music** — Ambient tracks, auto-ducking
- ✨ **Premium Quality** — Full HD, 30fps, publication-ready

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/yasha-ai/video-factory.git
cd video-factory

# Install dependencies
npm install

# Generate your first video
npm run generate -- --prompt "Create a 2-minute video about AI breakthroughs in 2026"
```

---

## Usage

### Basic Generation
```bash
npm run generate -- --prompt "Your video topic here"
```

### Custom Script
```bash
npm run generate -- --script ./my-script.txt --voice fenrir --lang ru
```

### Advanced Options
```bash
npm run generate -- \
  --script ./script.txt \
  --voice fenrir \
  --lang ru \
  --style tech-news \
  --music ambient \
  --subtitles on \
  --output ./my-video.mp4
```

---

## Configuration

Copy `.env.example` to `.env.local`:

```env
GOOGLE_GEMINI_API_KEY=your_key_here
DEEPGRAM_API_KEY=your_key_here
OUTPUT_DIR=./output
VIDEO_QUALITY=high
```

---

## Documentation

- 📋 [Technical Specification](SPEC.md)
- 🏗️ [Architecture](docs/architecture.md)
- 📚 [API Reference](docs/api-reference.md)
- 🧪 [Testing Guide](docs/testing.md)

---

## Roadmap

**Phase 1:** Foundation (Script processing, image generation, TTS, basic assembly)  
**Phase 2:** Enhancement (Subtitles, music, transitions, templates)  
**Phase 3:** Polish (Multi-voice, stock footage, advanced effects)  
**Phase 4:** Production (CI/CD, testing, public release)

---

## Tech Stack

- **TypeScript** — Scripting & orchestration
- **FFmpeg** — Video processing & encoding
- **Gemini API** — AI visuals & TTS
- **Remotion** (optional) — Programmatic video creation

---

## Contributing

This project follows **spec-driven development**:
1. Read [SPEC.md](SPEC.md) first
2. Propose changes via issues/PRs
3. Update SPEC.md before implementing

---

## License

MIT © Yasha AI

---

**Created by:** [Yasha](https://github.com/yasha-ai)  
**Status:** 🚧 In Development

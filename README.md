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
pip install -r requirements.txt

# Generate your first video
python scripts/generate_video.py --prompt "Create a 2-minute video about AI breakthroughs in 2026"
```

---

## Usage

### Basic Generation
```bash
python scripts/generate_video.py --prompt "Your video topic here"
```

### Custom Script
```bash
python scripts/generate_video.py --script ./my-script.txt --voice fenrir --lang ru
```

### Advanced Options
```bash
python scripts/generate_video.py \
  --script ./script.txt \
  --voice fenrir \
  --lang ru \
  --style tech-news \
  --music ambient \
  --subtitles \
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

- **Python 3.11+** — Scripting & orchestration
- **FFmpeg + MoviePy** — Video processing & encoding
- **Gemini API** — AI visuals & TTS
- **Deepgram** — Alternative TTS for English

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

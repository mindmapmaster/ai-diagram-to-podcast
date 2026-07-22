# AI Diagram to Podcast Generator

> What if diagrams could talk?

Transform mind maps, flowcharts, and structured visual content into engaging AI-generated dual-host podcast episodes.

AI Diagram to Podcast Generator is an experimental AI workflow exploring a new way to consume visual knowledge.

Starting from a diagram image, AI understands the structure, generates a natural conversational script, and synthesizes it into a podcast using neural text-to-speech.

This repository demonstrates the complete workflow and includes reproducible examples for both **mind maps** and **flowcharts**.

---

## Workflow

```text
Mind Map / Flowchart
          │
          ▼
AI Structure Understanding
          │
          ▼
Podcast Script Generation
          │
          ▼
Neural TTS (Dual Hosts)
          │
          ▼
Podcast Audio
```

---

# Features

## Supported Diagram Types

| Input Type | Structure Understanding | Script Generation | Voice Synthesis | Status |
|------------|-------------------------|-------------------|-----------------|--------|
| Mind Map | Central topic + hierarchical branches | Knowledge-sharing dual-host conversation | Edge TTS neural voice | ✅ Verified |
| Flowchart | Nodes + decisions + loops + merges | Sequential storytelling conversation | Edge TTS neural voice | ✅ Verified |

---

## Processing Pipeline

```
Diagram Image (Mind Map / Flowchart)
              │
              ▼
① AI Structure Understanding
   - Identify nodes and relationships
   - Understand hierarchy and logical flow
   - Extract structured information
              │
              ▼
② Podcast Script Generation
   - Convert structure into dialogue format
   - Add scenarios and examples
   - Create natural host interactions
              │
              ▼
③ Dual-host Voice Generation
   - Host A: zh-CN-YunxiNeural (Male)
   - Host B: zh-CN-XiaoxiaoNeural (Female)
   - Natural pauses between sentences
   - Export MP3 audio
```

---

# Technical Overview

## Tech Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| Diagram Understanding | Multimodal AI | Understand diagram images and logical structures |
| Script Generation | Large Language Model | Convert structured information into conversational scripts |
| Voice Synthesis | [edge-tts](https://github.com/rany2/edge-tts) | Microsoft Edge neural TTS with high-quality voices |
| Audio Processing | ffmpeg + Python wave | Audio processing, merging, and export |
| FFmpeg Distribution | [imageio-ffmpeg](https://github.com/imageio/imageio-ffmpeg) | Provides FFmpeg binaries without system installation |

---

## Voice Configuration

| Role | Voice | Gender | Speed |
|------|-------|--------|-------|
| Host A | zh-CN-YunxiNeural | Male | -3% |
| Host B | zh-CN-XiaoxiaoNeural | Female | -1% |

---

## Why edge-tts?

| Solution | Quality | Cost | Description |
|----------|---------|------|-------------|
| **edge-tts** | Good | Free | Neural voice synthesis used in this project |
| ElevenLabs | Excellent | Paid API | Higher-quality voice generation |
| pyttsx3 / SAPI5 | Basic | Free | Early prototype, no longer used |

---

# Getting Started

## Installation

```bash
git clone https://github.com/your-username/ai-diagram-to-podcast.git

cd ai-diagram-to-podcast

pip install -r requirements.txt
```

Python 3.10+ is recommended.

---

## Generate Podcast Audio

The core generator accepts Markdown scripts as input.

```bash
cd src

python podcast_generator.py \
-i ../examples/mindmap-demo/mindmap-demo-script.md \
-o output.mp3
```

Custom output:

```bash
python podcast_generator.py \
-i your-script.md \
-o your-podcast.mp3 \
--cache ./my-cache
```

---

## Script Format

The generator supports Markdown dialogue format:

```markdown
# Topic

## Section 1

**Host A:** Welcome to today's topic.

**Host B:** Let's explore this idea together.
```

Supported formats:

```
**Host A:**
**Host B:**

or

**A:**
**B:**
```

---

# AI Script Generation

The podcast scripts in this demo are generated from diagram images.

The workflow:

1. Analyze diagram structure and content
2. Convert visual information into conversational dialogue
3. Preserve the original logic while adding examples and interactions

> The multimodal image understanding and script generation step relies on AI models. This repository focuses on the automated workflow from generated scripts to final podcast audio.

---

# Demo Examples

Two complete examples are included:

- Mind Map → Podcast
- Flowchart → Podcast

Each demo contains:
- Generated script
- Final podcast audio
- Additional analysis files

---

## Example 1: Mind Map → Podcast

Input:

A yearly summary mind map containing:

- First-half review
- Key projects
- Lessons learned
- Second-half planning

Output:

- Script: `examples/mindmap-demo/mindmap-demo-script.md`
- Audio: `examples/mindmap-demo/mindmap-demo.mp3`

Duration:

Approximately 5 minutes.

---

## Example 2: Flowchart → Podcast

Input:

A library management system flowchart containing:

- Decision branches
- Loops
- Process transitions
- Merge points

Output:

- Script: `examples/flowchart-demo/flowchart-demo-script.md`
- Audio: `examples/flowchart-demo/flowchart-demo.mp3`
- Structure analysis: `examples/flowchart-demo/structure-analysis.md`

Duration:

Approximately 5.5 minutes.

---

# Mind Map vs Flowchart

Different diagram types require different transformation strategies.

| Type | Characteristics | Podcast Adaptation |
|------|-----------------|-------------------|
| Mind Map | Tree structure, hierarchical information | Parallel explanation and knowledge sharing |
| Flowchart | Directed graph, logical decisions | Sequential storytelling with transitions |

See:

`docs/flowchart-vs-mindmap.md`

---

# Project Structure

```
ai-diagram-to-podcast/

├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore

├── src/
│   └── podcast_generator.py

├── examples/
│   ├── mindmap-demo/
│   │   ├── README.md
│   │   ├── mindmap-demo-script.md
│   │   └── mindmap-demo.mp3
│   │
│   └── flowchart-demo/
│       ├── README.md
│       ├── flowchart-demo-script.md
│       ├── flowchart-demo.mp3
│       └── structure-analysis.md

└── docs/
    └── flowchart-vs-mindmap.md
```

---

# Generator Features

`src/podcast_generator.py` provides a reusable dual-host podcast generator.

Features:

- Multiple dialogue formats:
  - `**Host A:**`
  - `**Host B:**`
  - `**A:**`
  - `**B:**`

- Sentence-level caching
- Resume after interruption
- Async generation with concurrency control
- Automatic retry mechanism
- No system FFmpeg installation required
- Natural conversation pauses

---

# Future Extensions

| Feature | Description |
|---------|-------------|
| More diagram types | Architecture diagrams, UML, sequence diagrams, organization charts |
| English voice support | Generate bilingual podcasts |
| More voice options | Custom speaker configurations |
| Script templates | Tutorial, interview, and analysis formats |
| Emotion control | SSML-based expressive speech |
| ElevenLabs integration | Higher-quality voice generation |
| Podcast publishing automation | RSS-based publishing workflow |
| Blog generation | Convert diagrams into articles |
| Video generation | Create narrated visual content |

---

# Demo Assets

The diagrams used in the demo examples were created with **ProcessOn**, an online diagramming and knowledge visualization tool.

ProcessOn is only used as the source of demo diagrams. The workflow demonstrated in this repository is tool-agnostic and can be applied to diagrams created with other platforms.

---

# Limitations

- Diagram image understanding depends on multimodal AI models and is not included in this repository.
- edge-tts requires an internet connection because voice synthesis uses Microsoft's online service.
- edge-tts provides high-quality neural voices but may not reach premium commercial solutions such as ElevenLabs.
- Currently supports Chinese voice generation only.

---

# Acknowledgements

This project explores how AI can transform structured visual knowledge into new forms of content consumption.

Thanks to the open-source community and projects including:

- edge-tts
- imageio-ffmpeg

---

# License

MIT License
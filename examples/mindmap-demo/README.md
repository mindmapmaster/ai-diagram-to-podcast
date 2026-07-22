# Demo 1: Mind Map → Podcast

## Input

A "Mid-Year Summary" mind map created with ProcessOn, containing four major sections:

- H1 Work Review
- Key Projects & Achievements
- Lessons Learned
- H2 Plan

## Source Diagram

The original mind map was created with ProcessOn:

https://www.processon.com/view/629eefa31e08532ab7963343

## Processing Pipeline

1. **AI Structure Understanding**  
   Reads the mind map image and identifies the central topic, four main branches, and related sub-nodes.

2. **Podcast Script Generation**  
   Converts the tree structure into a knowledge-sharing style dual-host conversation, using examples and discussions instead of simply reading nodes.

3. **Neural Voice Synthesis**  
   Generates the final podcast audio using edge-tts neural voices:
   - Host A: zh-CN-YunxiNeural
   - Host B: zh-CN-XiaoxiaoNeural

## Output

| File | Description |
|------|-------------|
| `mindmap-demo-script.md` | Dual-host podcast script (17 Host A lines + 15 Host B lines) |
| `mindmap-demo.mp3` | Generated podcast audio, approximately 5 minutes, 192kbps MP3 |

## Audio Configuration

- Host A: zh-CN-YunxiNeural, speed -3%
- Host B: zh-CN-XiaoxiaoNeural, speed -1%
- Sentence pause: 0.38 seconds
- Paragraph pause: 0.65 seconds

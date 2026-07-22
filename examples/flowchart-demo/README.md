# Demo 2: Flowchart → Podcast

## Input

A "Library Management System" business flowchart created with ProcessOn, containing:

- Login authentication (with retry loop)
- Main function selection (three parallel branches)
- Borrowing confirmation (decision branch + rollback path)
- Return and overdue handling (path merging)

## Source Diagram

The original flowchart was created with ProcessOn:

https://www.processon.com/view/6a5f1878e240cc3a7dacbd4b

## Processing Pipeline

1. **AI Structure Understanding**  
   Reads the flowchart image and identifies 15+ nodes, 2 decision points, 2 loop/merge structures, and 3 parallel branches.

2. **Podcast Script Generation**  
   Converts the directed graph structure into a linear dual-host conversation, adding questions at decision points and explaining branches and rollback paths.

3. **Neural Voice Synthesis**  
   Generates the final podcast audio using edge-tts neural voices:
   - Host A: zh-CN-YunxiNeural
   - Host B: zh-CN-XiaoxiaoNeural

## Output

| File | Description |
|------|-------------|
| `flowchart-demo-script.md` | Dual-host podcast script (22 Host A lines + 21 Host B lines) |
| `flowchart-demo.mp3` | Generated podcast audio, approximately 5.5 minutes, 192kbps MP3 |
| `structure-analysis.md` | AI structure analysis result (nodes, connections, decision branches, loops, and merges) |

## Audio Configuration

- Host A: zh-CN-YunxiNeural, speed -3%
- Host B: zh-CN-XiaoxiaoNeural, speed -1%
- Sentence pause: 0.38 seconds
- Paragraph pause: 0.65 seconds

## Key Difference from Mind Map Demo

Compared with mind maps, flowcharts require stronger structural reasoning and narrative transformation.

Flowcharts are directed graphs with sequences, decisions, loops, and merges, while mind maps are hierarchical structures that can be expanded in parallel.

See [docs/flowchart-vs-mindmap.md](../../docs/flowchart-vs-mindmap.md).

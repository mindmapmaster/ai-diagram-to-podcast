# Demo 2: 流程图 → 播客

## 输入

一张「图书借阅管理系统业务流程图」，包含：
- 登录验证（含循环重试）
- 主功能选择（3 条并行分支）
- 借阅确认（判断分支 + 回退）
- 归还与逾期处理（双路径合并）

## 处理流程

1. **AI 结构识别**：读取流程图图片，识别 15+ 节点、2 个判断菱形、2 处循环/合并、3 条并行分支
2. **脚本生成**：将有向图结构转化为线性推进的双主播对话，在判断点插入提问，强调分支和回退路径
3. **语音合成**：edge-tts 神经网络语音，男声 YunxiNeural + 女声 XiaoxiaoNeural

## 产物

| 文件 | 说明 |
|------|------|
| `flowchart-demo-script.md` | 双主播播客脚本（22 句 Host A + 21 句 Host B） |
| `flowchart-demo.mp3` | 最终音频，约 5.5 分钟，192kbps MP3 |
| `structure-analysis.md` | AI 结构识别结果（节点、连接、判断分支、循环、合并） |

## 音频参数

- 男声 (Host A)：zh-CN-YunxiNeural，语速 -3%
- 女声 (Host B)：zh-CN-XiaoxiaoNeural，语速 -1%
- 句间停顿：0.38 秒
- 段落停顿：0.65 秒

## 与思维导图 Demo 的关键差异

流程图相比思维导图，对"结构理解"和"叙事转换"要求更高——
详见 [docs/flowchart-vs-mindmap.md](../../docs/flowchart-vs-mindmap.md)。

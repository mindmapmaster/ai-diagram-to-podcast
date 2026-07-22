# Demo 1: 思维导图 → 播客

## 输入

一张「年中总结」思维导图（使用 ProcessOn 思维导图模板创建），包含 4 大模块：
- 上半年工作回顾
- 重点项目与成果
- 经验总结
- 下半年计划

## 处理流程

1. **AI 结构识别**：读取思维导图图片，识别中心主题、4 个一级分支及其子节点
2. **脚本生成**：将树状结构转化为知识分享型双主播对话，用案例引入每个模块
3. **语音合成**：edge-tts 神经网络语音，男声 YunxiNeural + 女声 XiaoxiaoNeural

## 产物

| 文件 | 说明 |
|------|------|
| `mindmap-demo-script.md` | 双主播播客脚本（17 句 Host A + 15 句 Host B） |
| `mindmap-demo.mp3` | 最终音频，约 5 分钟，192kbps MP3 |

## 音频参数

- 男声 (Host A)：zh-CN-YunxiNeural，语速 -3%
- 女声 (Host B)：zh-CN-XiaoxiaoNeural，语速 -1%
- 句间停顿：0.38 秒
- 段落停顿：0.65 秒

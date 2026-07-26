# Build Video Semantic Graph Skill

一个面向 Codex/智能体的开源技能：把本地短视频素材转化为**带时间戳的视频语义搜索图谱**。

它可以完成素材盘点、时间戳故事板抽取、多模态模型结构化理解、入口视频分段、结果视频标注、候选召回与重排、图谱校验、人工复核表导出，以及通过备份后安全写入正式 JSON。

> 本技能来源于 CrossFrame「看到即搜索，搜索即剧情」视觉搜索项目的真实生产流程。

## 能生成什么

- 带时间范围的入口语义片段；
- 人物、对象、动作、场景和事件状态等结构化语义；
- 从暂停时刻对应片段指向相关结果视频的推荐关系；
- 模型调用与数据质量报告；
- 人工复核工作簿；
- 可直接供 H5/API 使用的 `videos.json`、`segments.json`、`relations.json`。

## 核心技术路线

```text
本地视频
  → 素材盘点与编解码检查
  → 带时间戳故事板抽取
  → 多模态模型理解
  → 入口视频语义分段
  → 结果视频结构化标注
  → 候选召回
  → 模型重排与多样性控制
  → 图谱校验
  → 人工复核工作簿
  → 备份后显式写入正式数据
```

## 如实说明当前实现

当前代码采用：

1. 从本地视频抽取带时间戳的故事板；
2. 通过 OpenAI-compatible 接口调用支持视觉输入的多模态模型；
3. 使用严格结构化输出完成入口视频分段与结果视频标注；
4. 先进行文本/语义候选召回，再使用模型重排；
5. 对时间边界、引用关系、推荐多样性、版权状态和媒体文件进行图谱级校验；
6. 所有正式写入必须经过人工复核，并先创建时间戳备份。

本项目不虚构“已经使用向量数据库”。在大规模视频池中，可以进一步接入多模态向量模型作为第一阶段召回层，同时继续使用本技能的片段数据结构、验证契约和重排流程。

## CrossFrame 参考规模

参考运行已完成：

- 33 条本地视频；
- 15 条入口视频、18 条结果视频；
- 100 个时间语义片段；
- 可支持多轮探索的推荐图谱。

本仓库不包含视频素材、密钥、私有模型响应和项目专属正式 JSON。

## 开源分发方式

完整可执行源码位于：

```text
dist/build-video-semantic-graph.skill
```

`.skill` 是兼容 ZIP 的源码包，内部包含 `SKILL.md`、`agents/`、`references/` 和完整 `scripts/`。代码未混淆、未编译。

SHA-256：

```text
45defd220e6ebfae001fefffe991137227561ff7bed27bfd996a1174bd3566f8
```

使用 Python 解压：

```bash
python tools/unpack_skill.py --output unpacked
```

也可以复制或重命名为 `.zip` 后使用任意解压工具。

## 运行环境

- Python 3.10+
- 系统 `PATH` 中可用的 `ffmpeg` 与 `ffprobe`
- 分析阶段需要支持视觉输入的多模态模型接口

解压并安装依赖：

```bash
python tools/unpack_skill.py --output unpacked
python -m pip install -r unpacked/scripts/requirements.txt
```

## 目标项目目录

```text
project/
├── raw/入口/                 # 或 raw/entry/
├── raw/结果/                 # 或 raw/result/
├── backend/app/data/
├── frontend/public/media/videos/
├── data/generated/
├── reports/autolabel/
└── work/
```

`raw/` 下的源视频始终视为只读文件。

## 模型配置

仅通过进程环境变量配置：

```bash
export CROSSFRAME_VLM_PROVIDER=volcengine_ark
export CROSSFRAME_VLM_MODEL=<支持视觉输入的模型 ID>
export CROSSFRAME_VLM_API_KEY=<密钥>
export CROSSFRAME_VLM_BASE_URL=<OpenAI-compatible API 地址>
```

不要提交真实密钥、包含密钥的 `.env`、模型请求/响应缓存、抽取音频或转写文本。

## 快速开始

先运行 dry run：

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --dry-run
```

运行完整流程：

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode all
```

校验每个源片段是否具有 1 个主结果和 2 个备选结果：

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results
```

复核后写入正式数据：

```bash
python unpacked/scripts/run_pipeline.py \
  --project-root /path/to/project \
  --mode validate \
  --require-three-results \
  --apply
```

写入前会自动创建时间戳备份。

## 安全原则

- 不修改 `raw/` 下的源素材；
- 不根据文件名伪造视觉标签；
- 文件名只能作为弱监督；
- 缺少模型密钥且存在未分析视频时安全停止；
- 公共仓库不保存模型证据、缓存、音频或私有转写；
- 时间错误、引用缺失、重复 ID、媒体缺失或版权状态不可用时禁止写入；
- 低置信度与视觉冲突必须人工复核。

## 自检

```bash
python unpacked/scripts/self_check.py
```

正常结果：

```text
Skill self-check: PASS
```

## 开源协议

MIT License，详见 [LICENSE](LICENSE)。

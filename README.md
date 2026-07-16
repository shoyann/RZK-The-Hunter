# Awesome OSINT Operator Skill v1.1.0

这不是把 `awesome-osint` 的链接机械地塞进一个提示词，而是把它升级成一套**可执行的 OSINT 调研系统**：任务分流、工具检索、风险控制、证据台账、交叉验证、置信度评级和报告模板都已经打包。

## 它比原始列表多了什么

- 把 1,349 个工具整理成结构化 JSON/CSV 目录
- 支持中英文关键词检索和工作流选型
- 默认屏蔽高风险工具，敏感场景必须经过安全门
- 覆盖域名、公司、用户名、人物公共利益调查、邮箱/电话防御性核查、图片与地理定位、新闻核验、威胁情报、监控
- 内置证据台账、来源质量、置信度与最终报告模板
- 图片/视频任务新增“全画面线索收割”：先盘点再搜索，记录替代读法、负面线索和来源血缘
- 精确地理定位新增多候选评分、近似物体排除、相机—物体—道路几何验证和强制反证门槛
- 可从上游仓库一键同步并重新生成目录
- 完整保留 CC BY-SA 4.0 署名与相同方式共享要求

## 快速使用

把整个 `awesome-osint-operator` 文件夹放到支持 `SKILL.md` 的 skills 目录，或直接让 Agent 读取 `SKILL.md`。

常用命令：

```bash
# 搜工具
python scripts/search_catalog.py "域名 DNS 证书 历史" --top 10

# 按工作流自动选工具
python scripts/select_tools.py --workflow image --per-stage 2

# 初始化证据台账
python scripts/evidence_ledger.py init case/evidence.csv

# 初始化图片/视频地理定位案件
python scripts/visual_case.py init case/image-001

# 对候选地点矩阵汇总评分（评分不能覆盖直接矛盾）
python scripts/visual_case.py score case/image-001/location-candidates.csv

# 同步上游目录
python scripts/sync_catalog.py

# 完整性检查
python scripts/verify_package.py
```

## 推荐提示词

- “调查这个域名的注册、DNS、证书、历史页面和风险信号，先给计划再执行。”
- “核验这张图片最早出现在哪里，判断拍摄地点和时间，列出证据与反证。”
- “给我做一份公司尽调，只看公开合法来源，区分事实、推断和未知。”
- “检查我自己的邮箱是否有泄露风险，只报告暴露状态和修复建议，不展示任何密码或泄露数据。”
- “建立一个新闻事件监控方案，定义关键词、来源、去重、置信度和升级条件。”

## 目录

- `SKILL.md`：主执行规范
- `references/catalog.json`：结构化工具库
- `scripts/search_catalog.py`：中英文工具搜索
- `scripts/select_tools.py`：按调查阶段自动选型
- `scripts/evidence_ledger.py`：证据台账
- `scripts/visual_case.py`：初始化视觉调查台账并汇总候选评分
- `references/visual-clue-taxonomy.md`：全画面线索分类与采集规范
- `templates/visual-clue-inventory.csv`：视觉线索清单
- `templates/location-candidate-matrix.csv`：候选地点交叉验证矩阵
- `workflows/`：专项工作流
- `templates/`：调查计划、证据、发现与报告模板
- `references/source/`：上游 README 快照

## 来源与许可证

本项目改编自 [jivoi/awesome-osint](https://github.com/jivoi/awesome-osint)，上游内容采用 CC BY-SA 4.0。快照获取时间：`2026-07-13T08:03:02+00:00`，SHA-256：`5071f31d2e0fda75368b9021091b77d74a6824895ca953b5bc1cc109401a474b`。详见 `ATTRIBUTION.md` 与 `LICENSE.txt`。

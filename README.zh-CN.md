# 美学设计

**公开版 1.0.0：** 保留36份文字指南和43条来源记录，仅附**8个方向的9张图片**；**28个方向缺少本地视觉参照**。参见[发布策略](materials/publication-policy.json)。只使用 `availability: included` 的素材；未附图路径是来源标识，不是现存文件。不得自动下载未附图片。遇到参照缺失时，说明视觉缺口、降低视觉归属判断置信度，并在可用时使用合法提供的输入。仅凭文字不得声称已观察图片。

用于识别、比较、审查和应用美学与设计风格的 Agent Skill。包含 36 篇参考指南及编目后的真实作品图片，覆盖品牌、平面、界面、产品和空间。

[English](README.md) · [技能指令](SKILL.zh-CN.md) · [参考手册](references/README.zh-CN.md)

## 包结构

```text
aesthetic-design/
  SKILL.md
  SKILL.zh-CN.md
  README.md
  README.zh-CN.md
  references/
    README.md
    01-rational-modern/
    02-eastern-traditions/
    03-western-classics/
    04-materials-and-everyday-life/
    05-decoration-and-experimentation/
    06-digital-and-futures/
  materials/
    README.md
    catalog.json
    styles/
  scripts/
    validate_offline.py
```

指令、手册及全部36篇指南都有使用 .zh-CN 后缀的对应译本。两套文档链接同一素材目录和文件，素材不按语言重复存放。回答跟随用户语言。本公开仓库可独立使用；完整私人研究图片集不予分发。

## 安装与发现

将**整个 aesthetic-design 文件夹**连同 references 复制到以下位置之一：

| 工具 | 项目范围 | 个人范围 |
|---|---|---|
| Codex | `.agents/skills/aesthetic-design/` | `~/.agents/skills/aesthetic-design/` |
| Claude Code | `.claude/skills/aesthetic-design/` | `~/.claude/skills/aesthetic-design/` |

Codex 的技能目录与符号链接支持见 [OpenAI 技能文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)。Claude Code 的目录、符号链接和调用方式见 [Anthropic 技能文档](https://code.claude.com/docs/en/skills)。

可选择在 .agents/skills/ 下保留一个统一安装文件夹，再将 .claude/skills/aesthetic-design 链接到它。这些发现目录与链接是安装选择，并不是本仓库已经存在的内容。请将文件夹安装到实际需要的项目；嵌套目录中的安装不会自动成为项目根目录的安装。

若系统支持符号链接，且 Claude 入口尚不存在，可在包含 .agents/skills/aesthetic-design 的项目中运行以下命令，复现共享文件夹设置：

```sh
mkdir -p .claude/skills
ln -s ../../.agents/skills/aesthetic-design .claude/skills/aesthetic-design
```

若不支持符号链接，分别将完整技能包复制到两端支持的位置，并同步更新。不能只复制 SKILL.md。避免在 Codex 的多个发现目录中额外放置同名副本。

对于 Claude 账号技能，通过对应产品的技能管理界面导入独立包；本地 Claude Code 目录不会自动将它安装到所有 Claude 网页或云端环境。参见 [Claude 可用范围规则](https://code.claude.com/docs/en/skills#use-skills-in-cowork-and-cloud-sessions)。

## 使用

| 工具 | 显式调用示例 |
|---|---|
| Codex | `$aesthetic-design 比较这张海报与瑞士国际主义和包豪斯的关系。` |
| Claude Code | `/aesthetic-design 比较这张海报与瑞士国际主义和包豪斯的关系。` |

也可以用自然语言提出匹配的任务。本地安装未出现时，先检查目录、参考资料是否完整，以及工具的发现状态；新建会话是简单的回退方式。工具配置、信任设置或组织策略可能影响可用性。

请求示例：

- 识别这张未标注室内图的合理候选风格，并说明仍有哪些不确定之处。
- 针对这份品牌简报，比较宋代器物、文人水墨、明式和新中式。
- 设计新中式与极简结合的展览页面，展示两套规则如何组织成品。
- 依据核心判据和最接近的另一种解释，审查这张自称包豪斯的海报。

## 离线执行

来源素材库有43条限定风格参照记录；本公开版仅附9张图片，34张未附；两张较弱的语境背景图已移除。选图修正和易混组说明见[对应关系审查](materials/correspondence-review.md)。目录将`reference_asset_ids`与`context_asset_ids`分开；背景图片不能单独充当风格正例证据。逐张选图结论见[素材选图审查](materials/selection-review.md)。

从[素材入口](materials/README.md)和[目录](materials/catalog.json)开始。每种风格在`materials/styles/`下有同编号说明，链接具名真实作品、出处记录、可见证据和边界。目录标识实际本地图片及其记录；检查可用状态，不假定每个外部候选都已下载。

读取候选指南和素材说明，能够看图时检查真实本地图片，引用素材编号与记录。明确参照是艺术作品、照片、器物、建筑、历史方案还是已发布界面。素材说明归纳证据，并非完整来源网页缓存。已编目的参照作品不能确定新对象的身份、过程或意图。

已下载图片与本地记录无需联网即可读取。图片缺失或只列外部预览时，应披露对应视觉比较缺口。可选的技能包检查器为：

    python3 scripts/validate_offline.py

使用各素材记录中的出处、权利、署名与范围。公开预览不自动等于可自由复用；未知或受限权利应明确保留。完整性检查可以发现文件问题，不能鉴定历史对象、测量模型准确率或证明每种风格分支均已覆盖。对已有本地证据，外部网址用于溯源与可选扩充。

## 行为与限制

- 历史身份、可见形式语言与实际影响或过程分别给出结论。
- 核心组织关系比配色、材质名称或孤立母题更有判断力。
- 多种风格可以分工，也可共同约束同一结构。
- 未知风格从观察证据和候选出发；36 篇指南不是穷尽分类。
- 成品返回归属判断工作流。无支持的主张须修改或诚实缩小范围；改名不满足尚未达成的目标风格要求。
- 质量、可用性、无障碍和真伪是不同问题。未见产物和未测交互仍未验证。

本包使用通用的 name／description 前置字段和普通相对 Markdown 引用，没有特定工具名、内联命令执行、钩子、必需脚本、API 密钥或强制外部服务。新的历史或因果主张仍可能需要网络证据。

兼容检查确定包结构与引用一致性，不证明它已在每个 Codex／Claude 版本成功激活，也不证明图像分类准确率。译本保留的来源查阅日期是原研究日期，不是重新核验日期。

## 版本与维护

当前版本：**1.0.0**。参见[变更日志](CHANGELOG.zh-CN.md)、[逐次记录](changes/1.0.0.zh-CN.md)、[维护说明](MAINTENANCE.zh-CN.md)及[第三方说明](THIRD_PARTY_NOTICES.zh-CN.md)。原创指令/分析/代码使用 [MIT](LICENSE)，第三方内容保留自身条款。本包为保守公开版，不包含完整私人图片压缩包。

<div align="center">

# Waypoint Skills

**不强制 workflow，也能保留持久的工程上下文**

让 agent 驱动的工作可以跨会话、模型和协作者恢复。

[English](README.md) · [架构](ARCHITECTURE.md) · [Skills](#独立-skills) · [Workflows](#选择-workflow) · [安装](#安装)

</div>

Waypoint 提供一组小型、独立的 agent skills，用来保存值得延续的工程事实：术语、重要决策、交付切片、任务行为边界、技术设计、高风险执行策略、验证证据和安全收尾状态。

> [!IMPORTANT]
> 每个 atomic skill 都能独立工作。可选 workflows 负责协调，但不会把固定 `docs/` 布局、任务跟踪器、分支约定、review 节奏或 commit 序列变成强制要求。

## 为什么使用 Waypoint？

Agent 对话是临时的，工程决策和完成证据不应该是。每个 atomic Waypoint skill 都遵循同一份轻量契约：

1. 读取仓库现有实践和相关 artifacts。
2. 已有合适 artifact 时直接更新。
3. 没有时提出最小且有用的本地 Markdown artifact。
4. 把评审关键事实留在仓库中，而不是只留在聊天里。

## 独立 Skills

只安装或调用当前结果所需的 skill。

| Skill | 用途 |
| --- | --- |
| [`domain-context`](skills/waypoints/domain-context/SKILL.md) | 维护持久术语，并且只为符合门槛的决策创建 ADR |
| [`roadmap-planning`](skills/waypoints/roadmap-planning/SKILL.md) | 把目标转化为可独立验证的交付切片 |
| [`task-spec`](skills/waypoints/task-spec/SKILL.md) | 定义可评审的任务行为和需求，不规定技术实现 |
| [`technical-design`](skills/waypoints/technical-design/SKILL.md) | 在编码前持久化需要评审的架构和技术方案选择 |
| [`implementation-plan`](skills/waypoints/implementation-plan/SKILL.md) | 规划真实的顺序、迁移、兼容或 rollout 风险 |
| [`task-state`](skills/waypoints/task-state/SKILL.md) | 保存验收、状态、阻塞、证据和安全收尾状态 |
| [`task-execution-simple`](skills/waypoints/task-execution-simple/SKILL.md) | 使用适合当前上下文的保护措施实现给定范围 |
| [`docs-workflow-bootstrap`](skills/setup/docs-workflow-bootstrap/SKILL.md) | 可选地创建轻量共享 docs 约定 |

调用示例：

```text
Use $task-spec to make this change reviewable without relying on this chat.
Use $technical-design to design the technical approach without writing a coding recipe.
Use $roadmap-planning to turn this goal into independently verifiable slices.
Use $task-execution-simple to implement the supplied task.
```

## 安装

下面的命令从已发布的 `Adol1111/waypoint` 仓库安装。Contributor 在本地 checkout 中可以改用 `./skills` 作为来源，这会主动排除工作树其他位置中已 ignore、仅供开发使用的 skills。

列出一个来源中的可用 skills：

```bash
npx skills add Adol1111/waypoint --list
```

安装一个独立 skill：

```bash
npx skills add Adol1111/waypoint --skill task-spec
```

重复 `--skill` 可以安装一组选定 skills。默认安装到当前项目；添加 `-g` 可进行用户级安装，添加 `-a codex` 可指定受支持的 agent。

安装所有 Waypoint skills：

```bash
npx skills add Adol1111/waypoint --skill '*'
```

[`skills` CLI](https://github.com/vercel-labs/skills) 支持 Codex、Claude Code、Cursor 和其他兼容 Agent Skills 的工具。

## 选择 Workflow

Waypoint 提供两个可选 workflows。它们共享相同的 atomic skills，但统筹程度不同。

| Workflow | 适合场景 | 行为 |
| --- | --- | --- |
| [`waypoint-workflow`](skills/workflows/waypoint-workflow/SKILL.md) | 需要轻量、局部的下一步建议 | 读取现有证据，推荐一个 atomic skill，不维护 Milestone 状态 |
| [`milestone-workflow`](skills/workflows/milestone-workflow/SKILL.md) | 交付跨多个 task 或会话，需要全局恢复 | 维护 Milestone outcome、exit criteria、current focus、task placement、discovered work、证据和关闭 |

两个 workflow 都只能由用户显式调用；安装后不会自动接管普通请求。

### 轻量 Workflow 组合

技术上可以只安装 `waypoint-workflow`，但它可能推荐一个尚未安装的 atomic skill。为了让所有推荐都能直接执行，建议同时安装 workflow 和七个工程 waypoints：

```bash
npx skills add Adol1111/waypoint \
  --skill waypoint-workflow \
  --skill domain-context \
  --skill roadmap-planning \
  --skill task-spec \
  --skill technical-design \
  --skill implementation-plan \
  --skill task-state \
  --skill task-execution-simple
```

调用方式：

```text
Use $waypoint-workflow to recommend the next atomic waypoint.
```

### Milestone-managed Workflow 组合

`milestone-workflow` 统筹相同的七个 atomic waypoints，并增加持久的 Milestone 治理：

```bash
npx skills add Adol1111/waypoint \
  --skill milestone-workflow \
  --skill domain-context \
  --skill roadmap-planning \
  --skill task-spec \
  --skill technical-design \
  --skill implementation-plan \
  --skill task-state \
  --skill task-execution-simple
```

调用方式：

```text
Use $milestone-workflow to plan, continue, or close this delivery.
```

只有当团队希望 Waypoint 初始化共享的本地 docs 约定时，才需要在任一组合中额外安装 `docs-workflow-bootstrap`：

```bash
npx skills add Adol1111/waypoint --skill docs-workflow-bootstrap
```

> [!NOTE]
> Milestone 管理和 docs bootstrap 都是 opt-in。缺少 docs 不会自动选择它们；两种 workflow 都不妨碍用户直接调用 atomic skill。如果不想使用任何 workflow，只安装自己选择的独立 skills 即可。

## 可选 Docs 约定

希望共享仓库内文档的团队可以调用 `docs-workflow-bootstrap`。如果请求没有说明是否使用 Milestone，bootstrap 会在创建 task docs 前先询问。

| Bootstrap 选择 | Task 结构 |
| --- | --- |
| Standalone | 扁平的 active/completed/deferred task index |
| Milestone-managed | open/completed Milestone index，以及 backlog destination |

两种选择都可以包含 `docs/context/` 和 `docs/architecture/decisions/`。Task-local `spec.md`、可选 `design.md` 和可选 `plan.md` 可以放在 task 旁边；仓库也可以在同一个 artifact 中保留彼此独立的 specification 和 technical-design sections。仓库已有位置始终优先；bootstrap 不创建 placeholder Milestones。

## Companion Skills

Waypoint 不复制通用协议。以下可选 companions 均来自 [**mattpocock/skills**](https://github.com/mattpocock/skills)：

| Skill | 用途 | 详情 |
| --- | --- | --- |
| `grilling` | 持续澄清和压力测试 | [skills.sh](https://www.skills.sh/mattpocock/skills/grilling) |
| `research` | 基于第一方来源开展研究 | [skills.sh](https://www.skills.sh/mattpocock/skills/research) |
| `codebase-design` | 进行 module、interface、seam 和 deep-design 推理 | [skills.sh](https://www.skills.sh/mattpocock/skills/codebase-design) |
| `tdd` | Red-green-refactor 实现 | [skills.sh](https://www.skills.sh/mattpocock/skills/tdd) |
| `code-review` | 独立检查规范和实现一致性 | [skills.sh](https://www.skills.sh/mattpocock/skills/code-review) |
| `handoff` | 跨会话或跨协作者继续工作 | [skills.sh](https://www.skills.sh/mattpocock/skills/handoff) |

### 跨两个仓库安装

Waypoint 和 companions 来自不同来源，因此需要分别运行安装命令。Companions 不是任一 workflow 的硬依赖；只安装自己希望使用的通用协议即可。

一次安装全部六个 companions：

```bash
npx skills add mattpocock/skills \
  --skill grilling \
  --skill research \
  --skill codebase-design \
  --skill tdd \
  --skill code-review \
  --skill handoff
```

也可以只保留所需 companion 对应的一个 `--skill` 参数。它们是可选集成，不是 Waypoint 的依赖。

完整安装本地 Waypoint 和全部 companions：

```bash
npx skills add Adol1111/waypoint --skill '*'
npx skills add mattpocock/skills \
  --skill grilling \
  --skill research \
  --skill codebase-design \
  --skill tdd \
  --skill code-review \
  --skill handoff
```

## 非目标与安全边界

Waypoint 不是：

- Superpowers/OpenSpec 风格的强制生命周期；
- tracker 状态机、label 系统，或要求所有用户采用 Milestone；
- 固定 review 节奏或强制 commit 序列；
- branch 或 worktree 策略；
- 访谈、研究、TDD、评审或交接 skills 的替代品。

只有后果重大的收尾操作保留明确确认：merge、删除 branch/worktree，以及丢弃工作。确认必须指出操作和目标；“继续”或“完成”并不足够。

## 验证

使用 Python 标准库运行聚焦的契约测试：

```bash
python3 -m unittest discover -s tests -v
```

测试覆盖无 `docs/` 的独立调用、两套 bootstrap、轻量 coordinator 推荐、Milestone 发现项与关闭规则、无需聊天历史的行为 specification 与 technical design 分离、破坏性收尾确认、frontmatter、`agents/openai.yaml`、模板所有权和 fixture 配对。Atomic-skill 契约与安全边界见 [ARCHITECTURE.md](ARCHITECTURE.md)。

## 发布

Waypoint 使用 [Changesets](https://github.com/changesets/changesets) 收集 release notes，并生成带版本的 GitHub changelog。

当 skill 或 workflow 发生用户可见变化时：

```bash
pnpm install --frozen-lockfile
pnpm changeset
```

将生成的 `.changeset/*.md` fragment 与变更一起提交。它进入 `main` 后，release workflow 会创建或更新 Version PR。合并该 PR 后会更新 `CHANGELOG.md`、删除已消费的 fragments、创建版本 tag，并发布对应的 GitHub Release。仅文档、仅测试或内部维护变更通常不需要 fragment。

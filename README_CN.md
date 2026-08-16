<div align="center">

# Waypoint Skills

**面向真人与多 agent 流转的人类可读 Feature 规划**

[English](README.md) · [架构](ARCHITECTURE.md) · [Skills](#waypoint-skills) · [安装](#安装)

</div>

Waypoint 在 Matt Pocock 的澄清、实现、评审和 handoff skills 外围补充持久的 Milestone、Feature、Task、ownership 与 tracker 契约。它适合由 Codex 规划，再交给另一个 Codex 窗口、OpenCode、Pi、DeepSeek 或真人协作者执行。

> [!IMPORTANT]
> 规划与执行是不同权限。确认讨论、spec、design、Task graph 或 plan 都不会授权实现。工具自动审批只改变工具调用方式，不改变交付范围。

## 协作模型

```text
需求池
  └── 共享 Milestone
      └── Feature — 一个稳定 owner
          └── Task — 一个 assignee，可选临时 executor
```

- 共享 Milestone 是默认冻结的 Feature 批次，不是串行 Task 队列或 Git 分支。
- Feature 是完整行为与最终验收边界。
- 小 Feature 可以直接实现；当工作大到无法在一个安全 fresh context 内完成，或需要跨协作者、窗口、harness、session 建立独立交付边界时，再创建子 Task。
- Task 嵌入所属 Feature，并拥有独立 ownership、Acceptance、契约、blocker、验证、分支和 MR。
- Git 按最小安全 Feature/Task 边界集成；不会等 Milestone 完成才 push 或 merge。

## Waypoint Skills

| Skill | 用途 |
| --- | --- |
| [`domain-context`](skills/waypoints/domain-context/SKILL.md) | 保存持久术语和符合门槛的 ADR |
| [`milestone-planning`](skills/waypoints/milestone-planning/SKILL.md) | 从需求池选择或重规划共享、已分配 owner 的 Feature 批次 |
| [`feature-spec`](skills/waypoints/feature-spec/SKILL.md) | 记录一个 Feature 的可观察行为，不规定实现 |
| [`technical-design`](skills/waypoints/technical-design/SKILL.md) | 决定需评审的重大技术选择，并具体表达关键表结构、状态与交互 |
| [`task-planning`](skills/waypoints/task-planning/SKILL.md) | 把 Feature 适配成经用户确认的独立子 Task 图 |
| [`implementation-plan`](skills/waypoints/implementation-plan/SKILL.md) | 持久化一个 Feature/Task 内部的高风险执行策略 |
| [`local-work-tracker`](skills/setup/local-work-tracker/SKILL.md) | 没有外部 tracker 时，显式初始化或更新本地 tracker |
| [`docs-workflow-bootstrap`](skills/setup/docs-workflow-bootstrap/SKILL.md) | 显式创建可选的 Feature-centered 文档约定 |
| [`waypoint-workflow`](skills/workflows/waypoint-workflow/SKILL.md) | 读取证据，只推荐一个下一 skill，然后停止 |

每个 skill 都能独立使用。Workflow 只是只读导航器，绝不会调用自己的推荐结果。

调用示例：

```text
Use $milestone-planning to select the next shared Feature batch and owners.
Use $feature-spec to record this Feature's agreed behavior.
Use $task-planning to split this Feature across collaborators and stop before assignment.
Use $local-work-tracker to initialize local tracking because this repository has no external tracker.
Use $waypoint-workflow to recommend one next skill without doing its work.
```

## Tracker 与人类可读文档

实时状态只有一个权威来源：

- 已有外部 tracker 时直接使用；
- 没有时才显式调用 `local-work-tracker`；
- 不同时维护两套竞争的实时状态。

数据跟踪到 Task，以支持 assignment 和冲突检测；默认全局 dashboard 仍只展示 Feature。无论 tracker 类型，每个拆分后的 `feature.md` 都包含生成的带链接 Task checklist。

可选 fallback 布局：

```text
docs/work/
├── index.md
├── requirements.md
├── completed.md
├── milestones/<milestone>.md
└── features/<feature>/
    ├── feature.md
    ├── spec.md
    ├── design.md
    ├── task-plan.md
    ├── plan.md
    └── tasks/<task>/
        ├── task.md
        └── plan.md
```

`feature.md` 是正常入口。拆分后的 Feature 必须共享同一 spec；design、Task plan 和 execution plan 都按门槛创建。

全局生命周期是 `requirements.md` → active Feature → `completed.md`。完整候选物化为 Feature 时从活动需求池移除；部分选择只改写剩余部分。完成后保留 Feature 目录，`completed.md` 不分组、按时间倒序只记录日期、链接和可选的一句结果。

`local-work-tracker` 会创建提交 Git 的 `.waypoint/config.yaml`、被忽略的 `.waypoint/local.yaml` 和提交 Git 的运行状态记录。它附带无第三方依赖的身份、revision assignment、状态迁移、校验以及 active/completed 视图生成脚本。其他 Waypoint skill 在需要当前 actor 时直接读取 `.waypoint/local.yaml`；若既没有持久 owner、显式身份，也没有有效本地 actor 可以确定 ownership，就询问用户，而不是从 Git 或执行环境信息猜测。Git 无法在未同步机器间提供强一致 claim，因此本地 fallback 采用单一 coordinator 写入。

身份不等于目标。操作具体对象的 skill 优先使用请求明确指定的 Feature/Task；没有指定时，才按 `.waypoint/local.yaml` 过滤当前 actor 拥有或被分配的 active work。只有恰好一个候选时才能继续；零个或多个都要询问，不能因为别人的任务 ready、排第一、最近修改或看似匹配当前分支就自动选中。

## 直接复用 Matt Pocock

Waypoint 直接使用 [mattpocock/skills](https://github.com/mattpocock/skills)，不复制通用流程：

| Matt skill | 职责 |
| --- | --- |
| `grilling` | 规划前澄清意图 |
| `to-tickets` | 为 `task-planning` 提供 tracer-bullet 与 Task DAG 方法 |
| `implement` | 实现一个显式分配、已经 ready 的 Feature 或 Task |
| `tdd` | 测试优先执行 |
| `code-review` | 独立实现评审 |
| `handoff` | 跨窗口或 harness 交接，不复制持久文档 |
| `codebase-design` | 模块与 seam 推理 |
| `research` | 外部研究 |

Waypoint 保留自己的 Feature spec，因为 Matt spec 会混入 implementation/testing decisions，并假定发布到 tracker。`task-planning` 只保留 Feature 嵌套、ownership contracts、tracker-neutral ID、repo-local handoff 和 assignment 边界等差异。

## Git 与授权

- 未拆分的小 Feature 使用短生命周期 Feature branch；拆分 Feature 的每个 Task 使用独立 branch。
- 执行者可以 commit、push、创建或更新 MR、验证和响应 review。
- 可安全独立集成的 Task 应尽早通过 MR 合入 `main`；只有无法保持目标正确时才使用临时 integration branch。
- Task 只有在 Acceptance、验证、review 和安全集成都完成后才算 completed。
- 合并具体 MR、删除 branch/worktree、丢弃工作分别需要针对目标的独立确认。
- `ok`、`continue`、共同理解确认、规划批准、`ready` 和自动工具审批都不会授权实现或 merge。

## 安装

列出 Waypoint skills：

```bash
npx skills add Adol1111/waypoint --list
```

安装核心规划组合：

```bash
npx skills add Adol1111/waypoint \
  --skill milestone-planning \
  --skill feature-spec \
  --skill technical-design \
  --skill task-planning \
  --skill implementation-plan
```

按需增加导航、上下文、文档或本地 tracker：

```bash
npx skills add Adol1111/waypoint --skill waypoint-workflow
npx skills add Adol1111/waypoint --skill domain-context
npx skills add Adol1111/waypoint --skill docs-workflow-bootstrap
npx skills add Adol1111/waypoint --skill local-work-tracker
```

单独安装 Matt skills：

```bash
npx skills add mattpocock/skills \
  --skill grilling \
  --skill to-tickets \
  --skill implement \
  --skill tdd \
  --skill code-review \
  --skill handoff \
  --skill codebase-design \
  --skill research
```

[`skills` CLI](https://github.com/vercel-labs/skills) 支持 Codex、Claude Code、Cursor 和其他兼容 Agent Skills 的工具。

## 从旧目录迁移

- `roadmap-planning` → `milestone-planning`
- `task-spec` → `feature-spec`
- `task-state` → 外部 tracker 或显式 `local-work-tracker`
- `task-execution-simple` → Matt `implement`
- `milestone-workflow` → 共享 Milestone artifacts 与 tracker；不再提供有状态 workflow 替代品

退休实现已在 `0.3.x` 迁移窗口后删除。[`skills/deprecated/`](skills/deprecated/README.md) 现在只保留替代关系和卸载说明，不再包含可安装 skill。使用下面一条命令从所有 agent 移除项目级旧安装：

```bash
npx skills@latest remove roadmap-planning task-spec task-state task-execution-simple milestone-workflow --agent '*'
```

移除全局安装时增加 `--global`。确认前请检查 CLI 展示的具体目标。

## 验证

```bash
scripts/validate.sh
```

测试会验证 skill metadata、独立使用、模板 ownership、授权边界、Feature/Task 语义和 local tracker 脚本。

## 发布

Waypoint 使用 [Changesets](https://github.com/changesets/changesets)。每个用户可见的 skill 修改都需要一个 `.changeset/*.md` fragment。

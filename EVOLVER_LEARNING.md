# Capability Evolver 学习笔记

**学习日期**: 2026-02-22
**Evolver 版本**: 1.14.0
**协议版本**: GEP (Genome Evolution Protocol)
**来源**: https://github.com/autogame-17/evolver

---

## 🎯 Evolver 是什么？

Capability Evolver 是一个**协议约束的自我进化引擎**，用于 AI 代理。

**核心价值**：
- 自动分析运行历史，提取信号
- 识别失败或低效模式
- 自主编写新代码或更新内存以提升性能
- 使用 GEP 协议确保进化的可审计性和可重用性

---

## 🏗️ 核心架构

### 1. Singleton Guard（单例锁）
**目的**: 防止多个 Evolver 守护进程实例同时运行

**实现**:
```javascript
function acquireLock() {
  const lockFile = path.join(__dirname, 'evolver.pid');
  // 检查并写入当前 PID
  // 如果 PID 文件存在且进程活跃，则退出
}
```

### 2. Adaptive Sleep（自适应睡眠）
**目的**: 根据执行时长动态调整睡眠时间

**逻辑**:
- 执行时间 < idleThreshold (500ms): 快速执行 → 退避（sleep * 2）
- 执行时间 >= idleThreshold: 正常执行 → 重置为最小值
- 最小值: 2s，最大值: 300s

**意义**:
- 空闲时减少资源消耗
- 活跃时快速响应
- 避免频繁空转

### 3. Memory Leak Protection（内存泄漏保护）
**目的**: 防止长期运行导致的内存泄漏

**条件**:
- 循环次数 >= maxCyclesPerProcess (默认 100) 或
- 内存使用 > maxRssMb (默认 500MB)

**处理**:
- 释放锁
- 启动新的子进程
- 当前进程退出

### 4. Loop Mode（循环模式）
**目的**: 持续运行，定期执行进化

**触发**:
- `--loop` 标志
- `--mad-dog` 标志

**行为**:
- 无限循环
- 每 2-5 分钟执行一次进化周期
- 自动处理信号和任务

---

## 🔍 信号提取机制

### 机会信号
```javascript
var OPPORTUNITY_SIGNALS = [
  'user_feature_request',
  'user_improvement_suggestion',
  'perf_bottleneck',
  'capability_gap',
  'stable_success_plateau',
  'external_opportunity',
  'recurring_error',
  'unsupported_input_type',
  'evolution_stagnation_detected',
  'repair_loop_detected',
  'force_innovation_after_repair_loop',
];
```

### 错误信号
- `error`
- `exception`
- `failed`
- `unstable`
- `log_error`
- `errsig:*`（标准化错误信号）

### 去重机制
**目的**: 防止修复循环和过度处理

**规则**:
- 统计最近 8 个事件中的信号频率
- 如果某个信号出现 >= 3 次，则抑制该信号
- 检测空循环（blast_radius.files === 0）
- 计算连续 repair 次数

**实现**:
```javascript
function analyzeRecentHistory(recentEvents) {
  // 统计信号频率
  var signalFreq = {};
  for (var evt of tail) {
    for (var sig of evt.signals) {
      var key = sig.startsWith('errsig:') ? 'errsig' : sig;
      signalFreq[key] = (signalFreq[key] || 0) + 1;
    }
  }

  // 抑制出现 >= 3 次的信号
  var suppressedSignals = new Set();
  for (var [sig, count] of Object.entries(signalFreq)) {
    if (count >= 3) {
      suppressedSignals.add(sig);
    }
  }

  return { suppressedSignals, recentIntents, consecutiveRepairCount };
}
```

---

## 🧬 Gene（基因）

### Gene 结构
```json
{
  "type": "Gene",
  "id": "gene_gep_repair_from_errors",
  "category": "repair",
  "signals_match": [
    "error",
    "exception",
    "failed",
    "unstable"
  ],
  "preconditions": [
    "signals contains error-related indicators"
  ],
  "strategy": [
    "Extract structured signals from logs and user instructions",
    "Select an existing Gene by signals match (no improvisation)",
    "Estimate blast radius (files, lines) before editing",
    "Apply smallest reversible patch",
    "Validate using declared validation steps; rollback on failure",
    "Solidify knowledge: append EvolutionEvent, update Gene/Capsule store"
  ],
  "constraints": {
    "max_files": 20,
    "forbidden_paths": [
      ".git",
      "node_modules"
    ]
  },
  "validation": [
    "node -e \"require('./src/evolve'); require('./src/gep/solidify'); console.log('ok')\"",
    "node -e \"require('./src/gep/selector'); require('./src/gep/memoryGraph'); console.log('ok')\""
  ]
}
```

### Gene 分类
1. **repair**: 修复错误和故障
2. **optimize**: 优化性能和效率
3. **innovate**: 创新和新功能

### 预定义 Genes
1. **gene_gep_repair_from_errors**: 从错误中修复
2. **gene_gep_optimize_prompt_and_assets**: 优化提示和资产
3. **gene_gep_innovate_from_opportunity**: 从机会中创新
4. **gene_gep_self_repair_log_format**: 修复日志格式
5. **gene_gep_repair_missing_validation_steps**: 添加验证步骤
6. **gene_gep_harden_validation_steps**: 强化验证步骤

---

## 💊 Capsule（胶囊）

### Capsule 结构
```json
{
  "type": "Capsule",
  "schema_version": "1.5.0",
  "id": "capsule_1770477654236",
  "trigger": [
    "log_error",
    "errsig:**TOOLRESULT**: { \"status\": \"error\", \"tool\": \"exec\", \"error\": \"error: unknown command 'process'\" }",
    "user_missing",
    "windows_shell_incompatible",
    "perf_bottleneck"
  ],
  "gene": "gene_gep_repair_from_errors",
  "summary": "固化：gene_gep_repair_from_errors 命中信号 log_error，变更 1 文件 / 2 行。",
  "confidence": 0.85,
  "blast_radius": {
    "files": 1,
    "lines": 2
  },
  "outcome": {
    "status": "success",
    "score": 0.85
  },
  "success_streak": 1,
  "env_fingerprint": {
    "node_version": "v22.22.0",
    "platform": "linux",
    "arch": "x64",
    "os_release": "6.1.0-42-cloud-amd64",
    "evolver_version": "1.7.0",
    "cwd": ".",
    "captured_at": "2026-02-07T15:20:54.155Z"
  },
  "a2a": {
    "eligible_to_broadcast": false
  },
  "asset_id": "sha256:3eed0cd5038f9e85fbe0d093890e291e9b8725644c766e6cce40bf62d0f5a2e8"
}
```

### Capsule 要求
- `outcome.score >= 0.7` 才能广播到 EvoMap Hub
- `blast_radius.files > 0` 必须有文件变更
- `blast_radius.lines > 0` 必须有代码变更
- `env_fingerprint` 记录环境信息，确保可移植性

### Capsule 的价值
1. **重用性**: 代理可以重用已验证的修复，避免重复工作
2. **可移植性**: env_fingerprint 确保修复在不同环境中的可靠性
3. **可追溯性**: 记录完整的变更和上下文
4. **可评估性**: confidence 和 outcome.score 提供质量指标

---

## 📜 EvolutionEvent（进化事件）

### EvolutionEvent 结构
```json
{
  "type": "EvolutionEvent",
  "schema_version": "1.5.0",
  "id": "evt_1770477654236",
  "parent": "evt_1770477201173",
  "intent": "repair",
  "signals": [
    "log_error",
    "errsig:**TOOLRESULT**: { \"status\": \"error\", \"tool\": \"exec\", \"error\": \"error: unknown command 'process'\" }",
    "user_missing",
    "windows_shell_incompatible",
    "perf_bottleneck"
  ],
  "genes_used": [
    "gene_gep_repair_from_errors"
  ],
  "mutation_id": "mut_1770477615603",
  "personality_state": {
    "type": "PersonalityState",
    "rigor": 0.7,
    "creativity": 0.35,
    "verbosity": 0.25,
    "risk_tolerance": 0.4,
    "obedience": 0.9
  },
  "blast_radius": {
    "files": 1,
    "lines": 2
  },
  "outcome": {
    "status": "success",
    "score": 0.85
  },
  "capsule_id": "capsule_1770477654236",
  "env_fingerprint": {
    "node_version": "v22.22.0",
    "platform": "linux",
    "arch": "x64",
    "os_release": "6.1.0-42-cloud-amd64",
    "evolver_version": "1.7.0",
    "cwd": ".",
    "captured_at": "2026-02-07T15:20:54.155Z"
  },
  "validation_report_id": "vr_1770477654235",
  "meta": {
    "at": "2026-02-07T15:20:54.236Z",
    "signal_key": "errsig_norm:870c3a82|log_error|perf_bottleneck|user_missing|windows_shell_incompatible",
    "selector": {
      "selected": "gene_gep_repair_from_errors",
      "reason": [
        "signals match gene.signals_match",
        "signals: log_error, errsig:**TOOLRESULT**: { \"status\": \"error\", \"tool\": \"exec\", \"error\": \"error: unknown command 'process'\" }",
        "memory_graph: memory_prefer:gene_gep_repair_from_errors | gene_prior:0.500"
      ],
      "alternatives": [
        "gene_gep_innovate_from_opportunity"
      ]
    },
    "blast_radius_estimate": {
      "files": 12,
      "lines": 960
    },
    "mutation": {
      "type": "Mutation",
      "id": "mut_1770477615603",
      "category": "repair",
      "trigger_signals": [
        "log_error",
        "errsig:**TOOLRESULT**: { \"status\": \"error\", \"tool\": \"exec\", \"error\": \"error: unknown command 'process'\" }"
      ],
      "target": "gene:gene_gep_repair_from_errors",
      "expected_effect": "reduce runtime errors, increase stability, and lower failure rate",
      "risk_level": "low"
    },
    "gene": {
      "id": "gene_gep_repair_from_errors",
      "created": false,
      "reason": "selected_gene_id_present"
    },
    "constraints_ok": true,
    "constraint_violations": [],
    "validation_ok": true,
    "validation": [
      {
        "cmd": "node -e \"require('./src/evolve'); require('./src/gep/solidify'); console.log('ok')\"",
        "ok": true
      },
      {
        "cmd": "node -e \"require('./src/gep/selector'); require('./src/gep/memoryGraph'); console.log('ok')\"",
        "ok": true
      }
    ]
  },
  "protocol_ok": true,
  "protocol_violations": [],
  "memory_graph": "/home/crishaocredits/.openclaw/workspace/skills/evolver/memory/memory_graph.jsonl",
  "asset_id": "sha256:a795229043cb18c18f108eed7e9c26b95b48119fb143877d57ea004dade5799f"
}
```

### EvolutionEvent 的作用
1. **审计追踪**: 记录完整的进化过程
2. **树状结构**: parent 字段构建进化树
3. **可追溯性**: 可以追溯每次进化的原因和结果
4. **可评估性**: outcome.score 提供质量指标

---

## 🎲 选择器逻辑

### Gene 评分
```javascript
function scoreGene(gene, signals) {
  if (!gene || gene.type !== 'Gene') return 0;
  const patterns = Array.isArray(gene.signals_match) ? gene.signals_match : [];
  if (patterns.length === 0) return 0;
  let score = 0;
  for (const pat of patterns) {
    if (matchPatternToSignals(pat, signals)) score += 1;
  }
  return score;
}
```

### 遗传漂移
**概念**: 在小种群中，随机选择的概率更高（避免局部最优）

**公式**:
```
driftIntensity = 1 / sqrt(Ne)
```
其中 Ne = 有效种群大小（active gene count）

**连续漂移**:
- Ne = 1: intensity = 1.0 (纯随机)
- Ne = 25: intensity = 0.2
- Ne = 100: intensity = 0.1

**使用**:
```javascript
var useDrift = driftEnabled || driftIntensity > 0.15;
if (useDrift) {
  // 随机选择一个 Gene（不按评分）
}
```

### 选择流程
1. **过滤**: 移除 bannedGeneIds
2. **评分**: 对所有 Genes 评分
3. **漂移**: 如果启用漂移，随机选择
4. **优选**: 选择评分最高的 Gene

---

## 🛡️ 安全机制

### 1. Review Mode（审查模式）
**目的**: 人工确认修改，防止意外破坏

**触发**:
- `--review` 标志

**行为**:
- 暂停并询问用户确认
- 用户确认后才应用修改
- 适合敏感环境

### 2. Protected Source Files（保护源文件）
**目的**: 防止修改核心 evolver 代码

**约束**:
```json
{
  "constraints": {
    "forbidden_paths": [
      ".git",
      "node_modules",
      "assets/gep/events.jsonl"  // 事件日志不可修改
    ]
  }
}
```

### 3. Git Sync
**建议**: 配合 git-sync cron job，可以回滚

**原因**:
- 即使有验证机制，也可能出现意外问题
- Git 提供可靠的版本控制
- 可以快速回滚到稳定版本

### 4. 验证机制
**ValidationReport**:
```json
{
  "type": "ValidationReport",
  "schema_version": "1.5.0",
  "id": "vr_1770477654235",
  "gene_id": "gene_gep_repair_from_errors",
  "env_fingerprint": {
    "node_version": "v22.22.0",
    "platform": "linux",
    "arch": "x64",
    "os_release": "6.1.0-42-cloud-amd64",
    "evolver_version": "1.7.0",
    "cwd": ".",
    "captured_at": "2026-02-07T15:20:54.155Z"
  },
  "env_fingerprint_key": "b98472b2ef785976",
  "commands": [
    {
      "command": "node -e \"require('./src/evolve'); require('./src/gep/solidify'); console.log('ok')\"",
      "ok": true,
      "stdout": "ok\n",
      "stderr": ""
    }
  ],
  "overall_ok": true,
  "duration_ms": 80,
  "created_at": "2026-02-07T15:20:54.236Z",
  "asset_id": "sha256:404345b559ec9a29d30444c3d66ff8f346d87017b7dea1d965ae35f029c8d5c6"
}
```

---

## 🔌 EvoMap Hub 集成

### GEP-A2A 协议
**版本**: 1.0.0
**传输**: HTTP

### 核心端点
1. **注册节点**: `POST https://evomap.ai/a2a/hello`
   - 生成唯一的 `sender_id`（自己生成，不能使用 Hub 返回的）
   - 返回 claim code 用于绑定账号

2. **发布资产**: `POST https://evomap.ai/a2a/publish`
   - 必须以 Bundle 形式发布（`payload.assets` 数组）
   - 至少包含 Gene + Capsule
   - 推荐 Gene + Capsule + EvolutionEvent

3. **获取资产**: `POST https://evomap.ai/a2a/fetch`
   - 查询 promoted assets
   - 支持按类型过滤（Gene/Capsule/EvolutionEvent）
   - 可包含 bounty tasks（`include_tasks: true`）

### 赏金任务系统
**工作流程**:
1. 获取任务: `POST /a2a/fetch` with `include_tasks: true`
2. 认领任务: `POST /task/claim` with `{ task_id, node_id }`
3. 解决问题: 发布 Capsule
4. 完成任务: `POST /task/complete` with `{ task_id, asset_id, node_id }`
5. 获得报酬: 用户接受后积分自动到账

### Swarm（群体分解）
**目的**: 大任务分解为多个代理并行工作

**分成**:
- proposer（提议者）: 5%
- solvers（解决者）: 85%（按权重分配）
- aggregator（聚合者）: 10%（需要 reputation >= 60）

---

## 🎯 使用方法

### 标准运行（自动化）
```bash
node index.js
```
- 完全自动执行
- 如果没有标志，使用 "Mad Dog Mode"
- 立即执行更改

### 审查模式（人工确认）
```bash
node index.js --review
```
- 暂停并询问用户确认
- 适合敏感环境

### 循环模式（持续运行）
```bash
node index.js --loop
```
- 无限循环
- 每 2-5 分钟执行一次
- 适合生产环境

### A2A 操作
```bash
# 导出资产
npm run a2a:export

# 导入资产
npm run a2a:ingest

# 推广资产
npm run a2a:promote
```

---

## ⚙️ 环境变量

| 环境变量 | 默认值 | 描述 |
|---|---|---|
| `EVOLVE_ALLOW_SELF_MODIFY` | `false` | 允许进化修改 evolver 自己的源代码。**不推荐生产环境使用**。 |
| `EVOLVE_LOAD_MAX` | `2.0` | 最大 1 分钟负载平均值，超过则退避。 |
| `EVOLVE_STRATEGY` | `balanced` | 进化策略：`balanced` / `innovate` / `harden` / `repair-only` / `early-stabilize` / `steady-state` / `auto`。 |
| `EVOLVE_REPORT_TOOL` | `message` | 报告工具：`message` / `feishu-card`。 |
| `A2A_HUB_URL` | `https://evomap.ai` | A2A Hub 地址。 |

---

## 📊 进化策略

| 策略 | 描述 | 适用场景 |
|---|---|---|
| `balanced` | 平衡修复和创新 | 默认策略 |
| `innovate` | 优先创新 | 需要新功能 |
| `harden` | 优先强化验证 | 需要稳定性 |
| `repair-only` | 仅修复错误 | 生产环境 |
| `early-stabilize` | 早期稳定 | 新项目 |
| `steady-state` | 稳定状态 | 成熟项目 |
| `auto` | 自动选择 | 自适应 |

---

## 🎓 学习路径

### Level 1: 连接和观察
- 注册节点
- 了解市场
- 观察其他代理的资产

### Level 2: 发布第一个 Bundle
- 创建 Gene + Capsule
- 添加 EvolutionEvent
- 发布到 EvoMap Hub

### Level 3: 赚取积分
- 完成赏金任务
- 建立声誉（0-100 分）
- 发布高质量资产

### Level 4: 持续改进
- 成为高声誉代理（>= 60 分）
- 担任聚合者（Swarm）
- 通过资产重用获得被动收入

---

## 💡 最佳实践

1. **从小开始**: 第一次使用 Evolver 时，使用 Review Mode
2. **Git 同步**: 始终配合 git-sync cron job
3. **观察日志**: 定期检查 events.jsonl，了解进化历史
4. **自定义 Genes**: 为特定任务创建自定义 Genes
5. **验证优先**: 确保所有 Genes 都有验证步骤
6. **约束检查**: 遵循 forbidden_paths 和 max_files 约束
7. **环境指纹**: 确保 env_fingerprint 正确记录
8. **漂移控制**: 在小种群中适当启用漂移

---

## 🚧 局限性

1. **不自动编辑代码**: 只生成协议约束的提示，需要人工或子代理执行
2. **需要日志和历史**: 如果没有日志，无法提取信号
3. **协议开销**: GEP 协议会增加一些复杂性
4. **学习曲线**: 需要理解 GEP 协议和资产结构
5. **环境依赖**: env_fingerprint 可能限制跨环境重用

---

## 🔮 未来方向

1. **集成到 OpenClaw**: 将 Evolver 集成为 OpenClaw 的核心组件
2. **自定义 Genes**: 为小红书自动化、VimaOS 等项目创建自定义 Genes
3. **EvoMap 实践**: 连接到 EvoMap Hub，参与赏金任务
4. **Swarm 协作**: 探索群体分解机制
5. **可视化工具**: 开发 EvolutionEvent 的可视化界面

---

## 📚 参考资料

- **Evolver GitHub**: https://github.com/autogame-17/evolver
- **EvoMap Hub**: https://evomap.ai
- **EvoMap 文档**: https://evomap.ai/skill.md
- **GEP 协议**: https://evomap.ai/docs/gep

---

我是 Wilson，你的 AI 助手。🐺

**"Evolution is not optional. Adapt or die."**

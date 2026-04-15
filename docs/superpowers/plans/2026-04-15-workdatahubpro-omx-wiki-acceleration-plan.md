# WorkDataHubPro OMX Wiki Acceleration Plan

> 状态：Proposed
> 日期：2026-04-15
> 目标：在不改变 `docs/system/` 与 `docs/wiki-bi/` 权威边界的前提下，使用 `oh-my-codex` 加速知识检索、round 执行与 wiki 维护。

## 1. 结论先行

对当前机器，推荐默认运行环境是 `WSL2 / Ubuntu`，不是原生 Windows。

原因有三点：

- 官方 README 明确说明 OMX 的推荐默认路径是 `macOS or Linux with Codex CLI`，Windows 是次级路径，Windows-hosted setup 也优先推荐 `WSL2`
- 当前机器已经具备可用的 `WSL2 / Ubuntu`
- 当前机器的 WSL 内 `tmux` 已存在，更适合作为 OMX team/runtime 的默认承载环境

同时要保持下面这条边界不变：

- `docs/system/` 与 `docs/wiki-bi/` 继续是仓库内可提交的知识权威层
- `.omx/wiki/` 只作为本地加速层、检索层、session 工作记忆层，不反客为主

## 2. 当前环境核验结果

本轮已在当前机器上做过最小核验。

### 2.1 WSL2 状态

PowerShell:

```powershell
wsl.exe --status
wsl.exe -l -v
```

已确认：

- 默认发行版：`Ubuntu`
- 默认 WSL 版本：`2`
- 已安装的发行版中 `Ubuntu` 为 `VERSION 2`

### 2.2 Windows 侧状态

PowerShell:

```powershell
node -v
npm -v
codex --version
omx --version
```

本机结果：

- `node`: `v22.19.0`
- `npm`: `10.9.3`
- `codex`: `codex-cli 0.120.0`
- `omx`: 未安装

### 2.3 WSL2 侧状态

PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash -lc "node -v"
wsl.exe -d Ubuntu -- bash -lc "npm -v"
wsl.exe -d Ubuntu -- bash -lc "tmux -V"
wsl.exe -d Ubuntu -- bash -lc "which -a codex || true"
wsl.exe -d Ubuntu -- bash -lc "which -a npm || true"
```

本机结果：

- `node`: `v22.17.0`
- `npm`: `10.9.2`
- `tmux`: `3.2a`
- `omx`: 未安装
- `codex` 当前错误地命中 Windows 路径：`/mnt/c/nvm4w/nodejs/codex`

这意味着：

- WSL2 已经具备运行 OMX 的基础条件
- 但 WSL2 里的 `codex` 仍需安装 Linux 版，不能继续借用 Windows 全局包

### 2.4 仓库可从 WSL2 直接访问

PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash -lc "cd /mnt/e/Projects/WorkDataHubPro && git status -sb"
```

已确认当前仓库可从 WSL 路径 `/mnt/e/Projects/WorkDataHubPro` 直接进入。

## 3. 采用策略

推荐的 OMX 采用策略如下：

### 3.1 默认运行面

- 默认：`WSL2 / Ubuntu`
- 仅保留 Windows 作为启动入口、文件浏览入口、WSL 调度入口
- 不默认采用 Windows 原生 `psmux` 路径

### 3.2 知识分层

- durable truth：`docs/system/`、`docs/wiki-bi/`
- local acceleration：`.omx/wiki/`
- session/runtime state：`.omx/` 其他内容

### 3.3 工作方式

- 先把高价值权威页镜像到 `.omx/wiki/`
- 再用 `omx wiki query`、`omx explore`、`$deep-interview`、`$ralplan`、`$ralph` 加速 round
- 所有稳定结论仍需人工回写到 `docs/wiki-bi/`

## 4. 安装前检查命令

先从 Windows PowerShell 跑一轮预检。

```powershell
wsl.exe --status
wsl.exe -l -v
wsl.exe -d Ubuntu -- bash -lc "node -v && npm -v && tmux -V"
wsl.exe -d Ubuntu -- bash -lc "which -a codex || true"
wsl.exe -d Ubuntu -- bash -lc "cd /mnt/e/Projects/WorkDataHubPro && git status -sb"
```

预期判断标准：

- `Ubuntu` 存在且是 `VERSION 2`
- `node` 与 `npm` 可用
- `tmux` 可用
- 仓库路径 `/mnt/e/Projects/WorkDataHubPro` 可进入

如果 `which -a codex` 仍只显示 `/mnt/c/...` 路径，不要直接开始装 OMX，先修复 WSL 内的 Codex CLI。

## 5. WSL2 作为默认环境的安装步骤

以下步骤在 `Ubuntu` 中执行。

### 5.1 进入仓库

Windows PowerShell:

```powershell
wsl.exe -d Ubuntu -- bash -lc "cd /mnt/e/Projects/WorkDataHubPro && pwd"
```

或直接进入交互式 shell：

```powershell
wsl.exe -d Ubuntu
```

然后在 WSL 中：

```bash
cd /mnt/e/Projects/WorkDataHubPro
```

### 5.2 修正 WSL 内的全局 npm 安装路径

当前 WSL 会错误命中 Windows 的 `codex`。先给 WSL 配自己的 npm global bin。

```bash
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
grep -q 'npm-global/bin' ~/.bashrc || printf '\nexport PATH="$HOME/.npm-global/bin:$PATH"\n' >> ~/.bashrc
export PATH="$HOME/.npm-global/bin:$PATH"
hash -r
```

可立即检查：

```bash
npm config get prefix
echo "$PATH" | tr ':' '\n' | sed -n '1,12p'
which -a npm || true
which -a codex || true
```

预期：

- `npm config get prefix` 指向 `~/.npm-global`
- 后续安装完成后，`codex` 与 `omx` 应优先落在 `~/.npm-global/bin/`

### 5.3 在 WSL 内安装 Linux 版 Codex CLI 和 OMX

```bash
npm install -g @openai/codex oh-my-codex
hash -r
which codex
which omx
codex --version
omx --version
```

预期：

- `which codex` 不再指向 `/mnt/c/...`
- `which omx` 指向 `~/.npm-global/bin/omx` 或其他 Linux 本地路径

如果 `which codex` 仍指向 `/mnt/c/...`，先执行：

```bash
hash -r
exec bash -l
which codex
```

如果问题依旧存在，再考虑下面这个更强的可选修复：

```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[interop]
appendWindowsPath=false
EOF
```

然后回到 Windows PowerShell：

```powershell
wsl.exe --shutdown
```

再重新进入 WSL，重复安装与检查。这个修复会影响 WSL 对 Windows PATH 的自动继承，只在前述步骤仍无法让 Linux 版 `codex` 优先生效时使用。

### 5.4 在仓库内执行 OMX 初始化

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx setup
omx doctor
```

注意：

- 官方文档说明 `omx setup` 会安装 prompts、skills、`AGENTS` scaffolding、`.codex/config.toml` 与 `.codex/hooks.json`
- 本仓库当前已经存在 `AGENTS.md` 和受控的 `.codex/skills/`
- 因此第一次执行后必须立即检查变更

建议紧跟一轮检查：

```bash
git status -sb
git diff -- AGENTS.md .codex
```

## 6. WorkDataHubPro 的 OMX wiki 设计

### 6.1 不要把 `.omx/wiki/` 当成正式 wiki

官方 `wiki-feature.md` 已明确：

- wiki 数据位于 `.omx/wiki/`
- 它是 local project state
- 它不是 source-controlled product code

因此对 `WorkDataHubPro`：

- `docs/wiki-bi/` 负责 durable knowledge
- `.omx/wiki/` 负责高频检索与 session 注入

### 6.2 建议的首批种子页

优先放入 `.omx/wiki/` 的不是全量文档，而是最能回答高频问题的入口页。

推荐首批种子：

- `docs/system/index.md`
- `docs/system/document-authority-model.md`
- `docs/wiki-bi/index.md`
- `docs/wiki-bi/log.md`
- `docs/wiki-bi/_meta/wiki-design.md`
- `docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md`
- `docs/wiki-bi/standards/input-reality/input-reality-contracts.md`
- `docs/wiki-bi/standards/output-correctness/output-correctness.md`
- `docs/wiki-bi/standards/semantic-correctness/identity-governance.md`
- `docs/wiki-bi/standards/verification-method/real-data-validation.md`
- `docs/wiki-bi/evidence/status-and-snapshot-evidence.md`
- `docs/wiki-bi/evidence/verification-assets-evidence.md`
- `docs/wiki-bi/evidence/operator-and-surface-evidence.md`
- `docs/wiki-bi/domains/annuity-performance.md`
- `docs/wiki-bi/domains/annual-award.md`
- `docs/wiki-bi/domains/annual-loss.md`
- `docs/wiki-bi/domains/annuity-income.md`

这些页足够支撑：

- authority routing
- domain 入口
- verification / evidence 高频查询
- 下一轮 wiki maintenance 的起点判定

## 7. 种子同步命令

以下命令在 WSL 中执行。

### 7.1 首次镜像 durable seeds 到 `.omx/wiki/`

```bash
cd /mnt/e/Projects/WorkDataHubPro
mkdir -p .omx/wiki/workdatahubpro
cp --parents \
  docs/system/index.md \
  docs/system/document-authority-model.md \
  docs/wiki-bi/index.md \
  docs/wiki-bi/log.md \
  docs/wiki-bi/_meta/wiki-design.md \
  docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md \
  docs/wiki-bi/standards/input-reality/input-reality-contracts.md \
  docs/wiki-bi/standards/output-correctness/output-correctness.md \
  docs/wiki-bi/standards/semantic-correctness/identity-governance.md \
  docs/wiki-bi/standards/verification-method/real-data-validation.md \
  docs/wiki-bi/evidence/status-and-snapshot-evidence.md \
  docs/wiki-bi/evidence/verification-assets-evidence.md \
  docs/wiki-bi/evidence/operator-and-surface-evidence.md \
  docs/wiki-bi/domains/annuity-performance.md \
  docs/wiki-bi/domains/annual-award.md \
  docs/wiki-bi/domains/annual-loss.md \
  docs/wiki-bi/domains/annuity-income.md \
  .omx/wiki/workdatahubpro
```

然后刷新 OMX wiki：

```bash
omx wiki refresh --json
omx wiki list --json
omx wiki lint --json
```

### 7.2 每轮 round 的热页增量同步

当某一轮只涉及少数页面时，不要重灌整个 `.omx/wiki/`，只同步热页。

示例：

```bash
cd /mnt/e/Projects/WorkDataHubPro
cp --parents \
  docs/wiki-bi/domains/annuity-income.md \
  docs/wiki-bi/evidence/annuity-income-gap-evidence.md \
  docs/wiki-bi/evidence/annuity-income-field-processing-evidence.md \
  docs/wiki-bi/log.md \
  .omx/wiki/workdatahubpro
omx wiki refresh --json
```

### 7.3 查询示例

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx wiki query --input '{"query":"当前 accepted replay protection story 是什么"}' --json
omx wiki query --input '{"query":"annuity_income 当前 active runtime path 与 compatibility inventory 的边界"}' --json
omx wiki query --input '{"query":"reference_sync 在 current accepted runtime 中的替代关系是什么"}' --json
```

### 7.4 检索与代码证据联合使用

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx explore --prompt "find current tests and specs proving the accepted runtime for reference_sync"
omx explore --prompt "find current repo evidence for annuity_income operator artifacts"
```

## 8. 推荐的 OMX 工作流

### 8.1 启动

WSL:

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx --madmax --high
```

如果你明确想把 leader session 放进 tmux：

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx --tmux --madmax --high
```

### 8.2 适配本仓库的 wiki maintenance 使用方式

进入 OMX 交互会话后，优先把它当作“加速执行器”，不是新的真相来源。

推荐提示词：

```text
$deep-interview "针对 WorkDataHubPro 的 docs/wiki-bi，本轮先澄清应该升级哪个 durable page，以及哪些 legacy raw sources 真正需要进入分析范围"
$ralplan "基于当前 wiki-domain-upgrade framework，为本轮 wiki maintenance 生成一个窄范围执行计划，要求不创建重复 summary page，并且必须回写 index/log"
$ralph "执行刚批准的 wiki maintenance 计划；先复用现有 docs/wiki-bi 页面，再按需要补充 evidence 和 cross-links，最后给出需要人工晋升回 durable wiki 的稳定结论"
```

当 round 足够大时再用 team：

```text
$team 3:executor "并行完成本轮 wiki maintenance：legacy source 分类、evidence page 整理、target page writeback；禁止把 working trace 直接写进 durable wiki"
```

## 9. 检查与验收命令

### 9.1 OMX 安装验收

WSL:

```bash
cd /mnt/e/Projects/WorkDataHubPro
which codex
which omx
codex --version
omx --version
omx doctor
```

### 9.2 Wiki 加速层验收

WSL:

```bash
cd /mnt/e/Projects/WorkDataHubPro
omx wiki list --json
omx wiki lint --json
omx wiki query --input '{"query":"document authority model"}' --json
```

### 9.3 仓库副作用检查

WSL:

```bash
cd /mnt/e/Projects/WorkDataHubPro
git status -sb
git diff -- AGENTS.md .codex .gitignore
```

建议验收标准：

- `codex` 与 `omx` 都来自 WSL 本地路径
- `omx doctor` 无阻断性错误
- `omx wiki query` 能命中 `.omx/wiki/` 中的种子页
- 没有出现意外覆盖 `AGENTS.md` 或仓库受控技能目录的情况

## 10. 风险与保护措施

### 10.1 `.omx/` 当前尚未在 `.gitignore` 中声明

当前仓库 `.gitignore` 已忽略 `.serena/`、`.worktrees/`，但还没有显式忽略 `.omx/`。

这意味着：

- 第一次启用 OMX 后，`.omx/` 可能进入 `git status`
- 若团队不希望提交本地 OMX state，应先做一次仓库级裁决，再决定是否把 `.omx/` 加入 `.gitignore`

本计划不在本轮直接改 `.gitignore`，但强烈建议在正式长期采用前处理这件事。

### 10.2 不要让 `.omx/wiki/` 取代 `docs/wiki-bi/`

禁止把下列内容直接视为 durable truth：

- session-log pages
- 临时 query 综合
- working trace
- 未经人工裁决的 agent synthesis

这些内容只能作为：

- 检索加速
- round 草稿
- 待晋升结论候选

### 10.3 不要一上来就重度使用 team runtime

当前最稳的落地顺序是：

1. 先修好 WSL 内的 `codex`
2. 安装 `omx`
3. 跑 `omx setup` 和 `omx doctor`
4. 先只使用 `omx wiki query`、`omx explore`、`$deep-interview`、`$ralplan`
5. 确认收益后再进入 `$team`

## 11. 最小执行清单

如果你现在只想按最短路径把 OMX 跑起来，执行下面这一组命令即可。

### 11.1 Windows PowerShell

```powershell
wsl.exe --status
wsl.exe -l -v
wsl.exe -d Ubuntu -- bash -lc "cd /mnt/e/Projects/WorkDataHubPro && node -v && npm -v && tmux -V && git status -sb"
```

### 11.2 WSL / Ubuntu

```bash
cd /mnt/e/Projects/WorkDataHubPro
mkdir -p ~/.npm-global
npm config set prefix ~/.npm-global
grep -q 'npm-global/bin' ~/.bashrc || printf '\nexport PATH="$HOME/.npm-global/bin:$PATH"\n' >> ~/.bashrc
export PATH="$HOME/.npm-global/bin:$PATH"
hash -r
npm install -g @openai/codex oh-my-codex
hash -r
which codex
which omx
codex --version
omx --version
omx setup
omx doctor
mkdir -p .omx/wiki/workdatahubpro
cp --parents \
  docs/system/index.md \
  docs/system/document-authority-model.md \
  docs/wiki-bi/index.md \
  docs/wiki-bi/log.md \
  docs/wiki-bi/_meta/wiki-design.md \
  docs/wiki-bi/_meta/wiki-domain-upgrade-framework.md \
  docs/wiki-bi/evidence/status-and-snapshot-evidence.md \
  docs/wiki-bi/evidence/verification-assets-evidence.md \
  docs/wiki-bi/evidence/operator-and-surface-evidence.md \
  .omx/wiki/workdatahubpro
omx wiki refresh --json
omx wiki query --input '{"query":"document authority model"}' --json
git status -sb
```

## 12. 参考来源

- OMX README: `https://github.com/Yeachan-Heo/oh-my-codex`
- OMX Getting Started: `https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/getting-started.html`
- OMX Wiki docs: `https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/wiki-feature.md`

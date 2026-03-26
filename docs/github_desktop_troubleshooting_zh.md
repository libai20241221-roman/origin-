# GitHub Desktop 报错：`can't find "7-Zip 9.20 ..."` 处理说明

你这个报错**反复在“重新克隆后”出现**，通常说明问题不在仓库代码，而在**本机持久化配置**：
- Git 配置（`core.editor` / `diff.tool` / `merge.tool`）
- GitHub Desktop 自身 `settings.json`（External editor / Shell 路径）

只要这些配置没被清掉，换仓库克隆也会继续报错。

## 先解决你现在这个报错（No such file or directory）

你贴的日志是：找不到 `scripts/fix_github_desktop_7zip_error.py`。这通常是以下两种情况：
1. 当前目录不是这个仓库根目录。
2. 本地仓库还没拉到最新提交（脚本文件还不存在）。

请先执行：

```bash
# Windows CMD
cd /d D:\Users\Administrator\Documents\origin-
dir

# 需要看到 scripts 目录和 fix_github_desktop_7zip_error.py（根目录启动器）
```

如果没看到，请更新：

```bash
git pull
```

## 一键修复（推荐）

在仓库根目录执行（推荐这个，不容易输错路径）：

```bash
python fix_github_desktop_7zip_error.py --dry-run
python fix_github_desktop_7zip_error.py
```

脚本会做两件事：
1. 扫描并清理 Git 配置中包含 `7-Zip` 的坏路径。
2. 扫描并清理 GitHub Desktop `settings.json` 中包含 `7-Zip` 的字段（并自动备份 `.bak`）。

## 手工兜底（如果你不想跑脚本）

### 1) GitHub Desktop 内修改
- 打开：`File -> Options -> Integrations`
- 把 **External editor** 改成可用编辑器（如 VS Code）
- 把 **Shell** 改成 Git Bash / PowerShell（不要指向失效路径）

### 2) 清理 Git 全局配置

```bash
git config --global --unset-all core.editor
git config --global --unset-all diff.tool
git config --global --unset-all merge.tool
```

> `--system` 级配置可能需要管理员权限。

## 为什么会“每次克隆都报错”

因为错误配置在**全局环境**里，而不是某个单独仓库里。新克隆仓库时 GitHub Desktop 仍会读取同一套坏配置，所以会重复弹窗。

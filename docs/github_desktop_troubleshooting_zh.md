# GitHub Desktop 报错：`can't find "7-Zip 9.20 ..."` 处理说明

你这个报错**反复在“重新克隆后”出现**，通常说明问题不在仓库代码，而在**本机持久化配置**：
- Git 配置（`core.editor` / `diff.tool` / `merge.tool`）
- GitHub Desktop 自身 `settings.json`（External editor / Shell 路径）

只要这些配置没被清掉，换仓库克隆也会继续报错。

---

## 你当前这条报错的直接原因

你现在看到的是：

```text
python ... can't open file ...\fix_github_desktop_7zip_error.py: [Errno 2] No such file or directory
```

这表示**当前这个仓库目录里没有该脚本文件**。最常见原因：
1. 你拉取的是不含该脚本的分支/提交（比如 PR 还没合并到你当前分支）。
2. 当前目录不是你以为的那个仓库根目录。

先确认：

```bash
cd /d D:\Users\Administrator\Documents\origin-
dir
```

如果目录里看不到 `fix_github_desktop_7zip_error.py`，说明本地仓库本身就没有这个文件（不是 Python 问题）。

---

## 不依赖仓库脚本的“立即修复”方案（推荐你先用这个）

在 CMD 里直接执行下面三条（可立即生效）：

```bash
git config --global --unset-all core.editor
git config --global --unset-all diff.tool
git config --global --unset-all merge.tool
```

然后打开这个文件（若存在）：

```text
%APPDATA%\GitHub Desktop\settings.json
```

把里面包含 `7-Zip` 的路径删掉（常见在 external editor / shell 相关字段），保存后重启 GitHub Desktop。

---

## 一键修复（当仓库里有脚本时）

在仓库根目录执行：

```bash
python fix_github_desktop_7zip_error.py --dry-run
python fix_github_desktop_7zip_error.py
```

脚本会做两件事：
1. 扫描并清理 Git 配置中包含 `7-Zip` 的坏路径。
2. 扫描并清理 GitHub Desktop `settings.json` 中包含 `7-Zip` 的字段（并自动备份 `.bak`）。

---

## 为什么会“每次克隆都报错”

因为错误配置在**全局环境**里，而不是某个单独仓库里。新克隆仓库时 GitHub Desktop 仍会读取同一套坏配置，所以会重复弹窗。

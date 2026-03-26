# GitHub Desktop 报错：`can't find "7-Zip 9.20 ..."` 处理说明

这个报错通常不是本仓库代码问题，而是**本机 Git/GitHub Desktop 配置**里某个工具路径损坏（常见于 editor/difftool/mergetool 被写成了无效的 7-Zip 路径）。

## 快速修复步骤（Windows）

1. 在仓库根目录打开终端（PowerShell / Git Bash）。
2. 先做检测（不改动）：

```bash
python scripts/fix_github_desktop_7zip_error.py --dry-run
```

3. 确认有异常项后，执行清理：

```bash
python scripts/fix_github_desktop_7zip_error.py
```

4. 重启 GitHub Desktop。

## 如果仍报错

请在 GitHub Desktop 里检查：
- `File -> Options -> Integrations` 中的 **External editor** 和 **Shell**。
- 若路径异常，改为 `Visual Studio Code`（或你已安装的编辑器）。

## 手工命令（可选）

如果你知道具体坏掉的键，也可以手工执行：

```bash
git config --global --unset-all core.editor
git config --global --unset-all diff.tool
git config --global --unset-all merge.tool
```

> 注意：`--system` 级配置可能需要管理员权限。

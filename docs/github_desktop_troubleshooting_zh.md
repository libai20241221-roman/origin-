# GitHub Desktop 报错：`Can't find "7-Zip 9.20 ..."` 处理说明

你这个报错如果在**最新版、重新克隆后仍出现**，说明问题通常不在仓库代码，而在**本机持久化配置**：
- Git 配置（`core.editor` / `diff.tool` / `merge.tool`）
- GitHub Desktop 用户配置（`settings.json` / Local Storage）

## 一键修复（普通）

在仓库根目录：

```bash
python fix_github_desktop_7zip_error.py --dry-run
python fix_github_desktop_7zip_error.py
```

## 一键修复（强制重置，解决“反复弹窗”）

如果普通模式后仍弹窗，执行：

```bash
python fix_github_desktop_7zip_error.py --dry-run --hard-reset-desktop
python fix_github_desktop_7zip_error.py --hard-reset-desktop
```

强制重置会：
1. 先备份 `%APPDATA%\GitHub Desktop\settings.json / Local Storage / Session Storage`
2. 再移除这些用户配置，避免旧坏路径继续被 GitHub Desktop 读取

## 手工兜底（不依赖脚本）

```bash
git config --global --unset-all core.editor
git config --global --unset-all diff.tool
git config --global --unset-all merge.tool
```

然后手工打开 `%APPDATA%\GitHub Desktop\settings.json`，删掉所有包含 `7-Zip` 的路径，重启 GitHub Desktop。

## 你截图里这类弹窗怎么选

看到 `Locate... / Remove` 时，优先点 **Remove**，把失效引用从系统记录里移除，然后再执行上面的修复流程。

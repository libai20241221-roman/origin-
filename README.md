# origin-
origin绘图转化成漫画手绘风

## 文档
- 使用说明：`docs/usage_zh.md`
- GitHub Desktop 7-Zip 报错修复：`docs/github_desktop_troubleshooting_zh.md`

## 快速开始
```bash
python scripts/generate_handdrawn_palette.py
```

## GitHub Desktop 报错快速修复
如果仓库里没有修复脚本，先用手工命令清理全局配置：
```bash
git config --global --unset-all core.editor
git config --global --unset-all diff.tool
git config --global --unset-all merge.tool
```

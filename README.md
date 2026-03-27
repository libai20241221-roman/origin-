# origin-
origin绘图转化成漫画手绘风

## 文档
- 使用说明：`docs/usage_zh.md`
- EXE 打包与使用：`docs/exe_guide_zh.md`
- GitHub Desktop 7-Zip 报错修复：`docs/github_desktop_troubleshooting_zh.md`

## 快速开始
```bash
python scripts/generate_handdrawn_palette.py
```

## 可点击运行（无需先打包）
```bash
run_origin_style_studio.bat
```

## 可点击运行（EXE 打包）
```bash
scripts\build_origin_style_studio_exe.bat
```

## GitHub Desktop 报错快速修复
```bash
python fix_github_desktop_7zip_error.py --dry-run
python fix_github_desktop_7zip_error.py

# 若仍反复弹窗
python fix_github_desktop_7zip_error.py --hard-reset-desktop
```

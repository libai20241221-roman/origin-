# Origin 柱状图“手绘风”自动上色使用说明

## 你会得到什么
- 一键把当前图页里的柱子换成柔和手绘风色板。
- 图例同步更新，不再需要在 PPT 里手工一个个描色。

## 文件说明
- `origin/handdrawn_bar_palette.ogs`：Origin LabTalk 脚本（直接在 Origin 中运行）。
- `scripts/generate_handdrawn_palette.py`：生成统一色板文件与预览文档。
- `origin/handdrawn_palette.txt`：导出的 RGB 色板。

## 1) 生成色板（可选）
在项目根目录运行：

```bash
python3 scripts/generate_handdrawn_palette.py
```

## 2) 在 Origin 里应用到柱状图
1. 打开你的柱状图页面，并激活该 Graph 窗口。
2. 打开 `Script Window`。
3. 执行：

```labtalk
run.section(origin\\handdrawn_bar_palette, Main);
```

执行后会自动：
- 按色板给每个柱（或每个数据绘图）上色。
- 同步更新图例颜色样式。
- 增加少量透明度和描边粗细，让视觉更接近手绘标记笔效果。

## 3) 自定义色板
在 `origin/handdrawn_bar_palette.ogs` 中修改：

```labtalk
color(1) = rgb(230, 126, 128);
...
```

如果你希望我再加一个“按类别名称固定颜色映射（例如 A 类永远是同一色）”的版本，也可以继续扩展。

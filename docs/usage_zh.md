# Origin 柱状图“手绘风”自动上色使用说明

## 你会得到什么
- 一键把当前图页里的柱子换成柔和手绘风色板。
- 图例同步更新，不再需要在 PPT 里手工一个个描色。

## 文件说明
- `origin/handdrawn_bar_palette.ogs`：Origin LabTalk 脚本（直接在 Origin 中运行）。
- `scripts/generate_handdrawn_palette.py`：生成统一色板文件与预览文档。
- `origin/handdrawn_palette.txt`：导出的 RGB 色板。

## 在 Origin 里应用到柱状图
1. 打开你的柱状图页面，并激活该 Graph 窗口。
2. 打开 `Script Window`。
3. 用绝对路径执行：

```labtalk
run.section("D:\\你的路径\\origin\\handdrawn_bar_palette.ogs", Main);
```

执行时会看到：
- `[handdrawn_bar_palette] applying...`
- `[handdrawn_bar_palette] done.`

## 如果“只有 applying 没有变化”
请按下面检查：
1. 点击图中的某一组柱子，确保当前图层里有激活 plot。
2. 再执行一次脚本。
3. 若是多图层页面，先只保留 1 个图层测试是否生效。
4. 确认图类型是 Bar/Column（线图/散点图视觉变化可能不明显）。

## 自定义色板
在 `origin/handdrawn_bar_palette.ogs` 中修改：

```labtalk
color(1) = rgb(230, 126, 128);
...
```

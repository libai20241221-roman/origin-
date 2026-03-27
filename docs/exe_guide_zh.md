# Origin Style Studio 打包 EXE 与使用说明

## 你会得到什么
- 一个可点击运行的 `OriginStyleStudio.exe`
- 可视化选择风格预设（Marker/Watercolor/Sketch/Comic）
- 自定义：配色、透明度、边框线宽、填充模式
- 一键生成 `.ogs`，并复制 Origin 可执行命令

## 1) 安装打包工具（仅一次）

```bash
pip install pyinstaller
```

## 2) 生成 EXE
在仓库根目录双击或执行：

```bash
scripts\build_origin_style_studio_exe.bat
```

成功后 EXE 在：

```text
dist\OriginStyleStudio.exe
```

## 3) 在 Origin 中应用
1. 打开 `OriginStyleStudio.exe`
2. 选一个风格，调整参数，点击“生成 OGS”
3. 点击“复制 Origin 执行命令”
4. 粘贴到 Origin Script Window 执行

例如：

```labtalk
run.section("D:\\Users\\Administrator\\Documents\\origin-\\origin\\style_studio_custom.ogs", Main);
```

## 4) 说明
- 这是“样式生成器”，负责快速产出风格脚本。
- 你可以保存多份 `.ogs`，对应不同期刊/汇报风格。

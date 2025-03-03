# ResizePeon

这是一个用于自动调整图片大小的 Python 脚本，支持：
- 按比例缩小图片，确保最终文件大小不超过 1024KB
- 不限制图片输入类型
- 保持输出文件为 `JPEG` 格式
- 输入和输出文件夹的图片文件会自动重命名为创建时间
- 小于1024KB的图片不会输出，只会变更原图名称为创建时间

## 使用方式
1. 运行 `ResizePeon.py`，第一次运行时需要选择 **输入文件夹** 和 **输出文件夹** 的位置，之后会自动记住保存至 `settings.json`文件。
2. 程序会处理文件夹中的所有图片，并保存到输出文件夹。

## 依赖安装
1. 在运行前，需要安装 `Pillow` 库：

```sh
pip install pillow
```
- 安装后，就可以运行 `ResizePeon.py` 了！

2. 更改输入/输出文件夹

- 如果想要重新设置输入/输出文件夹，删除 `settings.json`，然后重新运行 `ResizePeon.py`，会再次弹出文件夹选择窗口。

## 生成可执行文件
1. 安装pyinstaller
```sh
pip install pyinstaller
```

2. 打包ResizePeon.py脚本文件为windows可执行.exe 文件
```sh
pyinstaller --onefile --noconsole --icon=icon.ico --name=ResizePeon --hidden-import=PIL --clean ResizePeon.py
```
- --onefile：将所有依赖打包成单个 .exe 文件  
- --noconsole：不显示终端窗口（如果需要调试，可以去掉此参数,适用于 GUI 程序）
- --icon=icon.ico：需要是名为 icon.ico 格式的图标，放在脚本同目录下
- --name=ResizePeon：生成的可执行文件命名为 ResizePeon.exe
- --hidden-import=PIL：只包含 PIL（Pillow）库，避免不必要的依赖
- --clean：清除临时文件，减少打包体积

3. 测试可执行文件
- 打开 dist/ 目录，找到 ResizePeon.exe
- 双击运行，检查是否能正确处理图片




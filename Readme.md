# 知识图谱构建工具
DONE:已经近乎完成了一个知识图谱结构的构建
打包命令：pyinstaller --onefile --windowed   --add-data "picture/*;picture/"  --add-data "xml/*;xml/"  --add-data "setitem/*;setitem/" backup.py



另外的打包命令：nuitka --standalone --onefile --enable-plugin=pyqt5 --plugin-enable=numpy --include-package-data=picture --show-memory  --windows-disable-console --show-progress  --output-dir=out --remove-output backup.py
TODO:下一个不同样式的知识图谱模式，注意规范化整个过程
    -箭头样式
    -图元样式
    -切换流程

              2024/5/21
                -song
                -sun
--------
TODO:缩放注意比例(完成)
    -批量转图片
    -资源链接
    -保存更改为到指定文件夹(完成)
    -回退功能(完成)
    -新建应该新建到该目录下而不是temp

            2024/7/8
                -song

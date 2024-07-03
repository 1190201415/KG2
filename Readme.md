# 知识图谱构建工具
DONE:已经近乎完成了一个知识图谱结构的构建
打包命令：pyinstaller --onefile --windowed   --add-data "picture/*;picture/"  --add-data "xml/*;xml/"  --add-data "setitem/*;setitem/" backup.py



另外的打包命令：nuitka --standalone --onefile --enable-plugin=pyqt5 --include-package-data=picture --show-memory --show-progress  --output-dir=out --remove-output backup.py
TODO:下一个不同样式的知识图谱模式，注意规范化整个过程
    -箭头样式
    -图元样式
    -切换流程

              2024/5/21
                -song
                -sun
--------
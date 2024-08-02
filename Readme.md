# 知识图谱构建工具
DONE:已经近乎完成了一个知识图谱结构的构建
打包命令：pyinstaller --onefile --windowed   --add-data "picture/*;picture/"  --add-data "xml/*;xml/"  --add-data "setitem/*;setitem/" backup.py


少一个视频解码器
另外的打包命令：nuitka --standalone --onefile --enable-plugin=pyqt5 --plugin-enable=numpy --include-package-data=picture --show-memory  --windows-disable-console --show-progress  --output-dir=out --remove-output backup.py

nuitka和项目中的一些库可能存在冲突问题，比如在此次项目中用到PyMuPDF，一开始使用的版本为1.2x.x，发现编译时存在问题无法编译，降低PyMuPDF版本到1.18.0得以解决
nuitka --standalone --onefile --show-memory  --windows-disable-console --show-progress  --output-dir= --remove-output runbat.py

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
    -新建应该新建到该目录下而不是temp（）
    -换能力时应该进行保存
    -输入文件名的非法字符()
    -有几个特定的模版
    -回退时，信号应该屏蔽
    -保存或者读入的地方有问题()
    -修改填充（）
    -修改能力图谱初始化内容（）
    -更改资源节点颜色大小

            2024/7/8
                -song
TODO:改节点名称
    -链接名称与顺序
    -链接样式
    -界面美化
    -PPT转图片
    -视频解码器
    -图片模糊
    -节点乱跑
    -选中图谱名
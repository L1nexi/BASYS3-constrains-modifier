BASYS3 引脚锁定文件修改器
------

### 使用方法
将 `main.py` 文件与引脚锁定文件 `Basys3_Master.xdc` 置于同样的目录下，运行 `main.py` 文件。
输入需要重命名的引脚的编号（由 `0` 开始）以及重命名的名字。支持单项修改以及向量修改。
目前只支持 `LEDs` 和 `Switches` 的修改。

``` bash
Input the index of Switches and the new tag. Input 'Done' to finish.
0 1 arr
Handled.
Next one or quit by 'Done'?
2 singel
Handled.
Next one or quit by 'Done'?
Done
```

------
命令行参数：运行 `python main.py -h` 获取。
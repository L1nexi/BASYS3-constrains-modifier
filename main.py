#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import re
import os

# TODO 1: 增加启动参数以决定处理的元件类型

_NUMS_ = {"led": 16, "sw": 16, "seg": 7, "an": 4}
def handleArrLike(name, fin, fout):
    tmpList = []
    global _NUMS_
    for i in range(_NUMS_[name] * 2):
        tmpList.append(fin.readline())
    print("Please input the index of {0} (numbered from 0) and its new tag. Input \'Done\' when finished.".format(name))
    str = input();
    while (str != "Done"):
        index, tag = str.split()
        if int(index) < 0 or int(index) >= _NUMS_[name]:
            print("Invalid index. Please input again or quit by \'Done\'?")
            str = input()
            continue
        targetStr = name + "[{}]".format(index)
        tmpList[2 * int(index)] = re.sub(re.escape(targetStr), tag, tmpList[2 * int(index)])
        tmpList[2 * int(index)] = re.sub("#", "", tmpList[2 * int(index)])
        tmpList[2 * int(index) + 1] = re.sub(re.escape(targetStr), tag, tmpList[2 * int(index) + 1])
        tmpList[2 * int(index) + 1] = re.sub("#", "", tmpList[2 * int(index) + 1])
        print("Handled.\n Next one or quit by \'Done\'?")
        str = input()
    fout.writelines(tmpList)
    

try:
    with open("Basys3_Master.xdc", "r") as fin, open("Basys3_Master_new.xdc", "w", encoding="utf-8") as fout:
        for line in fin:
            if "Switches" in line:
                fout.write(line)
                handleArrLike("sw", fin, fout)
            elif "LEDs" in line:
                fout.write(line)
                handleArrLike("led", fin, fout)
            else:
                fout.write(line)
                
except KeyboardInterrupt:
    print("KeyboardInterrupt")
    exit(0)
    
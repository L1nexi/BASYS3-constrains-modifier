#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import re
import os

# TODO 1: 增加启动参数以决定处理的元件类型
# TODO 2: 支持数组元件的处理

_NUMS_ = {"led": 16, "sw": 16, "seg": 7, "an": 4}
_NAME_ = {"led": "LEDs", "sw": "Switches", "seg": "SEG", "an": "AN"}

def checkIndex(index, name):
    global _NUMS_
    if int(index) < 0 or int(index) >= _NUMS_[name]:
        return False
    return True

def handleArrLike(name, fin, fout):
    global _NUMS_
    tmpList = []

    for i in range(_NUMS_[name] * 2):
        tmpList.append(fin.readline())

    print("Start processing {}...".format(_NAME_[name]))
    print("Input the index of {} and the new tag. Input \'Done\' to finish.".format(_NAME_[name]))
    str = input();
    while (str != "Done"):
        try:
            if str.split().__len__() == 3:
                begin, end, tag = str.split()
                begin = int(begin)
                end = int(end)
            elif str.split().__len__() == 2:
                begin, tag = str.split()
                end = begin = int(begin)
            else:
                print("Invalid input. Please input again or input \'Done\' to finish.")
                str = input()
                continue


            if checkIndex(begin, name) == False or checkIndex(end, name) == False:
                print("Index out of bounds. Please input again or input \'Done\' to finish.?")
                str = input()
                continue

            # begin == end : 单个处理
            if begin == end:
                pattern = name + "[{}]".format(begin)
                tmpList[2 * begin] = re.sub(re.escape(pattern), tag, tmpList[2 * begin])
                tmpList[2 * begin] = re.sub("#", "", tmpList[2 * begin])
                tmpList[2 * begin + 1] = re.sub(re.escape(pattern), tag, tmpList[2 * begin + 1])
                tmpList[2 * begin + 1] = re.sub("#", "", tmpList[2 * begin + 1])
            
            # begin <= end : 按数组处理

            elif int(begin) < int(end):
                j = 0
                for i in range(begin, end + 1):
                    pattern = name + "[{}]".format(i)
                    arrTag = tag + "[{}]".format(j)
                    tmpList[2 * i] = re.sub(re.escape(pattern), arrTag, tmpList[2 * i])
                    tmpList[2 * i] = re.sub("#", "", tmpList[2 * i])
                    tmpList[2 * i + 1] = re.sub(re.escape(pattern), arrTag, tmpList[2 * i + 1])
                    tmpList[2 * i + 1] = re.sub("#", "", tmpList[2 * i + 1])
                    j += 1

            else :
                j = 0;
                for i in range(begin, end - 1, -1):
                    pattern = name + "[{}]".format(i)
                    arrTag = tag + "[{}]".format(j)
                    tmpList[2 * i] = re.sub(re.escape(pattern), arrTag, tmpList[2 * i])
                    tmpList[2 * i] = re.sub("#", "", tmpList[2 * i])
                    tmpList[2 * i + 1] = re.sub(re.escape(pattern), arrTag, tmpList[2 * i + 1])
                    tmpList[2 * i + 1] = re.sub("#", "", tmpList[2 * i + 1])
                    j += 1

            print("Handled.\nNext one or quit by \'Done\'?")
            str = input()

        except ValueError:
            print("Invalid input. Please input again or input \'Done\' to finish.")
            str = input()
            continue
    fout.writelines(tmpList)
    

try:
    with open("E:\\github\\BASYS3-constrains-modifier\\Basys3_Master.xdc", "r") as fin, open("E:\\github\\BASYS3-constrains-modifier\\Basys3_Master_new.xdc", "w", encoding="utf-8") as fout:
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
    
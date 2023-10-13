#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import re
import os
import argparse

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

def handleArg():
    parser = argparse.ArgumentParser(description="Modify constrains file for BASYS3")
    parser.add_argument("-i", "--input", default="Basys3_Master.xdc", help="Input file name. Stored as text.")
    parser.add_argument("-o", "--output", default="Basys3_Master_new.xdc", help="Output file name.")
    parser.add_argument("-L","--LED", help="Add LEDs to the handling lists.", action="store_true")
    parser.add_argument("-sw", "--switch", help="Add switches to the handling lists.", action="store_true")
    arg = parser.parse_args()
    return arg

def generateList(arg):
    procFlag = False
    procFlag = procFlag | arg.LED | arg.switch
    procFlag = not procFlag;
    list = []
    if (procFlag == True):
        list = ["sw", "led"]
    else:
        if arg.switch:
            list.append("sw")
        if arg.LED:
            list.append("led")
    return list

def main():
    global _NAME_
    arg = handleArg()
    list = generateList(arg)

    try:
        j = 0
        with open(arg.input, "r", encoding="utf-8") as fin, open(arg.output, "w", encoding="utf-8") as fout:
            curTarget = _NAME_[list[j]]
            for line in fin:
                if j < list.__len__() and curTarget in line:
                    fout.write(line)
                    handleArrLike(list[j], fin, fout)
                    j += 1
                    if j < list.__len__():
                        curTarget = _NAME_[list[j]]

                else:
                    fout.write(line)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit(0)

if __name__ == "__main__":
    main()
        
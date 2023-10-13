import re
import os
import argparse

__NUMS__ = {"led": 16, "sw": 16, "seg": 7, "an": 4}
__NAME__ = {"led": "LEDs", "sw": "Switches", "seg": "SEG", "an": "AN"}

def checkIndex(index, name):
    global __NUMS__
    if int(index) < 0 or int(index) >= __NUMS__[name]:
        return False
    return True

def handleArrLike(name, fin, fout):
    global __NUMS__
    tmpList = []

    for i in range(__NUMS__[name] * 2):
        tmpList.append(fin.readline())

    print("Start processing {}...".format(__NAME__[name]))
    print("Input the index of {} and the new tag. Input \'Done\' to finish.".format(__NAME__[name]))
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
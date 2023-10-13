#!/usr/bin/python
# -*- coding: UTF-8 -*- 
import os
import constrains_modify as cm

def main():
    arg = cm.handleArg()
    list = cm.generateList(arg)
    

    try:
        j = 0
        with open(arg.input, "r", encoding="utf-8") as fin, open(arg.output, "w", encoding="utf-8") as fout:
            curTarget = cm.__NAME__[list[j]]
            for line in fin:
                if j < list.__len__() and curTarget in line:
                    fout.write(line)
                    cm.handleArrLike(list[j], fin, fout)
                    j += 1
                    if j < list.__len__():
                        curTarget = cm.__NAME__[list[j]]

                else:
                    fout.write(line)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit(0)

if __name__ == "__main__":
    main()
        
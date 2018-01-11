# coding: utf-8
import glob
import math
import csv
import numpy as np
import pandas as pd
import itertools
import sys

"""
重心のxvgファイルからxy座標のみ取得
各時間のxy座標を配列にして返す
"""
def fetchLine():

    allFiles = glob.glob('*.xvg')
    counter = 0
    for file in allFiles:
        data = np.loadtxt(file)
        if counter == 0:
            datas = np.delete(data, [0, 3], 1)
        else:
            xydata = np.delete(data, [0, 3], 1)
            datas = np.append(datas, xydata, axis=1)
        counter += 1
        print 'file number :', counter

    rdatas = datas.reshape(datas.shape[0], datas.shape[1]/2, 2)
    return rdatas[range(1, tmax, dt),:]

"""
rdf計算
"""
def getRdf(xydatas, particlesNum, times):

    hist = np.zeros((times, int(diag/dr)))
    for time in range(0, times):
        print 'calculate distanses time:', time
        for i in range(0, particlesNum-1):
            for j in range(i+1, particlesNum):
                x1 = xydatas[time][i][0]
                x2 = xydatas[time][j][0]
                y1 = xydatas[time][i][1]
                y2 = xydatas[time][j][1]
                dx = (x1 - x2) - round((x1 - x2)/xsize)*xsize
                dy = (y1 - y2) - round((y1 - y2)/ysize)*ysize
                d = math.sqrt(dx**2 + dy**2)
                hist[time][int(d/dr)] += 1
    hist = np.delete(2 * hist, range(150,216), 1)
    aveHist = np.mean(hist, axis=0) / particlesNum
    print(len(aveHist))
    r = 0
    rd = []
    gr = []
    allDensity = particlesNum / (xsize**2)
    print 'get rdf'
    for n in aveHist:
        rInner = r
        rOuter = r + dr
        drDensity = n / (math.pi * (rOuter**2 - rInner**2))
        gr.append(drDensity / allDensity)
        rd.append(r)
        r += dr

    return pd.Series(gr, rd)

#main
argv = sys.argv
if len(argv) == 3:
    xsize = 30.0
    ysize = 30.0
    diag  = 21.6
    dr    = 0.1
    dt    = int(argv[1])
    tmax  = int(argv[2])
else:
    print("引数を入力してください")
    sys.exit()

xydatas = fetchLine()
particlesNum = xydatas.shape[1]
times = xydatas.shape[0]
gr = getRdf(xydatas, particlesNum, times)
print('end! check rdf.csv')
gr.to_csv("gr.csv")

import os
import linecache
import shutil
import sys
from collections import OrderedDict

#check lipid type from system.top data
def lipid_type(filenum):
    lipids = {"PPC": 192, "PPS": 256, "DPPC": 320, "PGPC": 448, "PIPC": 640, "POPC": 832, "PUPC": 896, "DOPE": 960, "PAPE": 1088, "PIPE": 1152, "PRPE": 1344, "PAPI": 1408, "PAPS": 1536, "PRPS": 1728, "BNSM": 1856, "DBSM": 2048, "DPSM": 2240, "DXSM": 2304, "CHOL": 4096}
    lipids = OrderedDict(sorted(lipids.items(), key=lambda x:x[1]))

    for lipid, lipidnum in lipids.items():
        if filenum <= lipidnum:
            lipidType = lipid
            break;

    return lipidType

#get initial zaxis from xvg file
def getZaxis(fileName):
    firstLine = linecache.getline(fileName, 1)
    firstLine = firstLine.replace(' ', ',')
    arrayLine = firstLine.split(',')
    zaxis = arrayLine[3].replace("\n", "")
    return float(zaxis)

#main
for filenum in range(3,4097):
    xvgfile = "r_"+str(filenum)+".xvg"

    zaxis = getZaxis(xvgfile)
    lipidType = lipid_type(filenum)
    lipidSide = "upper" if zaxis >= 6.10201 else "lower"
    nextpath = lipidSide+"/"+lipidType

    if not os.path.isdir(nextpath):
        os.mkdir(nextpath)

    shutil.copy(xvgfile, nextpath)

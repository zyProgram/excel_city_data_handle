# coding=utf-8
import os
from CommonDefine.Company import CompanyManager
from CommonDefine.ExcelOperator import ExcelOperator




if __name__ == '__main__':
    data2006Dir = "/home/zy123/Desktop/excel/2006"
    data2019Dir = "/home/zy123/Desktop/excel/2019"
    output2006Dir = "/home/zy123/Desktop/excel/output/2016"
    output2019Dir = "/home/zy123/Desktop/excel/output/2019"
    files2006 = os.listdir(data2006Dir)
    files2019 = os.listdir(data2019Dir)

    lele = ExcelOperator()

    for file in files2006:
        print("file:%s\n"%(file))
        lele.read_excel(data2006Dir+"/"+file,data2006Dir+"/out/"+file)


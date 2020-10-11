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
    if not os.path.exists(output2006Dir):
        os.makedirs(output2006Dir)
    if not os.path.exists(output2019Dir):
        os.makedirs(output2019Dir)
    lele = ExcelOperator()
    ExcelOperator.preProcess(lele,"/home/zy123/PycharmProjects/excel_handle/data/研究对象 城市汇总4.xlsx")
    for file in files2006:
        print("file:%s\n"%(file))
        lele.read_excel(data2006Dir+"/"+file,output2006Dir+"/"+file)

    for file in files2019:
        print("file:%s\n"%(file))
        lele.read_excel(data2019Dir+"/"+file,output2019Dir+"/"+file)

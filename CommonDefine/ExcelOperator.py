import xlrd  # 读模块
import xlsxwriter  # 写模块
import os

from CommonDefine.Company import CompanyManager
from CommonDefine.City import CityManager


class ExcelOperator():
    def __init__(self):
        self.companysManagers = dict()
        self.citysManagers = dict()
        self.matrixSheets = dict()
        self.replaceCityDicts = dict()
    @staticmethod
    def preProcess(operator,excelName):
        data = xlrd.open_workbook(excelName)
        sh2006 = data.sheet_by_name(u'2006无城市坐标')  # 表名法
        sh2019 = data.sheet_by_name(u'2019无城市坐标')  # 表名法
        totalRow = sh2006.nrows
        change = 0
        for row in range(2, totalRow):
            origin = sh2006.cell_value(row,0)
            replace = sh2006.cell_value(row,1)
            origin = origin.strip()
            if "改为" in replace:
                replace = replace.lstrip("改为").strip()
                operator.replaceCityDicts[origin] = replace
                change +=1
        print("change city name in 2006 is %d\n"%change)
        change = 0
        totalRow = sh2019.nrows
        for row in range(2, totalRow):
            origin = sh2019.cell_value(row, 0)
            replace = sh2019.cell_value(row, 1)
            origin = origin.strip()
            if "改为" in replace:
                replace = replace.lstrip("改为").strip()
                operator.replaceCityDicts[origin] = replace
                change+=1
        print("change city name in 2019 is %d\n" % change)



    def __replace_city_name(self,cityName):
        if cityName in self.replaceCityDicts:
            return self.replaceCityDicts[cityName]
        else:
            return cityName

    def startAssignMatrix(self, excelName):
        cityManager = self.citysManagers[excelName]
        companyManager = self.companysManagers[excelName]
        dict = cityManager.cityDict
        for (cityName, city) in dict.items():
            for (companyName, score) in city.companyScoreMap.items():
                if score == 1:
                    city.companyScoreMap[companyName] = companyManager.companyDict[companyName].masterScore
                else:
                    city.companyScoreMap[companyName] = companyManager.companyDict[companyName].branchScore

    def read_excel(self, excelName, output):
        if excelName in self.citysManagers:
            raise Exception("the %s is already been counted!!!")
        self.before_write(excelName, output)
        cityManager = CityManager(excelName)
        companyManager = CompanyManager(excelName)

        if not os.path.isdir(excelName):
            data = xlrd.open_workbook(excelName)
            sh = data.sheet_by_name(u'源数据')  # 表名法

            totalRow = sh.nrows
            for row in range(2, totalRow):
                companyName = sh.cell_value(row, 0)
                cityName = sh.cell_value(row, 1)
                cityName = self.__replace_city_name(cityName)

                isMater = True if sh.cell_value(row, 3) == 1 else False
                companyManager.push_back(companyname=companyName, city=cityName, ismaster=isMater)
                cityManager.push_back(cityName, companyName, isMater)
            self.citysManagers[excelName] = cityManager
            self.companysManagers[excelName] = companyManager
            self.startAssignMatrix(excelName)
            # cityManager.show()
            self.before_write(excelName,output)
            self.writeMatrix(excelName)
            self.after_write(excelName)
        else:  # is dir such as /2016
            pass

    def before_write(self, filename, output):
        workboot = xlsxwriter.Workbook(output)
        d = dict()
        d["workboot"] = workboot
        d["AssignMatrix"] = workboot.add_worksheet("AssignMatrix")
        d["CDCFullMatrix"] = workboot.add_worksheet("CDCFullMatrix")
        d["CDCTrialAngelMatrix"] = workboot.add_worksheet("CDCTrialAngelMatrix")
        d["GNCMatrix"] = workboot.add_worksheet("GNCMatrix")
        d["CDRTrialAngelMatrix"] = workboot.add_worksheet("CDRTrialAngelMatrix")
        d["CDRFullMatrix"] = workboot.add_worksheet("CDRFullMatrix")
        self.matrixSheets[filename] = d

    def writeAssignMatrix(self, filename):
        allMatrix = self.matrixSheets[filename]
        assignSheet = allMatrix["AssignMatrix"]
        cityManager = self.citysManagers[filename]
        companyManager = self.companysManagers[filename]
        cityColIndexDict = dict()
        col = 1
        for (cityname, city) in cityManager.cityDict.items():
            assignSheet.write(0, col, cityname)
            cityColIndexDict[cityname] = col
            col += 1
        row = 1
        for (companyname, company) in companyManager.companyDict.items():
            if -1 == assignSheet.write(row, 0, companyname):
                print("error write blank (%d,%d):%s\n" % (row, 0, companyname))
            else:
                print("write blank (%d,%d):%s success\n" % (row, 0, companyname))
            for master in company.multiMaster:
                assignSheet.write(row, cityColIndexDict[master], company.masterScore)
            for branch in company.branches:
                if -1 == assignSheet.write(row, cityColIndexDict[branch], company.branchScore):
                    print("error write blank (%d,%d):%d\n" % (row, cityColIndexDict[branch], company.branchScore));
            row += 1
        print("finish AssignMatrix success\n")

    def writeCDCFullAndTrialAngleMatrix(self, filename):
        allMatrix = self.matrixSheets[filename]
        CDCFullMatrixSheet = allMatrix["CDCFullMatrix"]
        CDCTrialAngelSheet = allMatrix["CDCTrialAngelMatrix"]
        cityManager = self.citysManagers[filename]
        cityIndexDict = dict()
        indexCityDict = dict()
        col = 1
        for cityname in cityManager.cityDict.keys():
            CDCFullMatrixSheet.write(0, col, cityname)
            cityIndexDict[cityname] = col
            indexCityDict[col] = cityname
            col += 1
        row = 1
        for cityname in cityManager.cityDict.keys():
            CDCFullMatrixSheet.write(row, 0, cityname)
            row += 1
        cityNum = len(cityManager.cityDict.items())
        triAngleRow = 1
        maxScore = 0
        doubleCityScore = dict()
        for i in range(1, (cityNum - 1)):
            for j in range(i + 1, cityNum):
                rowCity = cityManager.cityDict[indexCityDict[i]]
                colCity = cityManager.cityDict[indexCityDict[j]]
                score = 0
                for companyname in rowCity.companyScoreMap.keys():
                    if companyname in colCity.companyScoreMap.keys():
                        score += (rowCity.companyScoreMap[companyname] \
                                  * colCity.companyScoreMap[companyname])
                        print("%s in city(%s) and city(%s):%d\n"%(companyname,rowCity.cityName,colCity.cityName,score))
                CDCFullMatrixSheet.write(i,j,score)
                CDCFullMatrixSheet.write(j, i, score)
                if score!=0 :
                    triangle = [rowCity.cityName, colCity.cityName,score]
                    CDCTrialAngelSheet.write_row(triAngleRow,0,triangle)
                    doubleCityScore[triAngleRow] = score
                    triAngleRow += 1
                    maxScore = max(maxScore,score)
        for i in range(1,triAngleRow):
            print("debug %d/%d = ?\n"%(doubleCityScore[i], maxScore))
            CDCTrialAngelSheet.write_number(i, 3, doubleCityScore[i]/maxScore)
        print("finish CDCFullMatrix and trialAngleMatrix success\n")



    def writeGNCMatrix(self, filename):
        allMatrix = self.matrixSheets[filename]
        GNCMatrixSheet = allMatrix["GNCMatrix"]
        cityManager = self.citysManagers[filename]
        row = 1
        record = []
        for cityname in cityManager.cityDict.keys():
            city = cityManager.cityDict[cityname]
            GNCMatrixSheet.write(row, 0, cityname)
            record.append(city.basicInfo["totalScore"])
            GNCMatrixSheet.write(row, 1, city.basicInfo["totalScore"])
            row += 1
        print("finish GNCMatrix success,max record is %d\n"%max(record))
    def writeCDRTrialAngelMatrix(self, filename):
        pass

    def writeCDRFullMatrix(self, filename):
        pass

    def writeMatrix(self, filename):
        self.writeAssignMatrix(filename)
        self.writeCDCFullAndTrialAngleMatrix(filename)
        self.writeGNCMatrix(filename)
        self.writeCDRTrialAngelMatrix(filename)
        self.writeCDRFullMatrix(filename)

    def after_write(self, filename):
        allMatrix = self.matrixSheets[filename]
        allMatrix["workboot"].close()

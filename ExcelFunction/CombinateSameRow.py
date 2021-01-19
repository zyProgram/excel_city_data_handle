import xlrd  # 读模块
import xlsxwriter  # 写模块

class CountryInfo:
    def __init__(self,chineseName,number,ratio,rank):
        self.rank = rank
        self.chineseName = chineseName
        self.number = number
        self.ratio = ratio
    def combinate_info(self):
        return self.chineseName+"("+str(self.number)+")"

class SameRwFunc():
    # handleMatrixName = ["金融", "保险", "船级社", "海事法律"]
    handleMatrixName =["船东","船舶管理","船舶维修"]

    handleColName = ["中文", "数", "占比", "排名"]
    def __init__(self,excelName):
        self.readMatrixSheets = dict()
        self.writeMatrixSheets = dict()
        self.rankDicts = dict()
        self.excelName = excelName
    def preProcess(self):
        excelName = self.excelName
        data = xlrd.open_workbook(excelName)
        d = dict()
        for name in SameRwFunc.handleMatrixName:
            self.readMatrixSheets[name] = data.sheet_by_name(name)
        self.writeMatrixSheets = d
    def process(self):
        for name in self.readMatrixSheets:
            self.rankDicts[name] = dict()
            rankDict = self.rankDicts[name]
            cols = [0,0,0,0]
            sheet = self.readMatrixSheets[name]
            totalRow = sheet.nrows
            for col in range(0,sheet.row_len(1)):
                val = str(sheet.cell_value(0,col))
                if SameRwFunc.handleColName[0] in val:
                    cols[0] = col
                if SameRwFunc.handleColName[1] in val:
                   cols[1] = col
                if SameRwFunc.handleColName[2] in val:
                   cols[2] = col
                if SameRwFunc.handleColName[3] in val:
                   cols[3] = col
                if "2019" in val:
                    break
            for row in range(1, totalRow):
                s = sheet.cell_value(row, cols[0])
                if '' == s:
                    break
                chinesename  = sheet.cell_value(row, cols[0])
                number  = sheet.cell_value(row, cols[1])
                ratio = sheet.cell_value(row, cols[2])
                rank = sheet.cell_value(row, cols[3])
                if rank not in rankDict.keys():
                    rankDict[rank] = []
                rankDict[rank].append(CountryInfo(chinesename,number,ratio,rank))
            print("total country is %d\n" % rankDict.__len__())
    def afterProcess(self,outputfile):
        workboot = xlsxwriter.Workbook(outputfile)
        for name in SameRwFunc.handleMatrixName:
            outputname = "output_"+name
            self.writeMatrixSheets[outputname] = workboot.add_worksheet(outputname)
        for name in self.handleMatrixName:
            writeSheet = self.writeMatrixSheets["output_"+name]
            writeSheet.write(0, 0, "排名")
            writeSheet.write(0, 1, "国家(企业数)")
            writeSheet.write(0, 2, "市场份额")
            writeRow = 1
            cur_rank = self.rankDicts[name]
            for (rank, rankCitys) in cur_rank.items():
                if -1 == writeSheet.write(writeRow, 0, int(rank)):
                    print("error write blank (%d,%d):%d\n" % (writeRow, 0, int(rank)))
                else:
                    print("write blank (%d,%d):%d success\n" % (writeRow, 0, int(rank)))
                second = str()
                index=1
                for city in rankCitys:
                    second += city.combinate_info()
                    if index != rankCitys.__len__():
                        second += ","
                    index+=1
                if -1 == writeSheet.write(writeRow, 1, second):
                    print("error write blank (%d,%d):%s\n" % (writeRow, 1, second))
                else:
                    print("write blank (%d,%d):%s success\n" % (writeRow, 1, second))

                if -1 == writeSheet.write(writeRow, 2, rankCitys[0].ratio):
                    print("error write blank (%d,%d):%f\n" % (writeRow, 2, rankCitys[0].ratio))
                else:
                    print("write blank (%d,%d):%f success\n" % (writeRow, 2, rankCitys[0].ratio))
                writeRow+=1
            print("finish sheet %s success\n" % "output_"+name)
        workboot.close()

if __name__ == "__main__":
    lele = SameRwFunc("/home/zhangyu/PycharmProjects/excel_city_data_handle/data/func/new_up_stream.xlsx")
    lele.preProcess()
    lele.process()
    lele.afterProcess("/home/zhangyu/PycharmProjects/excel_city_data_handle/data/func/output_up_stream.xls")

class City(object):
    def __init__(self,name):
        self.__cityName = name
        self.__totoalCompanyNum = 0
        self.__companyScoreMap = dict()

    def push_back(self,companyname,isMaster):
        if companyname not in self.__companyScoreMap:
            self.__companyScoreMap[companyname] = 1 if isMaster else 0
            self.totoalCompanyNum += 1

    @property
    def cityName(self):
        return self.__cityName
    @property
    def companyScoreMap(self):
        return self.__companyScoreMap

    @property
    def totoalCompanyNum(self):
        return self.__totoalCompanyNum

    @totoalCompanyNum.setter
    def totoalCompanyNum(self,num):
        self.__totoalCompanyNum = num

    @property
    def basicInfo(self):
        totalScore = 0
        for (company,score) in self.__companyScoreMap.items():
            totalScore += score
        basicDict = {"totalCompanyNum": self.totoalCompanyNum,\
                     "totalScore":totalScore}
        return basicDict

class CityManager(object):
    def __init__(self,id):
        self.managerId = id
        self.cityDict = dict()

    def push_back(self,cityname,companyname,isMaster):
        cityname = cityname.strip()
        companyname = companyname.strip()
        if cityname not in self.cityDict:
            city = City(cityname)
            self.cityDict[cityname] = city

        city = self.cityDict[cityname]
        city.push_back(companyname,isMaster)

    def show(self):
        localIndex = 1
        print("basic info of all city as follow:\ntotal city:%d\n" % len(self.cityDict))
        for (cityName, city) in self.cityDict.items():
            citydict = city.basicInfo
            print("city %d:%s\n" % (localIndex, cityName))
            for (k, v) in citydict.items():
                print("\t%s:%d " % (k, v))
            print("\n")
            localIndex += 1


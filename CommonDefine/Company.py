class Company(object):
    def __init__(self, name):
        self.companyName = name
        self.dumplicateCity = dict()
        self.totalCityNum = 0
        self.multiMaster = []
        self.__branches = []

    def __eq__(self, other):
        if isinstance(other, Company):
            return self.companyName == other.companyName
        if isinstance(other, str):
            return self.companyName == other
        else:
            raise Exception("company compare type dont match")

    @property
    def branchNum(self):
        return len(self.branches)

    @property
    def masterNum(self):
        return len(self.multiMaster)

    @property
    def masterScore(self):
        return self.__masterScore

    @masterScore.setter
    def masterScore(self, score):
        self.__masterScore = score

    @property
    def branchScore(self):
        return self.__branchScore

    @branchScore.setter
    def branchScore(self, score):
        self.__branchScore = score

    @property
    def master(self):
        return self.multiMaster

    @master.setter
    def master(self, master):
        if master not in self.multiMaster:
            self.multiMaster.append(master)
            self.totalCityNum += 1
            self.assignScore()

    @property
    def branches(self):
        return self.__branches

    def assignScore(self):
        num = self.totalCityNum
        if num >= 15:
            self.masterScore = 5
            self.branchScore = 3
        elif 8 <= num <= 14:
            self.masterScore = 4
            self.branchScore = 2
        elif 2 <= num <= 7:
            self.masterScore = 3
            self.branchScore = 1
        else:
            self.masterScore = 0
            self.branchScore = 0

    def push_back(self, branch):
        if branch in self.dumplicateCity.keys():
            self.dumplicateCity[branch] += 1
            return
        if branch in self.branches:
            self.dumplicateCity[branch] = 2
            return
        self.branches.append(branch)
        self.totalCityNum += 1
        self.assignScore()

    @property
    def branch_total_size(self):
        return len(self.branch)

    def show(self):
        print("info of city:%s\n", self.companyName)
        if len(self.multiMaster) > 0:
            localCount = 1
            print("exist multi master:%d" % len(self.companyName, self))
            for n in self.multiMaster:
                print("master %d:%s\n" % (localCount, n))
                localCount += 1
        else:
            print("one master:%s\n" % self.master)
        if len(self.branchs) == 0:
            print("no branches\n")
        else:
            localCount = 1
            for n in self.branches:
                print("braches %d:%s\n" % (localCount, n))
                localCount += 1

    @property
    def basicInfo(self):
        basicDict = {"totalCompanyNum": self.totalCityNum, \
                     "masterNum": self.masterNum, \
                     "branchNum": self.branchNum}
        if len(self.dumplicateCity) != 0:
            n = len(self.dumplicateCity)
            for (city, dumplicate) in self.dumplicateCity.items():
                basicDict[city] = dumplicate
        return basicDict


class CompanyManager(object):
    def __init__(self,id):
        self.managerId = id
        self.companyDict = dict()

    def push_back(self, companyname, city, ismaster):
        if companyname not in self.companyDict.keys():
            company = Company(companyname)
            self.companyDict[companyname] = company

        company = self.companyDict[companyname]
        if ismaster:
            company.master = city
        else:
            company.push_back(city)

    def total_company_number(self):
        return len(self.companyDict)

    def show(self):
        localIndex = 1
        recordMultiCompany = dict()
        print("basic info of all company as follow:\ntotal company:%d\n" % len(self.companyDict))
        for (companyName, company) in self.companyDict.items():
            if company.masterNum > 1:
                recordMultiCompany[companyName] = company.masterNum
            companydict = company.basicInfo
            print("company %d:%s\n" % (localIndex, companyName))
            for (k, v) in companydict.items():
                print("\t%s:%d " % (k, v))
            print("\n")
            localIndex += 1
        print("summary:\n")
        for (k, v) in recordMultiCompany.items():
            print("the multi master company:%s,%d\n" % (k, v))

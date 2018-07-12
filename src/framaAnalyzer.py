import os
import re


class functionStats(object):
    
    def __init__(self, stringToParse):
        self.__funcName = ""
        self.__pathFile = ""
        self.__sloc = 0
        self.__mccabeComplexity = 0
        self.parse(stringToParse)

    def parse(self, stringToParse):
        '''
        Stats for function </workspace/cnfmanager/packages/cnfmanager/apl/mod/libdbn/src/pUtil.c/get_sorta>\n
        ============================================================\n
        Sloc = 3\n
        Decision point = 0\n
        Global variables = 0\n
        If = 0\n
        Loop = 0\n
        Goto = 0\n
        Assignment = 2\n
        Exit point = 1\n
        Function = 1\n
        Function call = 1\n
        Pointer dereferencing = 0\n
        Cyclomatic complexity = 1\n
        '''
        m = re.search("Stats for function <(.+)>\n", stringToParse, re.MULTILINE)
        if m:
            self.__pathFile, self.__funcName = os.path.split(m.group(1))
        m = re.search("Sloc = (.+)\n", stringToParse, re.MULTILINE)
        if m:
            self.__sloc = int(m.group(1))
        m = re.search("Cyclomatic complexity = (.+)\n", stringToParse, re.MULTILINE)
        if m:
            self.__mccabeComplexity = int(m.group(1))

    def getName(self):
        return self.__funcName
    
    def getPath(self):
        return self.__pathFile
    
    def getSloc(self):
        return self.__sloc
    
    def getMccabeComplexity(self):
        return self.__mccabeComplexity

    def printInfo(self):
        print ("path:%s - func:%s - sloc:%d - mccabe complexity:%d" % (self.getPath(), self.getName(), self.getSloc(), self.getMccabeComplexity()))


class framaAnalyzer(object):

    def __init__(self, fileName):
        self.__functionList = list()
        self.__filename = ""
        self.setFileName(fileName)

    def setFileName(self, fileName):
        if os.path.exists(fileName):
            self.__filename = fileName

    def getFilename(self):
        return self.__filename

    def isItaltelMethod(self, m):
        return m and "workspace" in m.group(1)

    def isFirstLineToSave(self, line):
        m = re.search("^  Stats for function <(.+)>\n", line)
        return m if self.isItaltelMethod(m) else None

    def isLastLineToSave(self, line):
        p = re.search("^  Cyclomatic complexity = .+\n", line)
        return p

    def extractAllSectionsFromFile(self, f, sections):
        index = 0
        canSaveLine = False
        for line in f.readlines():
            if self.isFirstLineToSave(line):
                canSaveLine = True
                sections.insert(index, [])
            if canSaveLine == True:
                sections[index].append(line)
                if self.isLastLineToSave(line):
                    canSaveLine = False
                    index = index + 1

    def setStatsPerFunction(self, sections):
        for ele in sections:
            self.__stats.append("".join(ele))
            func = functionStats("".join(ele))
            self.__functionList.append(func)
        self.calculateTotalSloc()
        self.calculateTotalSlocOver60()
        self.calculatePercentageSlocOver60()
        self.calculateTotalSloc30To60()
        self.calculateTotalSloc15To30()
        self.calculateTotalSlocUnder15()

    def printStatsPerFunction(self):
        for ele in self.__functionList:
            ele.printInfo()

    def getFunctionObjectList(self):
        return self.__functionList

    def calculateTotalSloc(self):
        totalSloc = 0
        for ele in self.__functionList:
            totalSloc = totalSloc + ele.getSloc()
        self.__totalSloc = totalSloc
        
    def getTotalSloc(self):
        return self.__totalSloc
    
    def calculateTotalSlocOver60(self):
        totalSlocOver60 = 0
        for ele in self.__functionList:
            if ele.getSloc() > 60:
                totalSlocOver60 = totalSlocOver60 + ele.getSloc()
        self.__totalSlocOver60 = totalSlocOver60
    
    def getTotalSlocOver60(self):
        return self.__totalSlocOver60
    
    def calculatePercentageSlocOver60(self):
        self.__totalPercentageOver60 = (self.__totalSlocOver60 * 100) / self.__totalSloc
    
    def getPercentageSlocOver60(self):
        return self.__totalPercentageOver60

    def calculateTotalSloc30To60(self):
        totalSloc30To60 = 0
        for ele in self.__functionList:
            if ele.getSloc() > 30 and ele.getSloc() <= 60:
                totalSloc30To60 = totalSloc30To60 + ele.getSloc()
        self.__totalSloc30To60 = totalSloc30To60

    def getTotalSloc30To60(self):
        return self.__totalSloc30To60
    
    def calculatePercentageSloc30To60(self):
        self.__totalPercentage30To60 = (self.__totalSloc30To60 * 100) / self.__totalSloc
    
    def getPercentageSloc30To60(self):
        return self.__totalPercentage30To60
    
    def calculateTotalSloc15To30(self):
        totalSloc15To30 = 0
        for ele in self.__functionList:
            if ele.getSloc() > 15 and ele.getSloc() <= 30:
                totalSloc15To30 = totalSloc15To30 + ele.getSloc()
        self.__totalSloc15To30 = totalSloc15To30

    def getTotalSloc15To30(self):
        return self.__totalSloc15To30
    
    def calculatePercentageSloc15To30(self):
        self.__totalPercentage15To30 = (self.__totalSloc15To30 * 100) / self.__totalSloc
    
    def getPercentageSloc15To30(self):
        return self.__totalPercentage15To30
    
    def calculateTotalSlocUnder15(self):
        totalSlocUnder15 = 0
        for ele in self.__functionList:
            if ele.getSloc() <= 15:
                totalSlocUnder15 = totalSlocUnder15 + ele.getSloc()
        self.__totalSlocUnder15 = totalSlocUnder15

    def getTotalSlocUnder15(self):
        return self.__totalSlocUnder15
    
    def calculatePercentageSlocUnder15(self):
        self.__totalPercentageUnder15 = (self.__totalSlocUnder15 * 100) / self.__totalSloc
    
    def getPercentageSlocUnder15(self):
        return self.__totalPercentageUnder15
    
    def extractSectionsFromFile(self):
        with open(self.__filename) as f:
            sections = list()
            self.__stats = list()
            self.extractAllSectionsFromFile(f, sections)
        self.setStatsPerFunction(sections)
        return len(self.__stats)

    
if __name__ == '__main__':
    fileName = os.path.join("D:\\tmp", "pippo.txt")
    siObj = framaAnalyzer(fileName)

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
        self.functionList = list()
        self.__filename = ""
        self.setFileName(fileName)
        self.extractSectionsFromFile()

    def getFilename(self):
        return self.__filename

    def getFunctionObjectList(self):
        return self.functionList

    def setFileName(self, fileName):
        if os.path.exists(fileName):
            self.__filename = fileName
        else:
            print ("Error: Filename %s not present" % (fileName))
            quit()

    def isMethodToAnalyze(self, m):
        return m and "workspace" in m.group(1)

    def isFirstLineToSave(self, line):
        m = re.search("^  Stats for function <(.+)>\n", line)
        return m if self.isMethodToAnalyze(m) else None

    def isLastLineToSave(self, line):
        p = re.search("^  Cyclomatic complexity = .+\n", line)
        return p

    def extractSectionsFromFile(self):
        self.__stats = list()
        if self.__filename != "":
            with open(self.__filename, "r") as f:
                sections = list()
                self.extractAllSectionsFromFile(f, sections)
            self.createStatsPerFunction(sections)
        return len(self.__stats)

    def getLenStats(self):
        return len(self.__stats)
    
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

    def printStatsPerFunction(self):
        for ele in self.functionList:
            ele.printInfo()

    def createStatsPerFunction(self, sections):
        for ele in sections:
            self.__stats.append("".join(ele))
            func = functionStats("".join(ele))
            self.functionList.append(func)

    def isOverWorstThreshold(self, stats, cutoff):
        return stats[0] > cutoff[0]

    def isOverSecondThreshold(self, stats, cutoff):
        threshold = cutoff[1] - stats[0]
        return stats[1] > threshold

    def isOverThirdThreshold(self, stats, cutoff):
        threshold = cutoff[2] - stats[1] - stats[0]
        return stats[2] > threshold

    def isOneRateStars(self, stats):
        cutoff = self.getCutoff("twoStar")

        if self.isOverWorstThreshold(stats, cutoff):
            return True

        if self.isOverSecondThreshold(stats, cutoff):
            return True

        if self.isOverThirdThreshold(stats, cutoff):
            return True

        return False
    
    def isRateWith(self, stars, stats):
        cutoff = self.getCutoff(stars)

        if self.isOverWorstThreshold(stats, cutoff):
            return False

        if self.isOverSecondThreshold(stats, cutoff):
            return False

        if self.isOverThirdThreshold(stats, cutoff):
            return False

        return True

    def isTwoRateStars(self, stats):
        if self.isRateWith("fiveStar", stats) == True:
            return False
        if self.isRateWith("fourStar", stats) == True:
            return False
        if self.isRateWith("threeStar", stats) == True:
            return False
        return self.isRateWith("twoStar", stats)

    def isThreeRateStars(self, stats):
        if self.isRateWith("fiveStar", stats) == True:
            return False
        if self.isRateWith("fourStar", stats) == True:
            return False
        return self.isRateWith("threeStar", stats)
    
    def isFourRateStars(self, stats):
        if self.isRateWith("fiveStar", stats) == True:
            return False
        return self.isRateWith("fourStar", stats)

    def isFiveRateStars(self, stats):
        return self.isRateWith("fiveStar", stats)

    def calculateRateStars(self):
        stats = self.createStatsList()
        if self.isOneRateStars(stats):
            return 1
        if self.isTwoRateStars(stats):
            return 2
        if self.isThreeRateStars(stats):
            return 3
        if self.isFourRateStars(stats):
            return 4
        if self.isFiveRateStars(stats):
            return 5

    def calculateTotalSloc(self):
        totalSloc = 0
        for ele in self.functionList:
            totalSloc = totalSloc + ele.getSloc()
        self.totalSloc = float(totalSloc)
        
    def getTotalSloc(self):
        return self.totalSloc

    
class framaSlocAnalyzer(framaAnalyzer):
    __cutoff = {'fiveStar': [5, 16, 31, 69], 'fourStar': [7, 22, 44, 56], 'threeStar':[9, 28, 55, 45], 'twoStar':[10, 34, 67, 33]}

    def __init__(self, fileName):
        framaAnalyzer.__init__(self, fileName)
        self.calculateTotalSloc()
        self.calculateTotalSlocOver60()
        self.calculatePercentageSlocOver60()
        self.calculateTotalSloc30To60()
        self.calculatePercentageSloc30To60()
        self.calculateTotalSloc15To30()
        self.calculatePercentageSloc15To30()
        self.calculateTotalSlocUnder15()
        self.calculatePercentageSlocUnder15()

    def getCutoff(self, key):
        return self.__cutoff.get(key)

    def calculateTotalSlocOver60(self):
        totalSlocOver60 = 0
        for ele in self.functionList:
            if ele.getSloc() > 60:
                totalSlocOver60 = totalSlocOver60 + ele.getSloc()
        self.__totalSlocOver60 = float(totalSlocOver60)
    
    def getTotalSlocOver60(self):
        return self.__totalSlocOver60
    
    def calculatePercentageSlocOver60(self):
        self.__totalPercentageOver60 = round((self.__totalSlocOver60 * 100) / self.totalSloc, 2)
    
    def getPercentageSlocOver60(self):
        return self.__totalPercentageOver60

    def calculateTotalSloc30To60(self):
        totalSloc30To60 = 0
        for ele in self.functionList:
            if ele.getSloc() > 30 and ele.getSloc() <= 60:
                totalSloc30To60 = totalSloc30To60 + ele.getSloc()
        self.__totalSloc30To60 = float(totalSloc30To60)
    
    def calculatePercentageSloc30To60(self):
        self.__totalPercentage30To60 = round((self.__totalSloc30To60 * 100) / self.totalSloc, 2)
    
    def getTotalSloc30To60(self):
        return self.__totalSloc30To60

    def getPercentageSloc30To60(self):
        return self.__totalPercentage30To60

    def calculateTotalSloc15To30(self):
        totalSloc15To30 = 0
        for ele in self.functionList:
            if ele.getSloc() > 15 and ele.getSloc() <= 30:
                totalSloc15To30 = totalSloc15To30 + ele.getSloc()
        self.__totalSloc15To30 = float(totalSloc15To30)

    def getTotalSloc15To30(self):
        return self.__totalSloc15To30
    
    def getPercentageSloc15To30(self):
        return self.__totalPercentage15To30

    def calculatePercentageSloc15To30(self):
        self.__totalPercentage15To30 = round((self.__totalSloc15To30 * 100) / self.totalSloc, 2)

    def getTotalSlocUnder15(self):
        return self.__totalSlocUnder15
    
    def calculateTotalSlocUnder15(self):
        totalSlocUnder15 = 0
        for ele in self.functionList:
            if ele.getSloc() <= 15:
                totalSlocUnder15 = totalSlocUnder15 + ele.getSloc()
        self.__totalSlocUnder15 = float(totalSlocUnder15)
    
    def calculatePercentageSlocUnder15(self):
        self.__totalPercentageUnder15 = round((self.__totalSlocUnder15 * 100) / self.totalSloc, 2)
    
    def getPercentageSlocUnder15(self):
        return self.__totalPercentageUnder15

    def createStatsList(self):
        return [self.getPercentageSlocOver60(), self.getPercentageSloc30To60(), self.getPercentageSloc15To30(), self.getPercentageSlocUnder15()]


class framaMcCabeAnalyzer(framaAnalyzer):

    __cutoff = {'fiveStar': [1, 5, 13, 87], 'fourStar': [2, 10, 25, 75], 'threeStar':[3, 13, 32, 68], 'twoStar':[5, 16, 39, 61]}

    def __init__(self, fileName):
        framaAnalyzer.__init__(self, fileName)
        self.calculateTotalSloc()
        self.calculateTotalMcCabeOver25()
        self.calculatePercentageMcCabeOver25()
        self.calculateTotalMcCabe10To25()
        self.calculatePercentageMcCabe10To25()
        self.calculateTotalMcCabe5To10()
        self.calculatePercentageMcCabe5To10()
        self.calculateTotalMcCabeUnder5()
        self.calculatePercentageMcCabeUnder5()

    def getCutoff(self, key):
        return self.__cutoff.get(key)

    def calculateTotalMcCabeOver25(self):
        totalMcCabeOver25 = 0
        for ele in self.functionList:
            if ele.getMccabeComplexity() > 25:
                totalMcCabeOver25 = totalMcCabeOver25 + ele.getSloc()
        self.__totalMcCabeOver25 = float(totalMcCabeOver25)
    
    def getTotalMcCabeOver25(self):
        return self.__totalMcCabeOver25
    
    def calculatePercentageMcCabeOver25(self):
        self.__totalPercentageOver25 = round((self.__totalMcCabeOver25 * 100) / self.totalSloc, 2)
    
    def getPercentageMcCabeOver25(self):
        return self.__totalPercentageOver25

    def calculateTotalMcCabe10To25(self):
        totalMcCabe10To25 = 0
        for ele in self.functionList:
            if ele.getMccabeComplexity() > 10 and ele.getMccabeComplexity() <= 25:
                totalMcCabe10To25 = totalMcCabe10To25 + ele.getSloc()
        self.__totalMcCabe10To25 = float(totalMcCabe10To25)

    def getTotalMcCabe10To25(self):
        return self.__totalMcCabe10To25
    
    def getPercentageMcCabe10To25(self):
        return self.__totalPercentage10To25

    def calculatePercentageMcCabe10To25(self):
        self.__totalPercentage10To25 = round((self.__totalMcCabe10To25 * 100) / self.totalSloc, 2)

    def calculateTotalMcCabe5To10(self):
        totalMcCabe5To10 = 0
        for ele in self.functionList:
            if ele.getMccabeComplexity() > 5 and ele.getMccabeComplexity() <= 10:
                totalMcCabe5To10 = totalMcCabe5To10 + ele.getSloc()
        self.__totalMcCabe5To10 = float(totalMcCabe5To10)

    def getTotalMcCabe5To10(self):
        return self.__totalMcCabe5To10
    
    def getPercentageMcCabe5To10(self):
        return self.__totalPercentage5To10

    def calculatePercentageMcCabe5To10(self):
        self.__totalPercentage5To10 = round((self.__totalMcCabe5To10 * 100) / self.totalSloc, 2)
        
    def calculateTotalMcCabeUnder5(self):
        totalMcCabeUnder5 = 0
        for ele in self.functionList:
            if ele.getMccabeComplexity() <= 5:
                totalMcCabeUnder5 = totalMcCabeUnder5 + ele.getSloc()
        self.__totalMcCabeUnder5 = float(totalMcCabeUnder5)

    def getTotalMcCabeUnder5(self):
        return self.__totalMcCabeUnder5
    
    def getPercentageMcCabeUnder5(self):
        return self.__totalPercentageUnder5

    def calculatePercentageMcCabeUnder5(self):
        self.__totalPercentageUnder5 = round((self.__totalMcCabeUnder5 * 100) / self.totalSloc, 2)

    def createStatsList(self):
        return [self.getPercentageMcCabeOver25(), self.getPercentageMcCabe10To25(), self.getPercentageMcCabe5To10(), self.getPercentageMcCabeUnder5()]


if __name__ == '__main__':
    fileName = os.path.join("D:\\tmp", "pippo.txt")
    slocAnalyzer = framaSlocAnalyzer(fileName)
    mcCabeAnalyzer = framaMcCabeAnalyzer(fileName)
    print("SLOC STATS: %d %d %d %d" % (slocAnalyzer.getPercentageSlocOver60(), slocAnalyzer.getPercentageSloc30To60(), slocAnalyzer.getPercentageSloc15To30(), slocAnalyzer.getPercentageSlocUnder15()))
    print("MCCABE STATS: %d %d %d %d" % (mcCabeAnalyzer.getPercentageMcCabeOver25(), mcCabeAnalyzer.getPercentageMcCabe10To25(), mcCabeAnalyzer.getPercentageMcCabe5To10(), mcCabeAnalyzer.getPercentageMcCabeUnder5()))


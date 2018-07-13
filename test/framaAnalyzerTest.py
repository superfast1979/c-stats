import unittest
import os
import framaAnalyzer as fa

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Test_framaStats(unittest.TestCase):

    def setUp(self):
        self.createFramaAnalyzer()

    def tearDown(self):
        pass

    def test_checkFilenameSavedOnConstructor(self):
        self.assertEqual(os.path.join(ROOT_DIR, 'pippo.txt'), self.siObj.getFilename())

    def test_checkFilenameSavedOnConstructorFileNotFound(self):
        self.siObj = fa.framaAnalyzer('pluto.txt')
        self.assertEqual("", self.siObj.getFilename())

    def createFramaAnalyzer(self):
        self.siObj = fa.framaAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))

    def test_extractSectionFromFile(self):
        self.createFramaAnalyzer()
        self.assertEqual(79, self.siObj.extractSectionsFromFile())
        
    def test_getFunctionList(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.assertEqual(79, len(self.siObj.getFunctionObjectList()))
        
    def test_getFunctionListCheckObject(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual("check_num_record", funcList[0].getName())
        self.assertEqual(2, funcList[0].getSloc())
        self.assertEqual(1, funcList[0].getMccabeComplexity())
        self.assertEqual("xmlParse_Startup", funcList[78].getName())
        self.assertEqual(28, funcList[78].getSloc())
        self.assertEqual(7, funcList[78].getMccabeComplexity())

    def test_getTotalSloc(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual(1567, self.siObj.getTotalSloc())
        
    def test_getTotalSlocOver60(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSlocOver60()
        self.assertEqual(333, self.siObj.getTotalSlocOver60())
        
    def test_getPercentageSlocOver60(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSlocOver60()
        self.assertEqual(21.25, self.siObj.getPercentageSlocOver60())
        
    def test_getTotalSloc30To60(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSloc30To60()
        self.assertEqual(290, self.siObj.getTotalSloc30To60())
        
    def test_getPercentageSloc30To60(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSloc30To60()
        self.assertEqual(18.51, self.siObj.getPercentageSloc30To60())
        
    def test_getTotalSloc15To30(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSloc15To30()
        self.assertEqual(642, self.siObj.getTotalSloc15To30())
        
    def test_getPercentageSloc15To30(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSloc15To30()
        self.assertEqual(40.97, self.siObj.getPercentageSloc15To30())
        
    def test_getTotalSlocUnder15(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSlocUnder15()
        self.assertEqual(302, self.siObj.getTotalSlocUnder15())
        
    def test_getPercentageSlocUnder15(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSlocUnder15()
        self.assertEqual(19.27, self.siObj.getPercentageSlocUnder15())

    def test_sumAllPercentage(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSlocUnder15()
        self.siObj.calculatePercentageSloc15To30()
        self.siObj.calculatePercentageSloc30To60()
        self.siObj.calculatePercentageSlocOver60()
        sumPerc = self.siObj.getPercentageSlocUnder15()
        sumPerc = sumPerc + self.siObj.getPercentageSloc15To30()
        sumPerc = sumPerc + self.siObj.getPercentageSloc30To60()
        sumPerc = sumPerc + self.siObj.getPercentageSlocOver60()
        self.assertEqual(100, sumPerc)
        
    def test_getCutoff(self):
        self.createFramaAnalyzer()
        self.assertEqual([7, 22, 44, 56], self.siObj.getCutoff('fourStar'))
        self.assertEqual([5, 16, 31, 69], self.siObj.getCutoff('threeStar'))
        self.assertEqual([3, 10, 20, 80], self.siObj.getCutoff('twoStar'))
        self.assertEqual([2, 8, 18, 82], self.siObj.getCutoff('oneStar'))
        
    def test_isOverWorstThreshold(self):
        self.createFramaAnalyzer()
        self.assertTrue(self.siObj.isOverWorstThreshold([9, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverWorstThreshold([7, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverWorstThreshold([6, 0, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverWorstThreshold([6, 0, 0, 91], [5, 22, 44, 56]))
        
    def test_isOverSecondThreshold(self):
        self.createFramaAnalyzer()
        self.assertTrue(self.siObj.isOverSecondThreshold([5, 18, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverSecondThreshold([4, 19, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverSecondThreshold([5, 17, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverSecondThreshold([4, 18, 0, 91], [7, 22, 44, 56]))
        
    def test_isOverThirdThreshold(self):
        self.createFramaAnalyzer()
        self.assertTrue(self.siObj.isOverThirdThreshold([5, 17, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverThirdThreshold([7, 15, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverThirdThreshold([1, 1, 43, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverThirdThreshold([4, 18, 22, 91], [7, 22, 44, 56]))
        
    def test_isFiveRateStars(self):
        self.createFramaAnalyzer()
        self.assertTrue(self.siObj.isFiveRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isFiveRateStars([7, 0, 0, 91]))
        
    def test_isOneRateStars(self):
        self.createFramaAnalyzer()
        self.assertFalse(self.siObj.isOneRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isOneRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isOneRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isOneRateStars([1, 7, 19, 81]))
        self.assertTrue(self.siObj.isOneRateStars([1, 7, 10, 83]))
        
    def test_isTwoRateStars(self):
        self.createFramaAnalyzer()
        self.assertFalse(self.siObj.isTwoRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([1, 7, 19, 81]))
        self.assertTrue(self.siObj.isTwoRateStars([1, 9, 0, 91]))
        self.assertTrue(self.siObj.isTwoRateStars([1, 7, 12, 80]))
        
    def test_isThreeRateStars(self):
        self.createFramaAnalyzer()
        self.assertFalse(self.siObj.isThreeRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 7, 12, 80]))
        self.assertTrue(self.siObj.isThreeRateStars([1, 7, 19, 81]))
        self.assertTrue(self.siObj.isThreeRateStars([4, 12, 15, 80]))
        self.assertTrue(self.siObj.isThreeRateStars([1, 15, 10, 80]))
        
    def test_isFourRateStars(self):
        self.createFramaAnalyzer()
        self.assertFalse(self.siObj.isFourRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([1, 7, 12, 80]))
        self.assertFalse(self.siObj.isFourRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isFourRateStars([4, 12, 15, 80]))
        self.assertFalse(self.siObj.isFourRateStars([1, 15, 10, 80]))
        self.assertTrue(self.siObj.isFourRateStars([7, 0, 0, 91]))
        self.assertTrue(self.siObj.isFourRateStars([7, 10, 26, 60]))

    def test_getRateStars(self):
        self.createFramaAnalyzer()
        self.siObj.extractSectionsFromFile()
        actualStats = self.siObj.createStatsList()
        self.assertEqual(5, self.siObj.getRateStars(actualStats))


suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaStats)
unittest.TextTestRunner(verbosity=2).run(suite)


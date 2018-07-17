import unittest
import os
import framaAnalyzer as fa

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Test_framaAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createFramaAnalyzer()

    def tearDown(self):
        pass

    def createFramaAnalyzer(self):
        self.siObj = fa.framaAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))
        return self.siObj.getLenStats()
        
    def test_checkFilenameSavedOnConstructor(self):
        self.assertEqual(os.path.join(ROOT_DIR, 'pippo.txt'), self.siObj.getFilename())

    def test_checkFilenameSavedOnConstructorFileNotFound(self):
        self.siObj = fa.framaAnalyzer('pluto.txt')
        self.assertEqual("", self.siObj.getFilename())

    def test_extractSectionFromFile(self):
        self.assertEqual(79, self.createFramaAnalyzer())
        
    def test_getFunctionList(self):
        self.assertEqual(79, len(self.siObj.getFunctionObjectList()))
        
    def test_getFunctionListCheckObject(self):
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual("check_num_record", funcList[0].getName())
        self.assertEqual(2, funcList[0].getSloc())
        self.assertEqual(1, funcList[0].getMccabeComplexity())
        self.assertEqual("xmlParse_Startup", funcList[78].getName())
        self.assertEqual(28, funcList[78].getSloc())
        self.assertEqual(7, funcList[78].getMccabeComplexity())

    def test_isOverWorstThreshold(self):
        self.assertTrue(self.siObj.isOverWorstThreshold([9, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverWorstThreshold([7, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverWorstThreshold([6, 0, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverWorstThreshold([6, 0, 0, 91], [5, 22, 44, 56]))
        
    def test_isOverSecondThreshold(self):
        self.assertTrue(self.siObj.isOverSecondThreshold([5, 18, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverSecondThreshold([4, 19, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverSecondThreshold([5, 17, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverSecondThreshold([4, 18, 0, 91], [7, 22, 44, 56]))
        
    def test_isOverThirdThreshold(self):
        self.assertTrue(self.siObj.isOverThirdThreshold([5, 17, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverThirdThreshold([7, 15, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.siObj.isOverThirdThreshold([1, 1, 43, 91], [7, 22, 44, 56]))
        self.assertFalse(self.siObj.isOverThirdThreshold([4, 18, 22, 91], [7, 22, 44, 56]))


class Test_framaSlocAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createSlocFramaAnalyzer()

    def tearDown(self):
        pass

    def createSlocFramaAnalyzer(self):
        self.siObj = fa.framaSlocAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))

    def test_getCutoff(self):
        self.assertEqual([5, 16, 31, 69], self.siObj.getCutoff('fiveStar'))
        self.assertEqual([7, 22, 44, 56], self.siObj.getCutoff('fourStar'))
        self.assertEqual([9, 28, 55, 45], self.siObj.getCutoff('threeStar'))
        self.assertEqual([10, 34, 67, 33], self.siObj.getCutoff('twoStar'))

    def test_getTotalSloc(self):
        self.assertEqual(1567, self.siObj.getTotalSloc())
        
    def test_getTotalSlocOver60(self):
        self.assertEqual(333, self.siObj.getTotalSlocOver60())
        
    def test_getPercentageSlocOver60(self):
        self.assertEqual(21.25, self.siObj.getPercentageSlocOver60())
        
    def test_getTotalSloc30To60(self):
        self.assertEqual(290, self.siObj.getTotalSloc30To60())
        
    def test_getPercentageSloc30To60(self):
        self.assertEqual(18.51, self.siObj.getPercentageSloc30To60())
        
    def test_getTotalSloc15To30(self):
        self.assertEqual(642, self.siObj.getTotalSloc15To30())
        
    def test_getPercentageSloc15To30(self):
        self.assertEqual(40.97, self.siObj.getPercentageSloc15To30())
        
    def test_getTotalSlocUnder15(self):
        self.assertEqual(302, self.siObj.getTotalSlocUnder15())
        
    def test_getPercentageSlocUnder15(self):
        self.assertEqual(19.27, self.siObj.getPercentageSlocUnder15())

    def test_sumAllPercentage(self):
        sumPerc = self.siObj.getPercentageSlocUnder15()
        sumPerc = sumPerc + self.siObj.getPercentageSloc15To30()
        sumPerc = sumPerc + self.siObj.getPercentageSloc30To60()
        sumPerc = sumPerc + self.siObj.getPercentageSlocOver60()
        self.assertEqual(100, sumPerc)
        
    def test_isOneRateStars(self):
        self.assertTrue(self.siObj.isOneRateStars([11, 0, 0, 91]))
        self.assertTrue(self.siObj.isOneRateStars([9, 36, 0, 91]))
        self.assertFalse(self.siObj.isOneRateStars([10, 24, 23, 33]))

    def test_isTwoRateStars(self):
        self.assertFalse(self.siObj.isTwoRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isTwoRateStars([1, 9, 0, 91]))
        self.assertTrue(self.siObj.isTwoRateStars([10, 24, 23, 80]))

    def test_isThreeRateStars(self):
        self.assertTrue(self.siObj.isThreeRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 7, 12, 80]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 7, 19, 81]))
        self.assertTrue(self.siObj.isThreeRateStars([4, 23, 28, 80]))
        self.assertTrue(self.siObj.isThreeRateStars([9, 19, 23, 80]))
         
    def test_isFourRateStars(self):
        self.assertFalse(self.siObj.isFourRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([1, 7, 12, 80]))
        self.assertFalse(self.siObj.isFourRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isFourRateStars([4, 12, 15, 80]))
        self.assertFalse(self.siObj.isFourRateStars([1, 15, 10, 80]))
        self.assertTrue(self.siObj.isFourRateStars([7, 0, 0, 91]))
        self.assertTrue(self.siObj.isFourRateStars([7, 10, 26, 60]))
 
    def test_isFiveRateStars(self):
        self.assertFalse(self.siObj.isFiveRateStars([9, 0, 0, 91]))
        self.assertTrue(self.siObj.isFiveRateStars([5, 0, 0, 91]))
          
    def test_getRateStars(self):
        self.assertEqual(1, self.siObj.calculateRateStars())


class Test_framaMcCabeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createMcCabeFramaAnalyzer()

    def tearDown(self):
        pass

    def createMcCabeFramaAnalyzer(self):
        self.siObj = fa.framaMcCabeAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))

    def test_getCutoff(self):
        self.assertEqual([1, 5, 13, 87], self.siObj.getCutoff('fiveStar'))
        self.assertEqual([2, 10, 25, 75], self.siObj.getCutoff('fourStar'))
        self.assertEqual([3, 13, 32, 68], self.siObj.getCutoff('threeStar'))
        self.assertEqual([5, 16, 39, 61], self.siObj.getCutoff('twoStar'))

    def test_getTotalMcCabe(self):
        self.assertEqual(1567, self.siObj.getTotalMcCabeLines())

    def test_getTotalMcCabeOver25(self):
        self.assertEqual(162, self.siObj.getTotalMcCabeOver25())

    def test_getPercentageMcCabeOver25(self):
        self.assertEqual(10.34, self.siObj.getPercentageMcCabeOver25())

    def test_getTotalMcCabe10To25(self):
        self.assertEqual(264, self.siObj.getTotalMcCabe10To25())
        
    def test_getPercentageMcCabe10To25(self):
        self.assertEqual(16.85, self.siObj.getPercentageMcCabe10To25())
        
    def test_getTotalMcCabe5To10(self):
        self.assertEqual(362, self.siObj.getTotalMcCabe5To10())
        
    def test_getPercentageMcCabe5To10(self):
        self.assertEqual(23.1, self.siObj.getPercentageMcCabe5To10())
        
    def test_getTotalMcCabeUnder5(self):
        self.assertEqual(779, self.siObj.getTotalMcCabeUnder5())
        
    def test_getPercentageMcCabeUnder5(self):
        self.assertEqual(49.71, self.siObj.getPercentageMcCabeUnder5())

    def test_sumAllPercentage(self):
        sumPerc = self.siObj.getPercentageMcCabeOver25()
        sumPerc = sumPerc + self.siObj.getPercentageMcCabe10To25()
        sumPerc = sumPerc + self.siObj.getPercentageMcCabe5To10()
        sumPerc = sumPerc + self.siObj.getPercentageMcCabeUnder5()
        self.assertEqual(100, sumPerc)

    def test_isOneRateStars(self):
        self.assertTrue(self.siObj.isOneRateStars([11, 0, 0, 91]))
        self.assertTrue(self.siObj.isOneRateStars([9, 36, 0, 91]))
        self.assertFalse(self.siObj.isOneRateStars([5, 1, 1, 33]))

    def test_isTwoRateStars(self):
        self.assertFalse(self.siObj.isTwoRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isTwoRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isTwoRateStars([1, 9, 0, 91]))
        self.assertTrue(self.siObj.isTwoRateStars([5, 11, 23, 80]))

    def test_isThreeRateStars(self):
        self.assertTrue(self.siObj.isThreeRateStars([3, 10, 19, 91]))
        self.assertTrue(self.siObj.isThreeRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isThreeRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 9, 0, 91]))
        self.assertFalse(self.siObj.isThreeRateStars([1, 7, 12, 80]))
        self.assertFalse(self.siObj.isThreeRateStars([4, 23, 28, 80]))
        self.assertFalse(self.siObj.isThreeRateStars([9, 19, 23, 80]))
         
    def test_isFourRateStars(self):
        self.assertTrue(self.siObj.isFourRateStars([1, 9, 0, 91]))
        self.assertTrue(self.siObj.isFourRateStars([1, 7, 12, 80]))
        self.assertFalse(self.siObj.isFourRateStars([9, 0, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([1, 7, 19, 81]))
        self.assertFalse(self.siObj.isFourRateStars([4, 12, 15, 80]))
        self.assertFalse(self.siObj.isFourRateStars([1, 15, 10, 80]))
        self.assertFalse(self.siObj.isFourRateStars([7, 0, 0, 91]))
        self.assertFalse(self.siObj.isFourRateStars([7, 10, 26, 60]))
 
    def test_isFiveRateStars(self):
        self.assertFalse(self.siObj.isFiveRateStars([9, 0, 0, 91]))
        self.assertTrue(self.siObj.isFiveRateStars([1, 1, 10, 91]))
          
    def test_getRateStars(self):
        self.assertEqual(1, self.siObj.calculateRateStars())


suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaAnalyzer)
suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaSlocAnalyzer)
suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaMcCabeAnalyzer)
unittest.TextTestRunner(verbosity=2).run(suite)


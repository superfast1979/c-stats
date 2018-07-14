import unittest
import os
import framaAnalyzer as fa

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Test_framaAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createFramaAnalyzer()
        self.slocAnalyzer = self.siObj.getFramaSlocAnalyzer()

    def tearDown(self):
        pass

    def test_checkFilenameSavedOnConstructor(self):
        self.assertEqual(os.path.join(ROOT_DIR, 'pippo.txt'), self.siObj.getFilename())

    def test_checkFilenameSavedOnConstructorFileNotFound(self):
        self.siObj = fa.framaAnalyzer('pluto.txt')
        self.assertEqual("", self.siObj.getFilename())

    def createFramaAnalyzer(self):
        self.siObj = fa.framaAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))
        return self.siObj.extractSectionsFromFile()
        
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


class Test_framaSlocAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createFramaAnalyzer()
        self.slocAnalyzer = self.siObj.getFramaSlocAnalyzer()

    def tearDown(self):
        pass

    def createFramaAnalyzer(self):
        self.siObj = fa.framaAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))
        return self.siObj.extractSectionsFromFile()

    def test_getTotalSloc(self):
        self.assertEqual(1567, self.slocAnalyzer.getTotalSloc())
        
    def test_getTotalSlocOver60(self):
        self.assertEqual(333, self.slocAnalyzer.getTotalSlocOver60())
        
    def test_getPercentageSlocOver60(self):
        self.assertEqual(21.25, self.slocAnalyzer.getPercentageSlocOver60())
        
    def test_getTotalSloc30To60(self):
        self.assertEqual(290, self.slocAnalyzer.getTotalSloc30To60())
        
    def test_getPercentageSloc30To60(self):
        self.assertEqual(18.51, self.slocAnalyzer.getPercentageSloc30To60())
        
    def test_getTotalSloc15To30(self):
        self.assertEqual(642, self.slocAnalyzer.getTotalSloc15To30())
        
    def test_getPercentageSloc15To30(self):
        self.assertEqual(40.97, self.slocAnalyzer.getPercentageSloc15To30())
        
    def test_getTotalSlocUnder15(self):
        self.assertEqual(302, self.slocAnalyzer.getTotalSlocUnder15())
        
    def test_getPercentageSlocUnder15(self):
        self.assertEqual(19.27, self.slocAnalyzer.getPercentageSlocUnder15())

    def test_sumAllPercentage(self):
        sumPerc = self.slocAnalyzer.getPercentageSlocUnder15()
        sumPerc = sumPerc + self.slocAnalyzer.getPercentageSloc15To30()
        sumPerc = sumPerc + self.slocAnalyzer.getPercentageSloc30To60()
        sumPerc = sumPerc + self.slocAnalyzer.getPercentageSlocOver60()
        self.assertEqual(100, sumPerc)
        
    def test_getCutoff(self):
        self.assertEqual([5, 16, 31, 69], self.slocAnalyzer.getCutoff('fiveStar'))
        self.assertEqual([7, 22, 44, 56], self.slocAnalyzer.getCutoff('fourStar'))
        self.assertEqual([9, 28, 55, 45], self.slocAnalyzer.getCutoff('threeStar'))
        self.assertEqual([10, 34, 67, 33], self.slocAnalyzer.getCutoff('twoStar'))
        
    def test_isOverWorstThreshold(self):
        self.assertTrue(self.slocAnalyzer.isOverWorstThreshold([9, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.slocAnalyzer.isOverWorstThreshold([7, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.slocAnalyzer.isOverWorstThreshold([6, 0, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.slocAnalyzer.isOverWorstThreshold([6, 0, 0, 91], [5, 22, 44, 56]))
        
    def test_isOverSecondThreshold(self):
        self.assertTrue(self.slocAnalyzer.isOverSecondThreshold([5, 18, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(self.slocAnalyzer.isOverSecondThreshold([4, 19, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.slocAnalyzer.isOverSecondThreshold([5, 17, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(self.slocAnalyzer.isOverSecondThreshold([4, 18, 0, 91], [7, 22, 44, 56]))
        
    def test_isOverThirdThreshold(self):
        self.assertTrue(self.slocAnalyzer.isOverThirdThreshold([5, 17, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.slocAnalyzer.isOverThirdThreshold([7, 15, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(self.slocAnalyzer.isOverThirdThreshold([1, 1, 43, 91], [7, 22, 44, 56]))
        self.assertFalse(self.slocAnalyzer.isOverThirdThreshold([4, 18, 22, 91], [7, 22, 44, 56]))
        
    def test_isOneRateStars(self):
        self.assertTrue(self.slocAnalyzer.isOneRateStars([11, 0, 0, 91]))
        self.assertTrue(self.slocAnalyzer.isOneRateStars([9, 36, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isOneRateStars([10, 24, 23, 33]))

    def test_isTwoRateStars(self):
        self.assertFalse(self.slocAnalyzer.isTwoRateStars([9, 0, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isTwoRateStars([7, 0, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isTwoRateStars([1, 7, 19, 81]))
        self.assertFalse(self.slocAnalyzer.isTwoRateStars([1, 9, 0, 91]))
        self.assertTrue(self.slocAnalyzer.isTwoRateStars([10, 24, 23, 80]))

    def test_isThreeRateStars(self):
        self.assertTrue(self.slocAnalyzer.isThreeRateStars([9, 0, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isThreeRateStars([7, 0, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isThreeRateStars([1, 9, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isThreeRateStars([1, 7, 12, 80]))
        self.assertFalse(self.slocAnalyzer.isThreeRateStars([1, 7, 19, 81]))
        self.assertTrue(self.slocAnalyzer.isThreeRateStars([4, 23, 28, 80]))
        self.assertTrue(self.slocAnalyzer.isThreeRateStars([9, 19, 23, 80]))
         
    def test_isFourRateStars(self):
        self.assertFalse(self.slocAnalyzer.isFourRateStars([9, 0, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isFourRateStars([1, 9, 0, 91]))
        self.assertFalse(self.slocAnalyzer.isFourRateStars([1, 7, 12, 80]))
        self.assertFalse(self.slocAnalyzer.isFourRateStars([1, 7, 19, 81]))
        self.assertFalse(self.slocAnalyzer.isFourRateStars([4, 12, 15, 80]))
        self.assertFalse(self.slocAnalyzer.isFourRateStars([1, 15, 10, 80]))
        self.assertTrue(self.slocAnalyzer.isFourRateStars([7, 0, 0, 91]))
        self.assertTrue(self.slocAnalyzer.isFourRateStars([7, 10, 26, 60]))
 
    def test_isFiveRateStars(self):
        self.assertFalse(self.slocAnalyzer.isFiveRateStars([9, 0, 0, 91]))
        self.assertTrue(self.slocAnalyzer.isFiveRateStars([5, 0, 0, 91]))
          
    def test_getRateStars(self):
        self.assertEqual(1, self.slocAnalyzer.calculateRateStars())


class Test_framaMcCabeAnalyzer(unittest.TestCase):

    def setUp(self):
        self.createFramaAnalyzer()
        self.mcCabeAnalyzer = self.siObj.getFramaMcCabeAnalyzer()

    def tearDown(self):
        pass

    def createFramaAnalyzer(self):
        self.siObj = fa.framaAnalyzer(os.path.join(ROOT_DIR, 'pippo.txt'))
        return self.siObj.extractSectionsFromFile()

    def test_getCutoff(self):
        self.assertEqual([1, 5, 13, 87], self.mcCabeAnalyzer.getCutoff('fiveStar'))
        self.assertEqual([2, 10, 25, 75], self.mcCabeAnalyzer.getCutoff('fourStar'))
        self.assertEqual([3, 13, 32, 68], self.mcCabeAnalyzer.getCutoff('threeStar'))
        self.assertEqual([5, 16, 39, 61], self.mcCabeAnalyzer.getCutoff('twoStar'))


suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaAnalyzer)
suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaSlocAnalyzer)
suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaMcCabeAnalyzer)
unittest.TextTestRunner(verbosity=2).run(suite)


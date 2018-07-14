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
        return self.siObj.extractSectionsFromFile()
        
    def test_extractSectionFromFile(self):
        self.assertEqual(79, self.createFramaAnalyzer())
        
    def test_getFunctionList(self):
        self.createFramaAnalyzer()
        self.assertEqual(79, len(self.siObj.getFunctionObjectList()))
        
    def test_getFunctionListCheckObject(self):
        self.createFramaAnalyzer()
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual("check_num_record", funcList[0].getName())
        self.assertEqual(2, funcList[0].getSloc())
        self.assertEqual(1, funcList[0].getMccabeComplexity())
        self.assertEqual("xmlParse_Startup", funcList[78].getName())
        self.assertEqual(28, funcList[78].getSloc())
        self.assertEqual(7, funcList[78].getMccabeComplexity())

    def test_getTotalSloc(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(1567, slocAnalyzer.getTotalSloc())
        
    def test_getTotalSlocOver60(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(333, slocAnalyzer.getTotalSlocOver60())
        
    def test_getPercentageSlocOver60(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(21.25, slocAnalyzer.getPercentageSlocOver60())
        
    def test_getTotalSloc30To60(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(290, slocAnalyzer.getTotalSloc30To60())
        
    def test_getPercentageSloc30To60(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(18.51, slocAnalyzer.getPercentageSloc30To60())
        
    def test_getTotalSloc15To30(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(642, slocAnalyzer.getTotalSloc15To30())
        
    def test_getPercentageSloc15To30(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(40.97, slocAnalyzer.getPercentageSloc15To30())
        
    def test_getTotalSlocUnder15(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(302, slocAnalyzer.getTotalSlocUnder15())
        
    def test_getPercentageSlocUnder15(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(19.27, slocAnalyzer.getPercentageSlocUnder15())

    def test_sumAllPercentage(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        sumPerc = slocAnalyzer.getPercentageSlocUnder15()
        sumPerc = sumPerc + slocAnalyzer.getPercentageSloc15To30()
        sumPerc = sumPerc + slocAnalyzer.getPercentageSloc30To60()
        sumPerc = sumPerc + slocAnalyzer.getPercentageSlocOver60()
        self.assertEqual(100, sumPerc)
        
    def test_getCutoff(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual([5, 16, 31, 69], slocAnalyzer.getCutoff('fiveStar'))
        self.assertEqual([7, 22, 44, 56], slocAnalyzer.getCutoff('fourStar'))
        self.assertEqual([9, 28, 55, 45], slocAnalyzer.getCutoff('threeStar'))
        self.assertEqual([10, 34, 67, 33], slocAnalyzer.getCutoff('twoStar'))
        
    def test_isOverWorstThreshold(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertTrue(slocAnalyzer.isOverWorstThreshold([9, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(slocAnalyzer.isOverWorstThreshold([7, 0, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(slocAnalyzer.isOverWorstThreshold([6, 0, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(slocAnalyzer.isOverWorstThreshold([6, 0, 0, 91], [5, 22, 44, 56]))
        
    def test_isOverSecondThreshold(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertTrue(slocAnalyzer.isOverSecondThreshold([5, 18, 0, 91], [7, 22, 44, 56]))
        self.assertTrue(slocAnalyzer.isOverSecondThreshold([4, 19, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(slocAnalyzer.isOverSecondThreshold([5, 17, 0, 91], [7, 22, 44, 56]))
        self.assertFalse(slocAnalyzer.isOverSecondThreshold([4, 18, 0, 91], [7, 22, 44, 56]))
        
    def test_isOverThirdThreshold(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertTrue(slocAnalyzer.isOverThirdThreshold([5, 17, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(slocAnalyzer.isOverThirdThreshold([7, 15, 23, 91], [7, 22, 44, 56]))
        self.assertTrue(slocAnalyzer.isOverThirdThreshold([1, 1, 43, 91], [7, 22, 44, 56]))
        self.assertFalse(slocAnalyzer.isOverThirdThreshold([4, 18, 22, 91], [7, 22, 44, 56]))
        
    def test_isOneRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertTrue(slocAnalyzer.isOneRateStars([11, 0, 0, 91]))
        self.assertTrue(slocAnalyzer.isOneRateStars([9, 36, 0, 91]))
        self.assertFalse(slocAnalyzer.isOneRateStars([10, 24, 23, 33]))

    def test_isTwoRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertFalse(slocAnalyzer.isTwoRateStars([9, 0, 0, 91]))
        self.assertFalse(slocAnalyzer.isTwoRateStars([7, 0, 0, 91]))
        self.assertFalse(slocAnalyzer.isTwoRateStars([1, 7, 19, 81]))
        self.assertFalse(slocAnalyzer.isTwoRateStars([1, 9, 0, 91]))
        self.assertTrue(slocAnalyzer.isTwoRateStars([10, 24, 23, 80]))

    def test_isThreeRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertTrue(slocAnalyzer.isThreeRateStars([9, 0, 0, 91]))
        self.assertFalse(slocAnalyzer.isThreeRateStars([7, 0, 0, 91]))
        self.assertFalse(slocAnalyzer.isThreeRateStars([1, 9, 0, 91]))
        self.assertFalse(slocAnalyzer.isThreeRateStars([1, 7, 12, 80]))
        self.assertFalse(slocAnalyzer.isThreeRateStars([1, 7, 19, 81]))
        self.assertTrue(slocAnalyzer.isThreeRateStars([4, 23, 28, 80]))
        self.assertTrue(slocAnalyzer.isThreeRateStars([9, 19, 23, 80]))
         
    def test_isFourRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertFalse(slocAnalyzer.isFourRateStars([9, 0, 0, 91]))
        self.assertFalse(slocAnalyzer.isFourRateStars([1, 9, 0, 91]))
        self.assertFalse(slocAnalyzer.isFourRateStars([1, 7, 12, 80]))
        self.assertFalse(slocAnalyzer.isFourRateStars([1, 7, 19, 81]))
        self.assertFalse(slocAnalyzer.isFourRateStars([4, 12, 15, 80]))
        self.assertFalse(slocAnalyzer.isFourRateStars([1, 15, 10, 80]))
        self.assertTrue(slocAnalyzer.isFourRateStars([7, 0, 0, 91]))
        self.assertTrue(slocAnalyzer.isFourRateStars([7, 10, 26, 60]))
 
    def test_isFiveRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertFalse(slocAnalyzer.isFiveRateStars([9, 0, 0, 91]))
        self.assertTrue(slocAnalyzer.isFiveRateStars([5, 0, 0, 91]))
          
    def test_getRateStars(self):
        self.createFramaAnalyzer()
        slocAnalyzer = self.siObj.getFramaSlocAnalyzer()
        self.assertEqual(1, slocAnalyzer.calculateRateStars())


suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaStats)
unittest.TextTestRunner(verbosity=2).run(suite)


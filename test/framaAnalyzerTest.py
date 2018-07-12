import unittest
import framaAnalyzer as fa


class Test_framaStats(unittest.TestCase):

    def setUp(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')

    def tearDown(self):
        pass

    def test_checkFilenameSavedOnConstructor(self):
        self.assertEqual("pippo.txt", self.siObj.getFilename())

    def test_checkFilenameSavedOnConstructorFileNotFound(self):
        self.siObj = fa.framaAnalyzer('pluto.txt')
        self.assertEqual("", self.siObj.getFilename())

    def test_extractSectionFromFile(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.assertEqual(79, self.siObj.extractSectionsFromFile())
        
    def test_getFunctionList(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.assertEqual(79, len(self.siObj.getFunctionObjectList()))
        
    def test_getFunctionListCheckObject(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual("check_num_record", funcList[0].getName())
        self.assertEqual(2, funcList[0].getSloc())
        self.assertEqual(1, funcList[0].getMccabeComplexity())
        self.assertEqual("xmlParse_Startup", funcList[78].getName())
        self.assertEqual(28, funcList[78].getSloc())
        self.assertEqual(7, funcList[78].getMccabeComplexity())

    def test_getTotalSloc(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        funcList = self.siObj.getFunctionObjectList()
        self.assertEqual(1567, self.siObj.getTotalSloc())
        
    def test_getTotalSlocOver60(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSlocOver60()
        self.assertEqual(333, self.siObj.getTotalSlocOver60())
        
    def test_getPercentageSlocOver60(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSlocOver60()
        self.assertEqual(21, self.siObj.getPercentageSlocOver60())
        
    def test_getTotalSloc30To60(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSloc30To60()
        self.assertEqual(290, self.siObj.getTotalSloc30To60())
        
    def test_getPercentageSloc30To60(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSloc30To60()
        self.assertEqual(18, self.siObj.getPercentageSloc30To60())
        
    def test_getTotalSloc15To30(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSloc15To30()
        self.assertEqual(642, self.siObj.getTotalSloc15To30())
        
    def test_getPercentageSloc15To30(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSloc15To30()
        self.assertEqual(40, self.siObj.getPercentageSloc15To30())
        
    def test_getTotalSlocUnder15(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculateTotalSlocUnder15()
        self.assertEqual(302, self.siObj.getTotalSlocUnder15())
        
    def test_getPercentageSlocUnder15(self):
        self.siObj = fa.framaAnalyzer('pippo.txt')
        self.siObj.extractSectionsFromFile()
        self.siObj.calculatePercentageSlocUnder15()
        self.assertEqual(19, self.siObj.getPercentageSlocUnder15())


suite = unittest.TestLoader().loadTestsFromTestCase(Test_framaStats)
unittest.TextTestRunner(verbosity=2).run(suite)


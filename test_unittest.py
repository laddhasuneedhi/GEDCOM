from pickle import TRUE
import sourcecode
import unittest
from datetime import date

class Test_Testsourcecode(unittest.TestCase):
    def test1_us11(self):
        self.assertEqual(sourcecode._us11(["25", "JAN", "1930"],["10", "APR", "1940"],  "@I2@"), [['@I2@' , '1940-04-10','1930-01-25']])
    def test2_us11(self):
        self.assertEqual(sourcecode._us11(["1", "DEC", "2009"],["30", "MAR", "2008"],  "@I2@"), [])
    def test3_us11(self):
        self.assertEqual(sourcecode._us11( ["1", "DEC", "2009"],["30", "MAR", "2010"], "@I6@"), [['@I6@', '2010-03-30', '2009-12-01']])
    def test4_us11(self):
        self.assertEqual(sourcecode._us11(["1", "DEC", "2011"],["30", "MAR", "2010"],  "@I6@"), [])
    def test5_us11(self):
        self.assertEqual(sourcecode._us11( ["31", "MAR", "2010"], [], "@I6@"), [['@I6@','2010-03-31' ,''] ])
        
    def test1_us12(self):
        self.assertEqual(sourcecode._us12( '@I6@', ["31", "MAR", "1990"], '@I7@', ["30", "MAR", "1990"], [['@I8', ["30", "MAY", "2020"]]] ), True)
    def test2_us12(self):
        self.assertEqual(sourcecode._us12( '@I6@', ["31", "MAR", "1910"], '@I7@', ["30", "MAR", "1910"], [['@I8', ["30", "MAY", "2020"]]] ), False)
   
    def test3_us12(self):
        self.assertEqual(sourcecode._us12( '@I8@', ["31", "MAR", "1955"], '@I7@', ["30", "MAR", "1970"], [['@I8', ["30", "MAY", "1990"]], ['@I9', ["30", "MAY", "1991"]]]  ), True)
    
    
if __name__ == '__main__':
    unittest.main()
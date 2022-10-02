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
        
        
if __name__ == '__main__':
    unittest.main()
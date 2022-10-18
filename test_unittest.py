from pickle import TRUE
import sourcecode
import unittest
from datetime import date
gender_dict = {}
gender_dict["@I2@"] = "M"
gender_dict["@I3@"] = "F"
gender_dict["@I4@"] = "F"
sib_list = {}
chil_list = {}
sib_list["@I5@"] = ["@I4@"]
chil_list["@I4@"] = ["@I2@"]
sib_list["@I4@"] = ["@I5@"]
chil_list["@I5@"] = ["@I10@"]
class Test_Testsourcecode(unittest.TestCase):
    def test1_us21(self):
        self.assertEqual(sourcecode._us21("HUSB", "@I2@", gender_dict), "Valid for @I2@")
    def test2_us21(self):
        self.assertEqual(sourcecode._us21("WIFE", "@I2@", gender_dict), "Invalid family role for @I2@")
    def test3_us21(self):
        self.assertEqual(sourcecode._us21("WIFE", "@I3@", gender_dict ), "Valid for @I3@")
    def test4_us21(self):
        self.assertEqual(sourcecode._us21("HUSB", "@I3@", gender_dict), "Invalid family role for @I3@")
    def test5_us21(self):
        self.assertEqual(sourcecode._us21( "WIFE", "@I4@", gender_dict), "Valid for @I4@")
        
    def test1_us20(self):
        self.assertEqual(sourcecode._us20( "@I2@", "@I5@", sib_list, chil_list ), "Marrying your niece or newphew not allowed")
    def test2_us12(self):
        self.assertEqual(sourcecode._us20( "@I4@", "@I10@", sib_list, chil_list ), "Marrying your niece or newphew not allowed" )
   
    def test3_us12(self):
        self.assertEqual(sourcecode._us20( "@I14@", "@I16@", chil_list, sib_list ), "Permittable")
    
    def test4_us12(self):
        self.assertEqual(sourcecode._us20( "@I81@", "@I39@", sib_list, chil_list), "Permittable")
    
    def test5_us12(self):
        self.assertEqual(sourcecode._us20("@I100@", "@I3@" , sib_list, chil_list ), "Permittable")
    
    
if __name__ == '__main__':
    unittest.main()
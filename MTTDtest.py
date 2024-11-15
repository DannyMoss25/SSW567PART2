import unittest
import MRTD

class TestStringMethods(unittest.TestCase):
    #This makes sure that the < is removed from the code, while maintaining the space so the code knows where the first line ends
    def testscanMRZ(self):
        self.assertEqual(MRTD.scanMRZ("SSW<<<<<<<<567<<<<<<"), "SSW567")
        self.assertEqual(MRTD.scanMRZ("SSW 567"), "SSW 567")
        self.assertEqual(MRTD.scanMRZ("SSW <<<<567"), "SSW 567")

    #This checks to make sure the number of characters of the two lines together are the correct length
    def testcheckInput(self):
        self.assertEqual(MRTD.checkInput("aaaaaaaaaaaaaaaaaa"), "INVALID SCAN: NOT ENOUGH CHARACTERS")
        self.assertEqual(MRTD.checkInput("aaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
                                         ), "INVALID SCAN: TOO MANY CHARACTERS")
        self.assertEqual(MRTD.checkInput("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1"), "Good")

    #This makes sure the only valid characters are used
    def testcheckValues(self):
        self.assertEqual(MRTD.checkValues("!@#$%^&*()_+"), "INVALID SCAN: INVALID CHARACTERS")
        self.assertEqual(MRTD.checkValues("5732+"), "INVALID SCAN: INVALID CHARACTERS")
        self.assertEqual(MRTD.checkValues("a93jgse"), "Works Out")
        self.assertEqual(MRTD.checkValues("awmvs"), "Works Out")
        self.assertEqual(MRTD.checkValues("42351"), "Works Out")

    # This returns the second line
    def testgetSecond(self):
        self.assertEqual(MRTD.getSecond("Test SSW567"), "SSW567")
        self.assertEqual(MRTD.getSecond("SSW567 Test"), "Test")
        self.assertEqual(MRTD.getSecond("First Second"), "Second")

    #This gets the digits from the list
    def testgetDigits(self):
        self.assertEqual(MRTD.getDigits("L898902C36UT07408122F1204159ZE184226B1"), ['6', '2', '9', '1'])
        self.assertEqual(MRTD.getDigits("L898902C32UT07408123F1204154ZE184226B6"), ['2', '3', '4', '6'])

    # This is a mock database request. The True is for debugging mode. if true, it just assumes every name is valid
    def testdatabaseRequestMRZ(self):
        self.assertEqual(MRTD.databaseRequest("MOSSDANNY", True), "Good, Return Original")
        self.assertEqual(MRTD.databaseRequest("FROSTDAVE", True), "Good, Return Original")
        self.assertEqual(MRTD.databaseRequest("PUTOLINCOLNABRAHAM", True), "Good, Return Original")
        self.assertEqual(MRTD.databaseRequest("PUTOLINCOLNABRAHAM", False), "THIS IS A FAKE ID, REPORT IT IMMEDIATELY")
    #This returns the second line if the name is valid
    def testgetDatabase(self):
        self.assertEqual(MRTD.getDatabase("SSW 567", True), "567")
        self.assertEqual(MRTD.getDatabase("Danny Moss", True), "Moss")
        self.assertEqual(MRTD.getDatabase("PUTOLINCOLNABRAHAM a84932", True), "a84932")
        self.assertEqual(MRTD.getDatabase("PUTOLINCOLNABRAHAM a84932", False), "THIS IS A FAKE ID, REPORT IT IMMEDIATELY")
    #this returns the mod
    def testgetMod(self):
        self.assertEqual(MRTD.getMod(22), 2)
        self.assertEqual(MRTD.getMod(5551), 1)
        self.assertEqual(MRTD.getMod(934925), 5)
        self.assertEqual(MRTD.getMod(13491048123), 3)
        self.assertEqual(MRTD.getMod(49496), 6)

    # this is the fletcher16 program
    def testfletcher16(self):
        self.assertEqual(MRTD.fletcher16("SSW567"), 13728)
        self.assertEqual(MRTD.fletcher16("Fletcher"), 54064)
        self.assertEqual(MRTD.fletcher16("Security314"), 43763)

    # this splits the string into the non-security parts
    def testsplitTheString(self):
        self.assertEqual(MRTD.splitTheString("L898902C36UT07408122F1204159ZE184226B1"), ['L898902C3', '740812', '120415', 'ZE184226B'])
        self.assertEqual(MRTD.splitTheString("L898902C32UT07408123F1204154ZE184226B6"), ['L898902C3', '740812', '120415', 'ZE184226B'])
        self.assertEqual(MRTD.splitTheString("aaaaaaaaa2bbbbbbbbb3ccccccc4ddddddddd6"),
                         ['aaaaaaaaa', 'bbbbbb', 'cccccc', 'ddddddddd'])
    #This cross compares the found security numbers and info.
    def testsecurityCheck(self):
        self.assertEqual(MRTD.securityCheck([1,2,3,4],[1,2,3,4],["aaa","bbb","ccc","ddd"],["aaa","bbb","ccc","ddd"]), "Record came up clean")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 2, 3, 5], ["aaa", "bbb", "ccc", "ddd"], ["aaa", "bbb", "ccc", "ddd"]).replace("\n", ""),
            "PERSONAL NUMBER SECURITY NUMBER FAILED: Expected: 5 Received: 4")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 5, 4], [1, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "bbb", "ccc", "ddd"]).replace("\n", ""),
            "EXPIRATION DATE SECURITY NUMBER FAILED: Expected: 3 Received: 5")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 5, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "bbb", "ccc", "ddd"]).replace("\n", ""),
            "DATE OF BIRTH SECURITY NUMBER FAILED: Expected: 5 Received: 2")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [5, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "bbb", "ccc", "ddd"]).replace("\n", ""),
            "Passport Number SECURITY NUMBER FAILED: Expected: 5 Received: 1")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["eee", "bbb", "ccc", "ddd"]).replace("\n", ""),
            "Passport Number FIELD FAILED: Expected: eee Received: aaa")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "eee", "ccc", "ddd"]).replace("\n", ""),
            "DATE OF BIRTH FIELD FAILED: Expected: eee Received: bbb")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "bbb", "eee", "ddd"]).replace("\n", ""),
            "EXPIRATION DATE FIELD FAILED: Expected: eee Received: ccc")
        self.assertEqual(
            MRTD.securityCheck([1, 2, 3, 4], [1, 2, 3, 4], ["aaa", "bbb", "ccc", "ddd"],
                               ["aaa", "bbb", "ccc", "eee"]).replace("\n", ""),
            "PERSONAL NUMBER FIELD FAILED: Expected: eee Received: ddd")

    #This puts it all together from start to finish
    def testTotal(self):
        self.assertEqual(MRTD.FULLSYSTEM("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C36UT07408122F1204159ZE184226B<<<<<<1", True).replace("\n", ""), "Passport Number SECURITY NUMBER FAILED: Expected: 2 Received: 6DATE OF BIRTH SECURITY NUMBER FAILED: Expected: 3 Received: 2EXPIRATION DATE SECURITY NUMBER FAILED: Expected: 4 Received: 9PERSONAL NUMBER SECURITY NUMBER FAILED: Expected: 6 Received: 1")
        self.assertEqual(MRTD.FULLSYSTEM("P<UTOERIKSSON<<ANNA<MARIA<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6", False).replace("\n", ""), "Record came up clean")
        self.assertEqual(MRTD.FULLSYSTEM("P<USALINCOLN<<ABRAHAM<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6", False), 'INVALID SCAN: NOT ENOUGH CHARACTERS')
        self.assertEqual(MRTD.FULLSYSTEM("P<USALINCOLN<<ABRAHAM<<<<<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6", False),'THIS IS A FAKE ID, REPORT IT IMMEDIATELY')
        self.assertEqual(MRTD.FULLSYSTEM("P<USALINCOLN<<ABRAHAM<<<<<<<<<<<<<<<<<< L898902C32UT07408123F1204154ZE184226B<<<<<<6",True), 'Record came up clean')

if __name__ == '__main__':
    unittest.main()
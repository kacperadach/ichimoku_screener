# adding this because my run config is not working
import unittest
from os import path, listdir
from TestingConstants import BASE_PATH, SPECIFIC_PATH

suite = unittest.TestSuite()

def _get_all_testing_files_in_temp():
    return [f for f in listdir(BASE_PATH) if path.isfile(path.join(BASE_PATH, f)) and f[0:5] == 'Test_']

if __name__ == "__main__":
    all_files = _get_all_testing_files_in_temp()
    for test_file in all_files:
        test_file = test_file.split('.')[0]
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(test_file))
    unittest.TextTestRunner().run(suite)

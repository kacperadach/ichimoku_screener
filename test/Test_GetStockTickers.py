import unittest
from os import path, mkdir, listdir, environ
from shutil import rmtree

environ['TESTING'] = 'True'

from TestingConstants import TEMP_PATH, SPECIFIC, SPECIFIC_PATH, BASE_PATH
from GetStockTickers import _write_all_tickers_from_ftp, \
    _pull_all_tickers_from_file, \
    _filter_all_tickers, \
    get_all_tickers_from_ftp, \
    get_all_tickers_from_api, \
    extract_tickers_from_api_response

class TestGetStockTickers(unittest.TestCase):

    def setUp(self):
        if path.exists(TEMP_PATH):
            rmtree(TEMP_PATH)
        mkdir(TEMP_PATH)

    def tearDown(self):
        rmtree(TEMP_PATH)

    def _get_all_files_in_temp(self):
        return [f for f in listdir(TEMP_PATH) if path.isfile(path.join(TEMP_PATH, f))]

    def _write_temp_file(self):
        with open(path.join(BASE_PATH, SPECIFIC_PATH), 'w') as f:
            f.writelines(('test|abc\n', 'test2&cba\n', 'test3|asdda\n', 'SYMBOL|not_reached\n'))

    def test_write_all_tickers_from_ftp(self):
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 0)
        _write_all_tickers_from_ftp(BASE_PATH, SPECIFIC_PATH)
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 1)
        with open(path.join(BASE_PATH, SPECIFIC_PATH), 'r') as f:
            lines = f.readlines()
        self.assertTrue(len(lines) > 100)

    def test_pull_all_tickers_from_file(self):
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 0)
        self._write_temp_file()
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 1)
        all_tickers = _pull_all_tickers_from_file(BASE_PATH, SPECIFIC_PATH)
        self.assertTrue(len(all_tickers) == 2)
        self.assertTrue('test' in all_tickers and 'test3' in all_tickers)

    def test_filter_all_tickers(self):
        ticker_list = ('BBA', 'ABC^D', 'BRK.A', 'POP', '$CGIX')
        filtered_list = _filter_all_tickers(ticker_list)
        self.assertTrue(len(filtered_list) == 2)

    def test_get_all_tickers_from_ftp(self):
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 0)
        all_tickers = get_all_tickers_from_ftp(BASE_PATH, SPECIFIC_PATH)
        self.assertTrue(len(all_tickers) > 5000)

    def test_get_all_tickers_from_api(self):
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 0)
        all_tickers = get_all_tickers_from_api(file_path=path.join(BASE_PATH, SPECIFIC))
        self.assertTrue(len(all_tickers) > 3000)
        tempDirFiles = self._get_all_files_in_temp()
        self.assertTrue(len(tempDirFiles) == 3)

if __name__ == '__main__':
    unittest.main()

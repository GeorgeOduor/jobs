import unittest
import pandas as pd
from googledrive.drivetools import DriveTools

class TestDriveTools(unittest.TestCase):
    def setUp(self):
        self.creds_file = 'googledrive/searchconsole-364317-ee5fb100ebef.json'
        self.workbook = 'WebResults'
        self.dt = DriveTools(self.creds_file, self.workbook)

    def test_write_df(self):
        df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        sheet_index = 0
        self.dt.write_df(df, sheet_index)
        # Assert that data has been written to the sheet
        sheet = self.dt.gc1.open(self.workbook).get_worksheet(sheet_index)
        self.assertEqual(sheet.cell(1, 1).value, 1)
        self.assertEqual(sheet.cell(2, 1).value, 2)
        self.assertEqual(sheet.cell(1, 2).value, 3)
        self.assertEqual(sheet.cell(2, 2).value, 4)

    def test_get_existing_jobs(self):
        sheet_index = 0
        existing_jobs = self.dt.get_existing_jobs(sheet_index)
        # Assert that existing jobs is not None
        self.assertIsNotNone(existing_jobs)

if __name__ == '__main__':
    unittest.main()

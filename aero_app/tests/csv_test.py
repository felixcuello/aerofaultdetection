import os
import sys
import unittest
from pandas import Timestamp

# Add the parent directory of the lib directory to the module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from lib.csv import CSV

class TestCSV(unittest.TestCase):

    def setUp(self):
        input_data = "./tests/test_input.csv"
        self.csv = CSV(input_data)

    def test_to_df(self):
        # Check that we parse the header CSV columns
        self.assertEqual(self.csv.to_df().columns[0], 'datetime')                          # 1st column
        self.assertEqual(self.csv.to_df().columns[1], 'V1;wind_speed;Avg (m/s)')           # 2nd column
        self.assertEqual(self.csv.to_df().columns[95], 'V9;wind_speed_vert;Min (m/s)')     # 95th column

        # Check we parse the values correctly
        row = self.csv.to_df().iloc[4]
        self.assertEqual(row['datetime'], Timestamp('2022-02-02 02:40:00'))
        self.assertEqual(row['V1;wind_speed;Max (m/s)'], 1.0001)
        self.assertEqual(row['V;channel;Max (V)'], 11.56)


if __name__ == '__main__':
    unittest.main()

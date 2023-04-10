import csv
import logging
import pandas as pd
from datetime import datetime

class CSV:
    def __init__(self, csv_file):
        logging.debug("Reading {}".format(csv_file))
        self.df = pd.read_csv(csv_file, sep=',')

        #  Apply conversion functions to the columns that require a particular adjustment
        # --------------------------------------------------------------------------------------
        self.df['datetime'] = self.df['datetime'].apply(lambda datetime_string: datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S"))

    def to_df(self):
        return self.df

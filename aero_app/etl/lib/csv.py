import csv
import uuid
import logging

DELIMITER = ','

def process_header(header):
    logging.debug("Processing CSV header")
    print(header)


def process_csv(db_connection, file_name : str):
    logging.info("Processing -> {}".format(file_name))

    tower_id = None
    tower_uuid = str(uuid.uuid4())

    data = open(file_name)
    csv_reader = csv.reader(data, delimiter=DELIMITER)
    header = process_header(next(csv_reader))

    # CSV format is:
    # col   | description
    # ------+------------------------
    # 0     | tower_id
    # 1     | datetime
    # 2..n  | devices
    for csv_row in csv_reader:
        if tower_id == None:
            tower_id = csv_row[0]

    logging.debug("Finished reading CSV")

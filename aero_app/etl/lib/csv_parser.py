import re
import csv
import uuid
import logging

class CsvParser:
    def __init__(self, db_connection, delimiter = ','):
        self.db_connection = db_connection
        self.delimiter = delimiter

    #  Process the CSV header since it's complex
    # ---------------------------------------------------------------
    def __process_header(self, header):
        logging.debug("Processing CSV header")

        processed_header = [{'type': 'datalogger_id'},{'type': 'datetime'}]

        for i in range(2, len(header)):
            col = header[i]
            subcol = col.split(";")

            sensor = re.findall(r"^([a-zA-Z]+?)\s*(\d*)$", subcol[0])
            sensor_type = sensor[0][0]   # Sensor type
            sensor_seq = sensor[0][1]    # Sensor sequential number in the weather station

            measurement = subcol[1]
            unit = subcol[2]

            processed_header.append({
                'sensor_id': subcol[0].lower(),
                'sensor_type': sensor_type.lower(),
                'sensor_seq': sensor_seq.lower(),
                'measurement_type': measurement.lower(),
                'measurement_unit': unit.lower()
            })

        return processed_header


    #  Process each CSV row
    # ---------------------------------------------------------------
    def __process_csv_row(self, csv_row, datalogger_uuid, header_info):
        datalogger_id = csv_row[0]
        datetime = csv_row[1]
        sensors = {}
        for col in range(2, len(header_info)):
            sensor_id = header_info[col]['sensor_id']
            type = header_info[col]['sensor_type']
            seq = header_info[col]['sensor_seq']

            match type:
                case "anemometro":
                    print("")
                case "kpc":
                    print("")
                case "barometro":
                    print("")
                case "veleta":
                    print("")
                case "a":
                    print("")
                case "c":
                    print("")
                case "d":
                    print("")
                case "i":
                    print("")
                case "t":
                    print("")
                case "v":
                    print("")
                case _:
                    logging.critical("!!!!!! Unknown type => {}".format(type))
                    raise("Unknown type")


    #  Process the CSV file
    # ---------------------------------------------------------------
    def process_csv(self, file_name : str):
        logging.info("Processing -> {}".format(file_name))

        datalogger_uuid = str(uuid.uuid4())

        data = open(file_name)
        csv_reader = csv.reader(data)
        header_information = self.__process_header(next(csv_reader))

        # CSV format is:
        # col   | description
        # ------+------------------------
        # 0     | datalogger_id
        # 1     | datetime
        # 2..n  | sensors measurements
        for csv_row in csv_reader:
            self.__process_csv_row(csv_row, datalogger_uuid, header_information)

        logging.debug("Finished reading CSV")

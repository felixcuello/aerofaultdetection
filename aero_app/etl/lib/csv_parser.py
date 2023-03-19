import re
import csv
import uuid
import logging

class CsvParser:
    def __init__(self, db_connection, delimiter = ','):
        self.db_connection = db_connection
        self.delimiter = delimiter
        self.sensor_uuids = {}
        self.sample_type_uuids = {}

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
    def __process_csv_row(self, csv_row, header_info):
        datalogger_id = csv_row[0]
        datetime = csv_row[1]

        #  Process all samples in that row (each column)
        # ------------------------------------------------------------
        for col in range(2, len(header_info)):
            cursor = self.db_connection.cursor()

            sensor_id = header_info[col]['sensor_id']
            sensor_type = header_info[col]['sensor_type']
            sensor_seq = header_info[col]['sensor_seq']
            if sensor_seq == '':
                sensor_seq = 0

            #  Create a new sensor if it wasn't created already
            # ---------------------------------------------------------
            if sensor_id not in self.sensor_uuids.keys():
                sensor_uuid = str(uuid.uuid4())
                self.sensor_uuids[sensor_id] = sensor_uuid

                logging.debug('Creating a new sensor => "{} {}" [{}]'.format(sensor_type, sensor_seq, sensor_uuid))
                cursor.execute(
                    "INSERT INTO aero_sensor (uuid, datalogger_id, sensor_type, sensor_seq)"
                    " VALUES "
                    "(%s, %s, %s, %s)",
                    (sensor_uuid, datalogger_id, sensor_type, sensor_seq)
                )
            else:
                sensor_uuid = self.sensor_uuids[sensor_id]

            #  Create new sample type if required
            # ---------------------------------------------------------
            sample_type = header_info[col]['measurement_type']
            sample_unit = header_info[col]['measurement_unit']
            sample_type_id = "{} {}".format(sample_type, sample_unit)
            sample_value = None if csv_row[col] == 'None' else float(csv_row[col])
            if sample_type_id not in self.sample_type_uuids.keys():
                sample_type_uuid = str(uuid.uuid4())
                self.sample_type_uuids[sample_type_id] = sample_type_uuid

                logging.debug('Creating a new sample type => "{} {}"'.format(sample_type, sample_unit))
                cursor.execute(
                    "INSERT INTO aero_sample_type(uuid, sensor_uuid, sample_type, sample_unit)"
                    " VALUES "
                    "(%s, %s, %s, %s)",
                    (sample_type_uuid, sensor_uuid, sample_type, sample_unit)
                )
            else:
                sample_type_uuid = self.sample_type_uuids[sample_type_id]

            #  Create new sample for this column
            # ---------------------------------------------------------
            cursor.execute(
                "INSERT INTO aero_sample (datetime, sample_type_uuid, sample_value)"
                " VALUES "
                "(%s, %s, %s)",
                (datetime, sample_type_uuid, sample_value)
            )

            self.db_connection.commit()


    #  Process the CSV file
    # ---------------------------------------------------------------
    def process_csv(self, file_name : str):
        logging.info("Processing -> {}".format(file_name))

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
            self.__process_csv_row(csv_row, header_information)

        logging.debug("Finished reading CSV")

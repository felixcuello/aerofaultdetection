import os
import sys
import logging

from lib.pgdb import db_conn
from lib.csv import process_csv

#  Setting the log level
# ---------------------------------------------------------
os_log_level = os.environ['LOG_LEVEL'] if os.environ['LOG_LEVEL'] != None else 'INFO'
logging.root.setLevel(os_log_level)


#  Hash with the available ETLs
# ---------------------------------------------------------
etl = {
    "csv": lambda file_name : process_csv(db_conn, file_name)
}


#  Usage format
# ---------------------------------------------------------
def print_usage():
    print("")
    print("{} <file_type> <file_name>".format(sys.argv[0]))
    print("")


#  Main program
# ---------------------------------------------------------
argc = len(sys.argv)
if(argc != 3):
    print_usage()
    quit()

file_type = sys.argv[1]
file_name = sys.argv[2]
if(file_type in etl):
    etl[file_type](file_name)
else:
    print("")
    print("ERROR: '{}' is not a valid file format".format(file_type))
    print("")
    print("Available types")
    for key in etl.keys():
        print(">> '{}'".format(key))
    print("")

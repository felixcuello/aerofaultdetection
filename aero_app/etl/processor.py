import sys

from lib.pgdb import db_conn
from lib.npg1 import process_npg1

#  Hash with the available ETLs
# ---------------------------------------------------------
etl = {
    "npg1": lambda file_name : process_npg1(db_conn, file_name)
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

import os
import psycopg2

db_conn = psycopg2.connect("host={} dbname={} user={} password={}".
                           format(
                               os.environ['POSTGRES_HOST'],
                               os.environ['POSTGRES_DB'],
                               os.environ['POSTGRES_USER'],
                               os.environ['POSTGRES_PASSWORD']
                           ))

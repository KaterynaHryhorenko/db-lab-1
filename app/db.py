import time

import psycopg2

from .config import (DB_HOST, DB_PORT, DB_USER,
                     DB_PASS, DB_NAME)


class DataBase:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect_db(self):
        while True:
            try:
                connection = psycopg2.connect(
                    host=DB_HOST,
                    port=DB_PORT,
                    database=DB_NAME,
                    user=DB_USER,
                    password=DB_PASS
                )
                break
            except psycopg2.OperationalError as err:
                print(err)
                print(
                    'The next attempt to connect to the database will be in 5 seconds.\n'
                )

                time.sleep(5)

        self.connection = connection
        self.cursor = connection.cursor()

    def create_table(self):
        with open('schema.sql', 'r', encoding='utf-8') as f:
            sql = f.read()

        self.cursor.execute(sql)
        self.connection.commit()

    def load_csv_to_db(self, csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                sql = """
                    COPY zno 
                    FROM STDIN 
                        DELIMITER ';' 
                        CSV 
                        HEADER
                        NULL 'null' 
                        QUOTE '"' 
                    ;
                """
                self.cursor.execute('BEGIN')
                self.cursor.copy_expert(sql, f)
                self.cursor.execute('COMMIT')

            print(f'Data from {csv_file} is successfully loaded to database.')

        except psycopg2.DataError as err:
            print(err)
            print(f'DataError - The data from {csv_file} will be rolled back.')

            self.connection.rollback()

    def get_statistic(self):
        self.cursor.execute("""
            SELECT 
                regname,
                year, 
                MAX(ukrball100) as ukrbal100
            FROM zno
            WHERE 
                ukrteststatus = 'Зараховано'
            GROUP BY
                year,
                regname
            ;
        """)

        return self.cursor.fetchall()

    def close(self):
        if self.cursor is not None:
            self.cursor.close()

        if self.connection is not None:
            self.connection.close()

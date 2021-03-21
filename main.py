import csv
import os

from app.downloader import Downloader
from app.extracter import Extracter
from app.db import DataBase
from app.config import YEARS, STATISTIC_CSV


def write_statistic_to_csv(statistic):
    with open(STATISTIC_CSV, 'w') as f:
        header = ['RegName', 'Year', 'MaxUkrBal100']

        writer = csv.writer(f)

        writer.writerow(header)
        writer.writerows(statistic)


def main():
    downloader = Downloader()
    extracter = Extracter()
    db = DataBase()

    archives = list()
    csv_files = list()
    # csv_files = ['CleanOdata2019File.csv', 'CleanOdata2020File.csv']

    for year in YEARS:
        print(f'Starting to download ZNO data for {year} year.')
        archive = downloader.download(year)
        print(f'{archive} is successfully downloaded.')
        archives.append(archive)

    for archive in archives:
        csv_file = extracter.extract(archive)
        print(f'{csv_file} is successfully extracted from {archive}.')
        os.remove(archive)
        print(f'{archive} is successfully remowed.')
        clean_csv_file = extracter.clean(csv_file)
        print(f"{csv_file} is successfully cleaned. \n (cp1251 -> utf-8, ',' -> '.')")
        csv_files.append(clean_csv_file)

    db.connect_db()
    print('Successfully connected to database.')
    db.create_table()
    print('ZNO table is created.')

    for csv_file in csv_files:
        db.load_csv_to_db(csv_file)
        os.remove(csv_file)
        print(f'{csv_file} is successfully remowed.')

    statistic = db.get_statistic()
    write_statistic_to_csv(statistic)
    print('Statistic is successfully loaded to csv file.')

    db.close()
    print('Database is closed.')


if __name__ == "__main__":
    main()

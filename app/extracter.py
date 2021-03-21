import os
import re

import py7zr

from .config import SIMULATE_ERROR, SIMULATE_ERROR_YEAR


class Extracter:
    def _get_csv_name(self, archive):
        csv_file = archive.split('.')[0][-4:]

        return f'Odata{csv_file}File.csv'

    def extract(self, archive):
        csv_file = self._get_csv_name(archive)

        with py7zr.SevenZipFile(archive, 'r') as a:
            a.extract(targets=[csv_file])

        return csv_file

    def clean(self, csv_file):
        path_to_clean_csv = 'Clean' + csv_file

        year = csv_file.split('.')[0][-8:-4]

        with open(csv_file, 'r', encoding='cp1251') as input_f:
            with open(path_to_clean_csv, 'w', encoding='utf-8') as output_f:
                for line in input_f:
                    # add column - year and convert commas to dots
                    output_f.write(
                        ';'.join(
                            [year, re.sub(',', '.', line)]
                        )
                    )

                # simulation of an error
                if year == str(SIMULATE_ERROR_YEAR) and SIMULATE_ERROR:
                    # writes not correct data
                    output_f.write(
                        '123;123;123;123;;;;'
                    )

        os.remove(csv_file)

        return path_to_clean_csv

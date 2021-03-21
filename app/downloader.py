import time

import requests

from .config import URL


class Downloader:
    def __init__(self):
        self.url = URL

    def _get_full_url(self, year):
        url = f'{self.url}OpenDataZNO{year}.7z'

        return url

    def _get_archive_name(self, url):
        archive = url.split('/')[-1]

        return archive

    def download(self, year):
        url = self._get_full_url(year)
        file = self._get_archive_name(url)

        while True:
            try:
                r = requests.get(url, stream=True)

                with open(file, "wb") as f:
                    for chunk in r.iter_content(chunk_size=2*1024):
                        f.write(chunk)
                break

            except requests.exceptions.ConnectionError as err:
                print(err)
                print(
                    'The next attempt to connect to the network will be in 5 seconds.\n'
                )
                time.sleep(5)

        return file

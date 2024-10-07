"""
Due too YT slow down in <country>, save YT links and target files, not dload
"""

from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import logger, Verbosity
import csv


class YTPostponedDownloader(AbstractDownloader):
    def download(self) -> None:
        logger.print(Verbosity.INFO,
                     'Saving YT link {} and target {}'.format(self.url, self.output_path))
        with open('YTPostponedDownloader.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([self.url, self.output_path])

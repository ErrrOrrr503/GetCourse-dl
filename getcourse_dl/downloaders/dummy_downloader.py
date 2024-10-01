"""
Just reporting dloader, for demonstation
"""

from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import logger, Verbosity


class DummyDownloader(AbstractDownloader):
    def download(self) -> None:
        logger.print(Verbosity.INFO,
                     'Dummy downloading file from {} and saving to {}'.format(self.url, self.output_path))

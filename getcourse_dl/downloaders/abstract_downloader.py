from abc import ABC, abstractmethod


class DownloaderException(Exception):
    """ Allow user to do error handling """


class AbstractDownloader(ABC):
    url: str
    output_path: str

    def __init__(self, url: str, output_path: str) -> None:
        self.url = url
        self.output_path = output_path

    @abstractmethod
    def download(self):
        """ perform dload """

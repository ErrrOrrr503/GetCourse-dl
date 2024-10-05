from abc import ABC, abstractmethod
from dataclasses import dataclass
from getcourse_dl.network_wrapper.nwrap import nwrap


class ParserException(Exception):
    """ Allow user to do error handling """


@dataclass
class Link:
    url: str
    name: str

    def __repr__(self) -> str:
        return 'Link({}, {})'.format(self.url, self.name)


class AbstractParser(ABC):
    page: str = ''
    link: Link

    def __init__(self, link: Link, page: str | None = None) -> None:
        """ spesify page to skip download """
        self.link = link
        if page:
            self.page = page

    def get(self) -> None:
        try:
            response = nwrap.get(self.link.url)
        except Exception as e:
            raise ParserException('Getting page failed due to: ' + str(e))
        if response.status_code != 200:
            raise ParserException('Getting page failed, status: ' +
                                  str(response.status_code))
        self.page = response.text

    def parse(self) -> list[Link]:
        """ parse_page wrapper """
        if len(self.page) == 0:
            self.get()
        return self._parse_page()

    @abstractmethod
    def _parse_page(self) -> list[Link]:
        """ actual user-defined parsing """

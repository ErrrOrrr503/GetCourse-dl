"""
find yt link in fact
"""

from getcourse_dl.parsers.abstract_parser import (AbstractParser,
                                                  ParserException,
                                                  Link)
from getcourse_dl.logger.logger import logger, Verbosity
from bs4 import BeautifulSoup, Tag


class YTParser(AbstractParser):
    def _parse_page(self) -> list[Link]:
        soup = BeautifulSoup(self.page, 'html.parser')
        links: list[Link] = []
        iframe = soup.find('iframe')
        if not isinstance(iframe, Tag):
            raise ParserException('iframe')
        header = soup.find('h2', attrs={'class': 'lesson-title-value'})
        if not isinstance(header, Tag):
            raise ParserException('header')
        hdr = header.string
        url = iframe['src']
        if not ('youtube' in url):
            raise ParserException('Unsupported iframe src')
        if not isinstance(hdr, str) or not isinstance(url, str):
            raise ParserException('Shold be literally impossible')
        links.append(Link(url, hdr))
        logger.print(Verbosity.INFO,
                     'YTParser: extracted {}'.format(links[0]))
        return links

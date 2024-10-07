from getcourse_dl.parsers.abstract_parser import (AbstractParser,
                                                  ParserException,
                                                  Link)
from getcourse_dl.logger.logger import logger, Verbosity
from getcourse_dl.network_wrapper.nwrap import nwrap
from bs4 import BeautifulSoup, Tag
import re


class M3U8PlaylistParser(AbstractParser):
    _pattern = re.compile(r'"masterPlaylistUrl":"(.*?)"')

    def _parse_page(self) -> list[Link]:
        soup = BeautifulSoup(self.page, 'html.parser')
        links: list[Link] = []
        iframe = soup.find('iframe')
        if not isinstance(iframe, Tag):
            raise ParserException('iframe')
        src = iframe['src']
        if not isinstance(src, str):
            raise ParserException('Shold be literally impossible')
        if not ('getcourse' in src):
            raise ParserException('Unsupported iframe src')
        try:
            response = nwrap.get(src)
        except Exception as e:
            raise ParserException(
                'Getting playlist-resp failed due to: ' + str(e))
        if response.status_code != 200:
            raise ParserException('Getting playlist-resp failed, status: ' +
                                  str(response.status_code))

        playlist_page = response.text
        match = self._pattern.search(playlist_page)
        if not match:
            raise ParserException('Re match failed. Wrong ans or regex.')
        url = match.group(1).replace('\\', '')

        header = soup.find('h2', attrs={'class': 'lesson-title-value'})
        if not isinstance(header, Tag):
            raise ParserException('header')
        hdr = header.string
        if not isinstance(hdr, str):
            raise ParserException('Shold be literally impossible')

        links.append(Link(url, hdr))
        logger.print(Verbosity.INFO,
                     'M3U8PlaylistParser: extracted {}'.format(links[0]))
        return links

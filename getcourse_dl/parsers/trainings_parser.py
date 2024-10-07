from getcourse_dl.parsers.abstract_parser import (AbstractParser,
                                                  ParserException,
                                                  Link)
from getcourse_dl.logger.logger import logger, Verbosity
from bs4 import BeautifulSoup, Tag


class TrainingsParser(AbstractParser):
    def _parse_page(self) -> list[Link]:
        soup = BeautifulSoup(self.page, 'html.parser')
        links: list[Link] = []
        table = soup.find('table', attrs={'class': 'stream-table'})
        if not table:
            raise ParserException('table not found')
        # body = table.find('tbody')
        # if not isinstance(body, Tag):
        #    raise ParserException('smth wrong with table_body')
        # rows = body.find_all('tr')
        if not isinstance(table, Tag):
            raise ParserException('smth wrong with table')
        rows = table.find_all('tr')
        for row in rows:
            url = 'https://dmdev.getcourse.ru' + row.find('a')['href']
            name = row.find('span', attrs={'class': 'stream-title'}).string
            link = Link(url, name)
            logger.print(Verbosity.INFO,
                         'TrainingsParser: extracted {}'.format(link))
            links.append(link)
        return links

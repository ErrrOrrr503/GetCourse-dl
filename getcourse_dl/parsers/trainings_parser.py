from getcourse_dl.parsers.abstract_parser import (AbstractParser,
                                                  ParserException,
                                                  Link)
from bs4 import BeautifulSoup, Tag


class TrainingsParser(AbstractParser):
    def _parse_page(self) -> list[Link]:
        soup = BeautifulSoup(self.page, 'html.parser')
        links: list[Link] = []
        table = soup.find('table', attrs={'class': 'stream-table'})
        if not table:
            raise ParserException('table not found')
        body = table.find('tbody')
        if not isinstance(body, Tag):
            raise ParserException('smth wrong with table_body')
        rows = body.find_all('tr')
        for row in rows:
            links.append(Link(url=row.find('a')['href'].string,
                              name=row.find('span', attrs={'class': 'stream-title'}).string))
        return links

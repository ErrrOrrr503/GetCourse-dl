from getcourse_dl.parsers.abstract_parser import (AbstractParser,
                                                  ParserException,
                                                  Link)
from getcourse_dl.logger.logger import logger, Verbosity
from bs4 import BeautifulSoup, Tag


class LessonsParser(AbstractParser):
    def _parse_page(self) -> list[Link]:
        soup = BeautifulSoup(self.page, 'html.parser')
        links: list[Link] = []
        lesson_list = soup.find('ul', attrs={'class': 'lesson-list'})
        if not isinstance(lesson_list, Tag):
            raise ParserException('lesson-list not found')
        lessons = lesson_list.find_all('li')
        for lesson in lessons:
            url = 'https://dmdev.getcourse.ru' + lesson.find('a')['href']
            if not url or len(url) == 0:
                raise ParserException('url')
            name = lesson.find(
                'div', attrs={'class': 'link title'}).text.strip().split('\t')[0]
            if not name or len(name) == 0:
                raise ParserException('name')
            link = Link(url, name)
            logger.print(Verbosity.INFO,
                         'LessonsParser: extracted {}'.format(link))
            links.append(link)
        return links

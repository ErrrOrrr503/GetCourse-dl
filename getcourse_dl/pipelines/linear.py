""" plain linear single thread impl """

from getcourse_dl.pipelines.abstract_pypline import AbstractPipeline, PipelineTree
from getcourse_dl.parsers.abstract_parser import AbstractParser, Link, ParserException
from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import Verbosity, logger
import os


class LinearPipeline(AbstractPipeline):
    def run(self) -> None:
        self._iterate_tree_deep(self.tree, '', [self.startpoint], [None])

    def _iterate_tree_deep(self,
                           node: PipelineTree,
                           path: str,
                           links: list[Link],
                           pages: list[str | None]) -> tuple[bool, list[None | str]]:
        saved_pages: list[str | None] = [None] * len(links)
        success = True
        for i, link in enumerate(links):
            page = pages[i]
            executor_type = node.item
            if issubclass(executor_type, AbstractParser):
                parser = executor_type(link=link, page=page)
                parsed_links = []
                try:
                    parsed_links = parser.parse()
                except ParserException as e:
                    logger.print(Verbosity.WARNING, 'link {} failed to be parsed with {}.\n\tcause: {}'.format(
                        link.url, parser, str(e)))
                    if parser.page:
                        logger.print(Verbosity.WARNING, 'dumping webpage')
                        logger.dump_webpage(parser.page, link.url)
                        saved_pages[i] = parser.page
                    success = False
                    continue
                saved_pages[i] = parser.page
                # now call lower level
                next_path = os.path.join(path, link.name)
                children = node.children()
                next_node = next(children)
                lower_success, lower_saved_pages = self._iterate_tree_deep(next_node,
                                                                           next_path,
                                                                           parsed_links,
                                                                           [None] * len(parsed_links))
                if lower_success is True:
                    continue
                for next_node in children:
                    lower_success, _ = self._iterate_tree_deep(next_node,
                                                               next_path,
                                                               parsed_links,
                                                               lower_saved_pages)
                    if lower_success is True:
                        break
                success = lower_success
            elif issubclass(executor_type, AbstractDownloader):
                output_path = os.path.join(path, link.name)
                self.mkpath_for(output_path)
                downloader = executor_type(url=link.url,
                                           output_path=output_path)
                try:
                    downloader.download()
                except DownloaderException as e:
                    logger.print(Verbosity.WARNING, 'download from {} failed with {}.\n\tcause: {}'.format(
                        link.url, downloader, str(e)))
                    success = False
                    continue
            else:
                raise Exception(
                    'This must be unreachable. Dramatic flaw in code')
        return success, saved_pages

    @staticmethod
    def mkpath_for(file_path: str) -> None:
        dir = os.path.dirname(file_path)
        os.makedirs(dir, exist_ok=True)

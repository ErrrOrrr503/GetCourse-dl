""" plain linear single thread impl """

from getcourse_dl.pipelines.abstract_pypline import AbstractPipeline, PipelineTree
from getcourse_dl.parsers.abstract_parser import AbstractParser, Link, ParserException
from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import Verbosity, logger
import os


class LinearPipeline(AbstractPipeline):
    def run(self) -> None:
        self._iterate_tree_deep(self.tree, '', [self.startpoint])

    def _iterate_tree_deep(self, node: PipelineTree, path: str, links: list[Link], page: str | None = None) -> None | str:
        for link in links:
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
                        return page
                    return None
                # now call lower level
                next_path = os.path.join(path, link.name)
                next_node = next(node.children())
                saved_page = self._iterate_tree_deep(next_node,
                                                     next_path,
                                                     parsed_links)
                for next_node in node.children():
                    self._iterate_tree_deep(next_node,
                                            next_path,
                                            parsed_links,
                                            saved_page)
                return parser.page
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
                    return None
            else:
                raise Exception(
                    'This must be unreachable. Dramatic flaw in code')
        return None

    @staticmethod
    def mkpath_for(file_path: str) -> None:
        dir = os.path.dirname(file_path)
        os.makedirs(dir, exist_ok=True)

""" plain linear single thread impl """

from getcourse_dl.pipelines.abstract_pypline import AbstractPipeline, PipelineTree
from getcourse_dl.parsers.abstract_parser import AbstractParser, Link, ParserException
from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader, DownloaderException
from getcourse_dl.logger.logger import Verbosity, logger
from os.path import dirname
from os import mkdir


class LinearPipeline(AbstractPipeline):
    def run(self):
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
                    logger.print(Verbosity.WARNING, 'link {} failed to be parsed with {}.\n\tcause: {}'.format(link.url, parser, str(e)))
                    return None
                # now call lower level
                next_path = path + '/' + link.name
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
                output_path = path + '/' + link.name
                self.mkpath_for(output_path)
                downloader = executor_type(url=link.url,
                                           output_path=output_path)
                try:
                    downloader.download()
                except DownloaderException as e:
                    logger.print(Verbosity.WARNING, 'download from {} failed with {}.\n\tcause: {}'.format(link.url, downloader, str(e)))
                    return None
            else:
                raise Exception('This must be unreachable. Dramatic flaw in code')

    @staticmethod
    def mkpath_for(file_path: str):
        dir = dirname(file_path)
        mkdir(dir, 0o755)


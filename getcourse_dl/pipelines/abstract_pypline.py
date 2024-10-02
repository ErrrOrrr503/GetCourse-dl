""" Pipeline - run parsers and downloaders """
from abc import ABC, abstractmethod
from typing import Any, Generator, Iterable, Type
from getcourse_dl.parsers.abstract_parser import AbstractParser, Link
from getcourse_dl.downloaders.abstract_downloader import AbstractDownloader


class PipelineTree:
    item: Type[AbstractParser] | Type[AbstractDownloader]

    def __init__(self, item: Type[AbstractParser] | Type[AbstractDownloader],
                 _parent: Any = None) -> None:
        self._children: list[PipelineTree] = []
        if _parent is not (PipelineTree | None):
            raise Exception('Fatal. Wrong tree usage.')
        self._parent: PipelineTree | None = _parent
        self.item = item

    def append_child(self, item: Type[AbstractParser] | Type[AbstractDownloader]) -> None:
        self._children.append(PipelineTree(item, self))

    def children(self) -> Generator[Any]:
        return (child for child in self._children)


class AbstractPipeline(ABC):
    tree: PipelineTree
    startpoint: Link

    def __init__(self, tree: PipelineTree, startpoint: Link) -> None:
        self.tree = tree
        self.startpoint = startpoint

    @abstractmethod
    def run(self) -> None:
        """ implement how to run pipeline """

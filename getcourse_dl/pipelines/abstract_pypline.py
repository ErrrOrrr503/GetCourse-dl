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
        if not (isinstance(_parent, PipelineTree) or _parent is None):
            raise Exception(
                'Fatal. Wrong tree usage. _parent is {}'.format(_parent))
        self._parent: PipelineTree | None = _parent
        self.item = item

    def append_child(self, item: Type[AbstractParser] | Type[AbstractDownloader]) -> Any:
        self._children.append(PipelineTree(item, self))
        return self._children[-1]

    def children(self) -> Generator[Any, None, None]:
        return (child for child in self._children)

    def __repr__(self) -> str:
        res = ''
        prefix = ''
        return self._repr_tree(res, prefix)  # list to make res mutable

    def _repr_tree(self, res: str, prefix: str) -> str:
        res += prefix + self.item.__name__ + '\n'
        prefix = ' ' * len(prefix) + '˪'
        for child in self._children:
            res = child._repr_tree(res, prefix)
        return res


class AbstractPipeline(ABC):
    tree: PipelineTree
    startpoint: Link

    def __init__(self, tree: PipelineTree, startpoint: Link) -> None:
        self.tree = tree
        self.startpoint = startpoint

    @abstractmethod
    def run(self) -> None:
        """ implement how to run pipeline """

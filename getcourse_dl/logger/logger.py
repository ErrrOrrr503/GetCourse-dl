"""
Simple project-wide logger
"""
from enum import Enum
from typing import Any
from termcolor import colored


class Verbosity(Enum):
    QUIET = 0
    ERROR = 1
    WARNING = 2  # default
    INFO = 3
    DEBUG = 4
    EVERYTHING = 5


class Logger():
    """ project-wide logger and, in fact, printer """
    verbosity: Verbosity

    def _print(self, logger_extra_print: bool, verbosity: Verbosity,
               *print_args: Any,
               **print_kwargs: Any) -> None:
        if (verbosity.value > self.verbosity.value):
            return
        if (logger_extra_print):
            if (verbosity == Verbosity.ERROR):
                print(colored('[ERROR]:     ', 'red'), end='')
            elif (verbosity == Verbosity.WARNING):
                print(colored('[WARNING]:   ', 'yellow'), end='')
            elif (verbosity == Verbosity.INFO):
                print('[INFO]:      ', end='')
            elif (verbosity == Verbosity.DEBUG):
                print('[DEBUG]:     ', end='')
            elif (verbosity == Verbosity.EVERYTHING):
                print('[EVERYTHING]:', end='')
        print(*print_args, **print_kwargs)

    def print(self, verbosity: Verbosity, *print_args: Any, **print_kwargs: Any) -> None:
        self._print(True, verbosity, *print_args, **print_kwargs)

    def print_as_is(self, verbosity: Verbosity, *print_args: Any, **print_kwargs: Any) -> None:
        self._print(False, verbosity, *print_args, **print_kwargs)


logger = Logger()

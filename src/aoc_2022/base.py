import abc
from contextlib import contextmanager
from typing import IO

from aoc_2022 import util


class Solution(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def day(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def part(self) -> int:
        pass

    @property
    def input_file_name(self) -> str:
        return f'day_{self.day:02d}_01_input.txt'

    @contextmanager
    def get_input_file(self) -> IO:
        with open(util.get_resource_path(self.input_file_name), 'r') as f:
            yield f

    @abc.abstractmethod
    def run(self):
        pass

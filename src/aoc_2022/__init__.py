import abc


class Solution(metaclass=abc.ABCMeta):

    @property
    @abc.abstractmethod
    def day(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def part(self) -> int:
        pass

    @abc.abstractmethod
    def run(self):
        pass

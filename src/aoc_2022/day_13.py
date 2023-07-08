import dataclasses
from functools import reduce, cmp_to_key
from typing import List, Any

from setuptools.namespaces import flatten

from aoc_2022 import Solution


@dataclasses.dataclass
class PacketPair:
    left: Any
    right: Any


class Solution13Common:

    @staticmethod
    def parse_input(input_file) -> List[PacketPair]:
        with input_file as f:
            lines = f.readlines()

        packets = list()
        current_left_line = None

        for current_line in lines:
            if current_line.startswith('\n'):
                continue
            parsed_line = eval(current_line)
            if current_left_line is None:
                current_left_line = parsed_line
            else:
                packets.append(PacketPair(left=current_left_line, right=parsed_line))
                current_left_line = None

        return packets

    @staticmethod
    def is_correctly_ordered(packet: PacketPair):
        """
        Tests if a packet pair is correctly sorted. Returns True if it is correctly sorted; false otherwise
        :param packet:
        :return:
        """

        return Solution13Common.compare_packets(packet.left, packet.right)

    @staticmethod
    def compare_packets(l, r):
        def compare_values(l, r):
            if l < r:
                return 1
            elif l > r:
                return -1
            else:
                return 0

        if isinstance(l, int) and isinstance(r, int):
            return compare_values(l, r)

        l = l if isinstance(l, list) else [l, ]
        r = r if isinstance(r, list) else [r, ]

        for l_i, r_i in zip(l, r):
            res = Solution13Common.compare_packets(l_i, r_i)
            if res != 0:
                return res
        return compare_values(len(l), len(r))


class Solution1301(Solution):
    day = 13
    part = 1

    def run(self):
        input = Solution13Common.parse_input(self.get_input_file())
        sum_of_indicies_that_are_in_the_correct_order = 0
        for i, packet in enumerate(input, start=1):
            if Solution13Common.is_correctly_ordered(packet) == 1:
                sum_of_indicies_that_are_in_the_correct_order = sum_of_indicies_that_are_in_the_correct_order + i

        return sum_of_indicies_that_are_in_the_correct_order


class Solution1302(Solution):
    day = 13
    part = 2

    def run(self):
        input = Solution13Common.parse_input(self.get_input_file())
        # Add the divider packet
        input.append(PacketPair(left=[[2]], right=[[6]]))
        packets = flatten(map(lambda x: [x.left, x.right], input))
        sorted_packets = sorted(packets, key=cmp_to_key(Solution13Common.compare_packets), reverse=True)

        indexes = []
        for i, p in enumerate(sorted_packets, start=1):
            if p in ([[2]], [[6]]):
                indexes.append(i)

        return reduce(lambda x, y: x * y, indexes, 1)

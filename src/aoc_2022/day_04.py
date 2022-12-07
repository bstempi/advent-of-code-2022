from aoc_2022 import util, Solution


class Solution0401(Solution):
    day = 4
    part = 1

    def run(self) -> int:
        current_total = 0
        with open(util.get_resource('day_04_01_input.txt')) as f:
            while True:
                line = f.readline().strip()
                if not line or line == '':
                    break
                ranges = line.split(',')
                first_range = ranges[0].split('-')
                second_range = ranges[1].split('-')
                overlaps = self.do_ranges_completely_overlap(int(first_range[0]), int(first_range[1]),
                                                               int(second_range[0]), int(second_range[1]))
                if overlaps:
                    current_total += 1

        return current_total

    @staticmethod
    def do_ranges_completely_overlap(x_start, x_end, y_start, y_end):
        if x_start <= y_start and x_end >= y_end:
            return True
        if y_start <= x_start and y_end >= x_end:
            return True

        return False


class Solution0402(Solution):
    day = 4
    part = 2

    def run(self) -> int:
        current_total = 0
        with open(util.get_resource('day_04_01_input.txt')) as f:
            while True:
                line = f.readline().strip()
                if not line or line == '':
                    break
                ranges = line.split(',')
                first_range = ranges[0].split('-')
                second_range = ranges[1].split('-')
                overlaps = self.do_ranges_overlap(int(first_range[0]), int(first_range[1]),
                                                  int(second_range[0]), int(second_range[1]))
                if overlaps:
                    current_total += 1

        return current_total

    @staticmethod
    def do_ranges_overlap(x_start, x_end, y_start, y_end):
        """
        This is basically the opposite of, "does it not overlap?"
        :param x_start:
        :param x_end:
        :param y_start:
        :param y_end:
        :return:
        """
        if x_end < y_start:
            return False
        if y_end < x_start:
            return False
        return True

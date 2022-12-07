import string

from aoc_2022 import Solution, util


item_priorities = {item: priority+1
                   for priority, item in enumerate(string.ascii_lowercase + string.ascii_uppercase)}


class Solution0301(Solution):
    day = 3
    part = 1

    def run(self) -> int:
        current_total = 0
        with open(util.get_resource('day_03_01_input.txt')) as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break

                sack_size = len(line) // 2
                sack_0 = set(line[:sack_size])
                sack_1 = set(line[sack_size:])
                overlap = sack_0.intersection(sack_1)
                if len(overlap) != 1:
                    raise RuntimeError(f'Found an overlap of more than one item; sacks: {line}')
                score_for_overlap = item_priorities[next(iter(overlap))]
                current_total += score_for_overlap

        return current_total


class Solution0302(Solution):
    day = 3
    part = 2

    def run(self) -> int:
        current_highest_totals = []
        total = 0
        current_sets = []
        with open(util.get_resource('day_03_01_input.txt')) as f:
            while True:
                line = f.readline().strip()
                if not line:
                    break
                current_sets.append(set(line))

                if len(current_sets) == 3:
                    intersection = current_sets[0] & current_sets[1] & current_sets[2]
                    if len(intersection) != 1:
                        raise RuntimeError(f'Intersection should only be 1; intersection was {len(intersection)}; '
                                           f'sets: {current_sets}')
                    total += item_priorities[next(iter(intersection))]
                    current_sets = []

        return total

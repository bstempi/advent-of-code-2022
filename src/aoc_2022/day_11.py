import dataclasses
import functools
from abc import ABC
from typing import List, Callable, Dict

from aoc_2022 import Solution


@dataclasses.dataclass
class Monkey:
    id: int
    items: List[int]
    operation_line: str
    test_line: str
    left_monkey_id: int
    right_monkey_id: int


class Solution11Common:

    @staticmethod
    def parse_monkey_data(input_file) -> Dict[int, Monkey]:
        monkey_dict = dict()
        with input_file as f:
            lines = f.readlines()

        # 7 lines per monkey
        for i in range((len(lines) + 1) // 7):
            offset = i * 7
            monkey_id_line = lines[offset].strip()
            starting_items_line = lines[offset + 1].strip()
            operation_line = lines[offset + 2].strip()
            test_line = lines[offset + 3].strip()
            test_true_line = lines[offset + 4].strip()
            test_false_line = lines[offset + 5].strip()

            # Skip the blank line in between

            monkey = Monkey(
                id=int(monkey_id_line.replace('Monkey ', '').replace(':', '')),
                items=[int(x.strip()) for x in starting_items_line.replace('Starting items: ', '').split(',')],
                operation_line=operation_line.replace('Operation: ', ''),
                test_line=test_line.replace('Test: ', ''),
                left_monkey_id=int(test_true_line.replace('If true: throw to monkey ', '')),
                right_monkey_id=int(test_false_line.replace('If false: throw to monkey ', ''))
            )
            monkey_dict[monkey.id] = monkey
        return monkey_dict

    @staticmethod
    def apply_operation(monkey_dict: Dict[int, Monkey], monkey_id: int, apply_relief: bool) -> int:
        """
        Pops the head off of the items list for the given monkey and applies the operation to it. This returns the
        result of the operation so that the user can decide what to do with this item.
        :param monkey_dict:
        :param monkey_id:
        :param apply_relief:
        :return:
        """
        monkey = monkey_dict[monkey_id]
        exec_globals = {}
        exec_locals = {'old': monkey.items.pop(0)}
        # Operation shows how your worry level changes as that monkey inspects an item. (An operation like
        # new = old * 5 means that your worry level after the monkey inspected the item is five times whatever your
        # worry level was before inspection.)
        exec(monkey.operation_line, exec_globals, exec_locals)
        # After each monkey inspects an item but before it tests your worry level, your relief that the
        # monkey's inspection didn't damage the item causes your worry level to be divided by three and
        # rounded down to the nearest integer.
        if apply_relief:
            exec_locals['new'] = exec_locals['new'] // 3

        return exec_locals['new']

    @staticmethod
    def apply_test(monkey_dict: Dict[int, Monkey], monkey_id, worry_level) -> bool:
        """
        Given the worry level and some monkey id, this function will apply the test and return a true if the test passed,
        false otehrwise.
        :param monkey_dict:
        :param monkey_id:
        :param worry_level:
        :return:
        """
        # It just so happens that all of the tests are "divisible by," so we just need to parse the number at the end
        monkey = monkey_dict[monkey_id]
        line = monkey.test_line
        unparsed_number = line.split(' ')[2]
        denominator = int(unparsed_number)
        return worry_level % denominator == 0


class Solution1101(Solution):
    day = 11
    part = 1

    def run(self):
        monkey_dict = Solution11Common.parse_monkey_data(self.get_input_file())
        rounds = 20
        inspection_counts = {k: 0 for k in monkey_dict.keys()}

        # For each round
        for r in range(rounds):
            # For each monkey in each round
            # We're counting on the fact that the dict remembers order
            for m_id, monkey in monkey_dict.items():
                # For each item that the monkey has this round
                if len(monkey.items) == 0:
                    continue
                for _ in range(len(monkey.items)):
                    # The monkey is considering an item, so increment it's counter
                    inspection_counts[m_id] += 1
                    # Figure out the new worry level
                    new_worry_level = Solution11Common.apply_operation(monkey_dict, m_id, True)
                    # Apply the test
                    test_result = Solution11Common.apply_test(monkey_dict, m_id, new_worry_level)
                    if test_result:
                        dest_m_id = monkey.left_monkey_id
                    else:
                        dest_m_id = monkey.right_monkey_id
                    monkey_dict[dest_m_id].items.append(new_worry_level)

        inspection_counts = inspection_counts.values()
        return functools.reduce(lambda x, y: x * y, sorted(inspection_counts, reverse=True)[:2], 1)


class Solution1102(Solution):
    day = 11
    part = 2

    def run(self):
        monkey_dict = Solution11Common.parse_monkey_data(self.get_input_file())
        rounds = 10000
        inspection_counts = {k: 0 for k in monkey_dict.keys()}

        # These number will keep growing forever (to thousands of digits) if I don't find a way to reduce them. The idea
        # that I have is to figure out what the product of all of the "tests" are and use that as the maximum number I
        # should consider before reduction. If I have 3 monkeys and the test numbers are 2, 3, and 5, the threshold for
        # reduction is 30. I'm really only interested in values 0-29 because the tests only care about multiples of
        # their respective tests. Once I'm over 30, if I modulo the number by 30, I get a remainder that still fulfills
        # the properties that the test cares about: divisibility. E.g., 2, 3, and 5 modulo into 1 with the same
        # remainder as they modulo into 31; they divide into 15 with the same modulo as 45, 75, etc. We need to figure
        # out what this product is. The exception is when the remainder is 0; 30%5 yeilds a number, but 0%5 does not.
        # This line is dense; the input iterator (the second arg) is the parsed number from each of the test lines.
        # The first argument multiples all numbers together
        # The last arg start with a seed value of 1.
        magic_product = functools.reduce(lambda x, y: x * y,
                                         [int(x.test_line.split(' ')[2]) for x in monkey_dict.values()],
                                         1)

        # For each round
        for r in range(rounds):
            # For each monkey in each round
            # We're counting on the fact that the dict remembers order
            for m_id, monkey in monkey_dict.items():
                # For each item that the monkey has this round
                if len(monkey.items) == 0:
                    continue
                for _ in range(len(monkey.items)):
                    # The monkey is considering an item, so increment it's counter
                    inspection_counts[m_id] += 1
                    # Figure out the new worry level
                    new_worry_level = Solution11Common.apply_operation(monkey_dict, m_id, False)
                    # Apply the test
                    test_result = Solution11Common.apply_test(monkey_dict, m_id, new_worry_level)
                    if test_result:
                        dest_m_id = monkey.left_monkey_id
                    else:
                        dest_m_id = monkey.right_monkey_id

                    # Before assignment, we need to reduce
                    if new_worry_level % magic_product > 0:
                        new_worry_level = new_worry_level % magic_product
                    monkey_dict[dest_m_id].items.append(new_worry_level)

        inspection_counts = inspection_counts.values()
        return functools.reduce(lambda x, y: x * y, sorted(inspection_counts, reverse=True)[:2], 1)

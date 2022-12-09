import dataclasses
from typing import List, Dict

from aoc_2022 import Solution, util


def read_initial_state(f) -> Dict[int, List[str]]:
    col_start = 1
    col_step = 4
    col_mappings = {}

    read_next_line = True
    while read_next_line:
        line = f.readline()
        current_col = 0
        continue_reading_row = True
        while continue_reading_row:
            current_col_index = col_start + current_col * col_step

            if current_col_index > len(line):
                # We hit the end of the line (literally)
                continue_reading_row = False
                break

            col_value = line[current_col_index]
            if str.isalpha(col_value):
                # We found a value; read it and move onto the next col
                if current_col not in col_mappings.keys():
                    col_mappings[current_col] = []
                col_mappings[current_col].insert(0, col_value)
                current_col += 1
            elif col_value == ' ':
                # Nothing found; increment the counter and continue
                current_col += 1
            elif str.isnumeric(col_value):
                # We hit the absolute end of our setup
                read_next_line = False
                continue_reading_row = False
                break

    return col_mappings


@dataclasses.dataclass
class MoveCommand:
    origination_stack: int
    destination_stack: int
    containers_to_move: int

    @staticmethod
    def parse_line(line):
        parts = line.split(' ')
        containers_to_move = int(parts[1])
        origination_stack = int(parts[3])
        destination_stack = int(parts[5])

        return MoveCommand(origination_stack=origination_stack,
                           destination_stack=destination_stack,
                           containers_to_move=containers_to_move)


class Solution0501(Solution):

    day = 5
    part = 1

    def run(self) -> int:
        with self.get_input_file() as f:
            ship_stacks = read_initial_state(f)

            # Burn the blank line
            f.readline()

            # Execute the move commands
            while True:
                line = f.readline().strip()
                if not line or line == '':
                    break
                command = MoveCommand.parse_line(line)
                for _ in range(command.containers_to_move):
                    item_in_transit = ship_stacks[command.origination_stack-1].pop()
                    ship_stacks[command.destination_stack-1].append(item_in_transit)

        stack_count = len(ship_stacks.keys())
        return ''.join([ship_stacks[x].pop() for x in range(stack_count)])


class Solution0502(Solution):
    day = 5
    part = 2

    def run(self) -> int:
        with self.get_input_file() as f:
            ship_stacks = read_initial_state(f)

            # Burn the blank line
            f.readline()

            # Execute the move commands
            while True:
                line = f.readline().strip()
                if not line or line == '':
                    break
                command = MoveCommand.parse_line(line)

                items_in_transit = []
                for _ in range(command.containers_to_move):
                    items_in_transit.append(ship_stacks[command.origination_stack - 1].pop())
                for _ in range(command.containers_to_move):
                    ship_stacks[command.destination_stack - 1].append(items_in_transit.pop())

        stack_count = len(ship_stacks.keys())
        return ''.join([ship_stacks[x].pop() for x in range(stack_count)])

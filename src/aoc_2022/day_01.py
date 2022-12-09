from aoc_2022 import Solution, util


class Solution0101(Solution):

    day = 1
    part = 1

    def run(self) -> int:
        current_highest_total = 0
        current_elf_total = 0
        with self.get_input_file() as f:
            while True:
                line = f.readline()
                if not line:
                    break

                if line != '\n':
                    current_elf_total += int(line)
                else:
                    # End of line; is this new total higher?
                    if current_elf_total > current_highest_total:
                        current_highest_total = current_elf_total
                    # No matter what, reset the current counter
                    current_elf_total = 0

        return current_highest_total


class Solution0102(Solution):
    day = 1
    part = 2

    def run(self) -> int:
        current_highest_totals = []
        current_elf_total = 0
        with self.get_input_file() as f:
            while True:
                line = f.readline()
                if not line:
                    break

                if line != '\n':
                    current_elf_total += int(line)
                else:
                    # End of line; is this new total higher?
                    current_highest_totals.append(current_elf_total)
                    if len(current_highest_totals) > 3:
                        # Get rid of the min value
                        min_val = min(current_highest_totals)
                        current_highest_totals.remove(min_val)

                    # No matter what, reset the current counter
                    current_elf_total = 0

        return sum(current_highest_totals)

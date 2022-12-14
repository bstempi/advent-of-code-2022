from aoc_2022 import Solution


class Solution1001(Solution):

    day = 10
    part = 1

    def run(self):
        with self.get_input_file() as f:
            signal_strength_sum = 0
            special_cycles = [20, 60, 100, 140, 180, 220]
            x = 1
            cycle_counter = 0
            while True:
                line = f.readline().strip()

                if not line or line == '':
                    break

                # Do a check
                if cycle_counter+1 in special_cycles:
                    signal_strength = x * (cycle_counter+1)
                    signal_strength_sum += signal_strength

                # No matter what instruction we read, it increases our cycle counter by at least one
                cycle_counter += 1

                # If this was an addition operation, increment the counter, check "during the operation," then do the
                # add
                if line.startswith('addx'):

                    if cycle_counter+1 in special_cycles:
                        signal_strength = x * (cycle_counter+1)
                        signal_strength_sum += signal_strength

                    _, val = line.split(' ')
                    x += int(val)

                    cycle_counter += 1

            return signal_strength_sum


class Solution1002(Solution):

    day = 10
    part = 2

    def run(self):
        with self.get_input_file() as f:
            line_width = 40
            lines = []

            x = 1
            cycle_counter = 0
            current_line = ''
            while True:
                line = f.readline().strip()

                if not line or line == '':
                    break

                # Draw a pixel
                if x-1 <= cycle_counter % 40 <= x+1:
                    current_line += '#'
                else:
                    current_line += ' '

                # No matter what instruction we read, it increases our cycle counter by at least one
                cycle_counter += 1
                if len(current_line) == line_width:
                    lines.append(current_line)
                    current_line = ''

                # If this was an addition operation, increment the counter, check "during the operation," then do the
                # add
                if line.startswith('addx'):

                    # Draw a pixel
                    if x - 1 <= cycle_counter % 40 <= x + 1:
                        current_line += '#'
                    else:
                        current_line += ' '

                    _, val = line.split(' ')
                    x += int(val)

                    cycle_counter += 1
                    if len(current_line) == line_width:
                        lines.append(current_line)
                        current_line = ''

            return '\n' + '\n'.join(lines)

import functools
from typing import Dict, Tuple

from aoc_2022 import Solution


class Solution0701(Solution):

    day = 7
    part = 1

    @staticmethod
    def parse_commands_calculate_total_of_immediate_children(io) -> Dict[Tuple[str], int]:
        """
        Given some list of commands that traverse a file system, this function figures out the total size of the file
        objects within each directory. It does not count the size of subdirectories.
        :param io:
        :return:
        """
        mode = None
        current_path = []
        current_total = 0

        # This represents how much space the files that are in this directory (but not their children) consume
        path_direct_totals = {}
        while True:
            line = io.readline().strip()
            if not line or line == '':
                # We're done, but we may have been actively adding sizes. Check to make sure we're not in ls mode
                if mode == 'ls':
                    path_direct_totals[tuple(current_path)] = current_total
                break

            parts = line.split(' ')
            if line[0] == '$':
                # We have a command
                command = parts[1]

                if command == 'cd':
                    # Before we cd, we need to record the current total for the files that are direct children of
                    # this dir
                    if mode == 'ls':
                        path_direct_totals[tuple(current_path)] = current_total

                    mode = 'cd'
                    if parts[2] == '..':
                        # You can't cd above root...
                        if len(current_path) > 1:
                            current_path.pop()
                    else:
                        if parts[2] == '/':
                            current_path = ['', ]
                        else:
                            current_path.append(parts[2])
                if command == 'ls':
                    current_total = 0
                    mode = 'ls'
            elif mode == 'ls':
                if parts[0] == 'dir':
                    continue
                else:
                    current_total += int(parts[0])
        return path_direct_totals

    @staticmethod
    def calculate_cumulative_directory_sizes(dir_dict) -> Dict[Tuple[str], int]:
        """
        Given a dict of directory sizes (dir tuple, immediate file size), this function will calculate cumulative
        directory sizes.
        :param dir_dict:
        :return:
        """
        path_cumulative_totals = {}
        for outer_path, size in dir_dict.items():
            for i in range(len(outer_path)):
                inner_path = tuple(outer_path[0:i + 1])
                path_cumulative_totals[inner_path] = path_cumulative_totals.get(inner_path, 0) + size
        return path_cumulative_totals

    def run(self) -> int:
        with self.get_input_file() as f:
            path_direct_totals = self.parse_commands_calculate_total_of_immediate_children(f)
            path_cumulative_totals = self.calculate_cumulative_directory_sizes(path_direct_totals)

            upper_bound = 100000
            total_below_threshold = 0
            for size in path_cumulative_totals.values():
                if size <= upper_bound:
                    total_below_threshold += size

            return total_below_threshold


class Solution0702(Solution):

    day = 7
    part = 2

    total_disk_space = 70000000
    required_disk_space = 30000000

    def run(self):
        with self.get_input_file() as f:
            path_direct_totals = Solution0701.parse_commands_calculate_total_of_immediate_children(f)
            path_cumulative_totals = Solution0701.calculate_cumulative_directory_sizes(path_direct_totals)

            # Calculate our thresholds
            total_disk_usage = functools.reduce(lambda x, y: x + y, path_direct_totals.values(), 0)
            free_disk_space = self.total_disk_space - total_disk_usage
            additional_space_needed = self.required_disk_space - free_disk_space

            smallest_dir_over_required = total_disk_usage
            for v in path_cumulative_totals.values():
                if additional_space_needed <= v <= smallest_dir_over_required:
                    smallest_dir_over_required = v

        return smallest_dir_over_required

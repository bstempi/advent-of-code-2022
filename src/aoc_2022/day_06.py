from aoc_2022 import Solution


class Solution0601(Solution):

    day = 6
    part = 1

    def run(self) -> int:
        with self.get_input_file() as f:
            # The one and only line
            line = f.readline()

        unique_seq_len = 4
        for i in range(unique_seq_len-1, len(line)):
            s = set()
            s.update(line[i-unique_seq_len+1:i+1])
            if len(s) == unique_seq_len:
                return i + 1


class Solution0602(Solution):

    day = 6
    part = 2

    def run(self) -> int:
        with self.get_input_file() as f:
            # The one and only line
            line = f.readline()

        unique_seq_len = 14
        for i in range(unique_seq_len - 1, len(line)):
            s = set()
            s.update(line[i - unique_seq_len + 1:i + 1])
            if len(s) == unique_seq_len:
                return i + 1

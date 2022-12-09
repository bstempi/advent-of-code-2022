from enum import Enum

from aoc_2022 import Solution, util


class RoundOutcome(Enum):
    WIN = 0
    LOSS = 1
    DRAW = 2


class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


# Does move A beat move B?
MOVE_COMBO_OUTCOMES = {
    # Draws
    (Move.ROCK, Move.ROCK): RoundOutcome.DRAW,
    (Move.PAPER, Move.PAPER): RoundOutcome.DRAW,
    (Move.SCISSORS, Move.SCISSORS): RoundOutcome.DRAW,

    # Wins
    (Move.SCISSORS, Move.ROCK): RoundOutcome.WIN,
    (Move.PAPER, Move.SCISSORS): RoundOutcome.WIN,
    (Move.ROCK, Move.PAPER): RoundOutcome.WIN,

    # Losses
    (Move.ROCK, Move.SCISSORS): RoundOutcome.LOSS,
    (Move.SCISSORS, Move.PAPER): RoundOutcome.LOSS,
    (Move.PAPER, Move.ROCK): RoundOutcome.LOSS,
}


PARSER_MAPPINGS = {
    'A': Move.ROCK,
    'B': Move.PAPER,
    'C': Move.SCISSORS,
    'X': Move.ROCK,
    'Y': Move.PAPER,
    'Z': Move.SCISSORS,
}


MOVE_SCORE_MAPPINGS = {
    Move.ROCK: 1,
    Move.PAPER: 2,
    Move.SCISSORS: 3,
}


ROUND_SCORE_MAPPINGS = {
    RoundOutcome.WIN: 6,
    RoundOutcome.DRAW: 3,
    RoundOutcome.LOSS: 0,
}


class Solution0201(Solution):
    day = 2
    part = 1

    def run(self) -> int:
        total_score = 0
        with self.get_input_file() as f:
            while True:
                line = f.readline()

                if not line:
                    break

                (opponent_move, my_move) = line.strip().split(' ')
                opponent_move = PARSER_MAPPINGS[opponent_move]
                my_move = PARSER_MAPPINGS[my_move]
                round_outcome = MOVE_COMBO_OUTCOMES[(opponent_move, my_move)]
                round_score = ROUND_SCORE_MAPPINGS[round_outcome]
                move_score = MOVE_SCORE_MAPPINGS[my_move]

                total_score += (round_score + move_score)

        return total_score


ROUND_ENDING_MAPPING = {
    'X': RoundOutcome.LOSS,
    'Y': RoundOutcome.DRAW,
    'Z': RoundOutcome.WIN,
}

OPPONENT_MOVE_DESIRED_OUTCOME_MAPPING = {(o_move, outcome): my_move
                                         for (o_move, my_move), outcome in MOVE_COMBO_OUTCOMES.items()}


class Solution0202(Solution):
    day = 2
    part = 2

    outcome_scores = [

    ]

    def run(self) -> int:
        total_score = 0
        with self.get_input_file() as f:
            while True:
                line = f.readline()

                if not line:
                    break

                (opponent_move, desired_outcome) = line.strip().split(' ')
                opponent_move = PARSER_MAPPINGS[opponent_move]
                desired_outcome = ROUND_ENDING_MAPPING[desired_outcome]
                round_score = ROUND_SCORE_MAPPINGS[desired_outcome]
                my_move = OPPONENT_MOVE_DESIRED_OUTCOME_MAPPING[(opponent_move, desired_outcome)]
                move_score = MOVE_SCORE_MAPPINGS[my_move]

                total_score += (round_score + move_score)

        return total_score

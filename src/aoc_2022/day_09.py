import dataclasses
import enum
import functools
from typing import Dict

from aoc_2022 import Solution


@dataclasses.dataclass(frozen=True, order=True, eq=True)
class Move:
    x: int
    y: int


@dataclasses.dataclass(frozen=True, order=True, eq=True)
class Point:
    x: int
    y: int

    def apply_move(self, move: Move):
        return Point(x=self.x + move.x, y=self.y + move.y)


class Moves(enum.Enum):
    D = Move(x=0, y=-1)
    U = Move(x=0, y=1)
    L = Move(x=-1, y=0)
    R = Move(x=1, y=0)


class Solution0901(Solution):

    day = 9
    part = 1

    def run(self):
        tail_locations = set()
        head_location = Point(0, 0)
        tail_location = Point(0, 0)

        with self.get_input_file() as f:
            while True:
                move = f.readline().strip()

                if not move or move == '':
                    break

                direction, distance = move.split(' ')
                move = Moves[direction].value
                distance = int(distance)

                for _ in range(distance):

                    # Apply the move and save the old location for the head in a buffer to figure out what should happen
                    # to the tail
                    old_head = head_location
                    head_location = head_location.apply_move(move)
                    walking_distance = abs(head_location.x - tail_location.x) + abs(head_location.y - tail_location.y)

                    # Add the x and y distance; if it's greater than 2, this is one of those weird diagonal situations,
                    # and the tail where go where the head used to be.
                    if walking_distance == 3:
                        tail_location = old_head
                    elif walking_distance == 2:
                        # They're diagonal from each other (one move on the x plane, one move on the y plane; nothing
                        # needs to happen
                        if head_location.x != tail_location.x and head_location.y != tail_location.y:
                            pass
                        # They're on the same row or column and there's a gap between them; apply the move to the rope
                        # to make it follow.
                        else:
                            tail_location = tail_location.apply_move(move)
                    # With a distance of 1, the tail is close enough already. With a distance of 0, they're on top of
                    # each other, which is the same case.
                    else:
                        pass

                    # We did some sort of move; log it in the list of tail locations
                    tail_locations.add(tail_location)

            return len(tail_locations)


class Solution0902(Solution):

    day = 9
    part = 2

    def run(self):
        tail_locations = set()
        num_knots = 10
        knots = [Point(0, 0) for _ in range(num_knots)]

        with self.get_input_file() as f:
            while True:
                move = f.readline().strip()

                if not move or move == '':
                    break

                direction, distance = move.split(' ')
                move = Moves[direction].value
                distance = int(distance)

                for _ in range(distance):

                    # Apply the move to the head and allow the inner-loop to worry about the rest of the rope
                    knots[0] = knots[0].apply_move(move)

                    # Treat the larger rope like a series of 2-knot ropes; h is head and t is tail for this current pair
                    # This loop moves the whole rope to follow whever the head went
                    for h in range(num_knots-1):
                        t = h + 1
                        x_distance = abs(knots[h].x - knots[t].x)
                        y_distance = abs(knots[h].y - knots[t].y)
                        walking_distance = x_distance + y_distance

                        x_direction = 0 if x_distance == 0 else (knots[h].x - knots[t].x) / x_distance
                        y_direction = 0 if y_distance == 0 else (knots[h].y - knots[t].y) / y_distance

                        # Add the x and y distance; if it's greater than 2, this is one of those weird diagonal situations,
                        # and the tail where go where the head used to be. This is a confusing swaperoo since we need to
                        # keep reusing "old head"
                        if walking_distance >= 3:
                            # In the case of a single rope, knots[t] = old_head works, because it just to happens it's
                            # always diagonal. In the case of a more complex rope setup, the "old head" isn't always
                            # the same as a diagonal. We need to calculate an actual diagonal here.
                            knots[t] = knots[t].apply_move(Move(x=x_direction, y=y_direction))
                        elif walking_distance == 2:
                            # They're diagonal from each other (one move on the x plane, one move on the y plane; nothing
                            # needs to happen
                            if knots[h].x != knots[t].x and knots[h].y != knots[t].y:
                                pass
                            # They're on the same row or column and there's a gap between them; apply the move to the rope
                            # to make it follow.
                            else:
                                # In a less complex rope setup, knots[t] = knots[t].apply_move(move) works here, but
                                # because complex ropes can snake around, we need to figure out the move direction here.
                                # It turns out it look a lot like the diagonal move
                                knots[t] = knots[t].apply_move(Move(x=x_direction, y=y_direction))
                        # With a distance of 1, the tail is close enough already. With a distance of 0, they're on top of
                        # each other, which is the same case.
                        else:
                            pass

                    # We did some sort of move; log it in the list of tail locations
                    tail_locations.add(knots[-1])

            return len(tail_locations)

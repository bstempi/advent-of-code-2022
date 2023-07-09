import dataclasses
import itertools
from enum import Enum, auto
from functools import reduce
from typing import Dict

from aoc_2022 import Solution


@dataclasses.dataclass(eq=True, order=True, frozen=True)
class Coordinate:
    x: int
    y:int

    def __add__(self, other: 'Coordinate'):
        return Coordinate(x=self.x + other.x, y=self.y + other.y)


class TileType(Enum):
    rock = auto()
    sand = auto()


class Map:

    SAND_ORIGIN_COORDINATE = Coordinate(x=500, y=0)
    DOWN = Coordinate(x=0, y=1)
    DOWN_AND_TO_LEFT = Coordinate(x=-1, y=1)
    DOWN_AND_TO_RIGHT = Coordinate(x=1, y=1)
    SAND_MOVE_ATTEMPT_ORDER = [DOWN, DOWN_AND_TO_LEFT, DOWN_AND_TO_RIGHT]
    def __init__(self):
        self.tile_dict: Dict[Coordinate, TileType] = {}

    def add_rock_line(self, line)-> None:
        """
        Given some line from the input file, this function will update the internal dictionary to represent rock walls
        :param line:
        :return:
        """
        unparsed_coordinates = line.replace(' ', '').split('->')
        parsed_coordinates = [Coordinate(x=int(p[0]), y=int(p[1])) for p in (u.split(',') for u in unparsed_coordinates)]
        for start_coordinate, end_coordinate in itertools.pairwise(parsed_coordinates):
            # For each coordinate pair...
            direction = Coordinate(x=end_coordinate.x-start_coordinate.x, y=end_coordinate.y-start_coordinate.y)
            direction = Coordinate(x=int(direction.x/abs(direction.x)) if direction.x != 0 else 0,
                                   y=int(direction.y/abs(direction.y)) if direction.y != 0 else 0)
            current_coordinate = start_coordinate
            while current_coordinate != end_coordinate:
                # Fill in that line
                self.tile_dict[current_coordinate] = TileType.rock
                current_coordinate = current_coordinate + direction
            self.tile_dict[end_coordinate] = TileType.rock

    def calculate_lowest_rock_position(self) -> int:
        """
        Given the current state of the map, this function will calculate the highest y value for all rocks, inclusive.
        Returns 0 if there are no rocks.
        :return:
        """
        def rock_tile_filter(item):
            coordinate, tile_type = item
            return tile_type == TileType.rock
        rock_tiles = filter(rock_tile_filter, self.tile_dict.items())
        rock_tile_y_coordinates = map(lambda c: c[0].y, rock_tiles)
        return reduce(lambda y0, y1: max(y0, y1), rock_tile_y_coordinates, 0)

    def add_sand(self, sand_origin: Coordinate, max_depth: int)-> bool:
        """
        Adds a unit of sand to the map. Returns true if it was able to add something; false if the map was too full
        :param sand_origin:
        :param max_depth:
        :return:
        """
        # Check to make sure we have room for more sand
        if self.is_occupied(self.SAND_ORIGIN_COORDINATE):
            return False
        current_tile = sand_origin
        done = False
        while True:
            # Check to make sure we're not too deep
            if current_tile.y > max_depth:
                return False

            # We have room; try to move the sand
            done = True
            for current_direction_attempt in self.SAND_MOVE_ATTEMPT_ORDER:
                attempted_position = current_tile + current_direction_attempt
                if not self.is_occupied(attempted_position):
                    current_tile = attempted_position
                    done = False
                    break

            if done:
                break

        # If we got here, then the sand is in its final resting place
        self.tile_dict[current_tile] = TileType.sand
        return True


    def is_occupied(self, coordinate: Coordinate):
        """
        Tests if a tile is already occupied by something other than air
        :param coordinate:
        :return:
        """
        return coordinate in self.tile_dict


class Solution1401(Solution):
    day = 14
    part = 1

    def run(self):
        with self.get_input_file() as input_file:
            input = input_file.readlines()

        map = Map()
        for l in input:
            map.add_rock_line(l)

        i = -1
        max_depth = map.calculate_lowest_rock_position()
        keep_going = True
        while keep_going:
            keep_going = map.add_sand(map.SAND_ORIGIN_COORDINATE, max_depth)
            i += 1
        return i


class Solution1402(Solution):
    day = 14
    part = 2

    def run(self):
        with self.get_input_file() as input_file:
            input = input_file.readlines()

        map = Map()
        for l in input:
            map.add_rock_line(l)

        # Add a rock line at 2 space below the max y
        current_max_rock_depth = map.calculate_lowest_rock_position()
        rock_floor = current_max_rock_depth + 2
        map.add_rock_line(f'0,{rock_floor}->1000,{rock_floor}')

        i = -1
        max_depth = rock_floor + 1 # Set it to a depth we don't expect to get to
        keep_going = True
        while keep_going:
            keep_going = map.add_sand(map.SAND_ORIGIN_COORDINATE, max_depth)
            i += 1
        return i

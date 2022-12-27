import dataclasses
from typing import List, Tuple, Dict

from aoc_2022 import Solution


@dataclasses.dataclass(eq=True, frozen=True)
class Location:
    x: int
    y: int
    height: int


class Solution12Common:
    @staticmethod
    def parse_file(f) -> Tuple[List[Location], Location, Location]:
        """
        Parse the file into a collection of location information.
        :param f:
        :return:
        """
        locations = list()
        starting_location = None
        ending_location = None
        with f as file:
            lines = file.readlines()

        for y, current_line in enumerate(lines):
            current_line = current_line.strip()
            if current_line == '':
                break
            for x, current_loc_height in enumerate(current_line):
                is_starting_loc = False
                is_ending_loc = False

                if current_loc_height == 'S':
                    current_loc_height = 'a'
                    is_starting_loc = True

                if current_loc_height == 'E':
                    current_loc_height = 'z'
                    is_ending_loc = True

                loc = Location(x, y, current_loc_height)
                locations.append(loc)
                if is_starting_loc:
                    starting_location = loc
                if is_ending_loc:
                    ending_location = loc

        return locations, starting_location, ending_location

    @staticmethod
    def parse_dict_by_coordinate(locations: List[Location]) -> Dict[Tuple[int, int], Location]:
        locations_by_coordinates = {(l.x, l.y): l for l in locations}
        return locations_by_coordinates

    @staticmethod
    def calculate_neighbor_coordinates(x: int, y: int) -> List[Tuple[int, int]]:
        diff = (-1, 1)
        for x_diff in diff:
            yield x + x_diff, y
        for y_diff in diff:
            yield x, y + y_diff

    @staticmethod
    def shortest_path_from_to(starting_location: Location, ending_location: Location,
                              location_dict: Dict[Tuple[int, int], Location]) -> int:
        # Walk the graph; keep a stack to figure out which path to evaluate next, and keep a set to know which
        # places we've already visited
        visited_locations = set()
        # Current depth that we're visiting
        traversal_stack = list()
        # Queue for the next depth, so that we keep track of how deep we are
        next_traversal_stack = list()
        traversal_stack.append(starting_location)
        current_depth = 0
        target_reached = False

        while not target_reached:
            if len(traversal_stack) == 0:
                raise RuntimeError('Infinite loop; we have not found our target and have no more nodes to traverse.')
            while len(traversal_stack) > 0:
                # Which node are we dealing with?
                current_node = traversal_stack.pop(0)
                # If we've visited this node, continue on; no need to double-back
                if current_node in visited_locations:
                    continue
                # Keep track of the fact that we visited
                visited_locations.add(current_node)
                # Is this the node we're looking for? Flip the flag an exit the loop
                if current_node == ending_location:
                    target_reached = True
                    break
                # Not the node we're looking for? Queue up it's neighbors if they're eligible and if we've not visited
                # it before
                for neighboring_coordinate in Solution12Common.calculate_neighbor_coordinates(
                        current_node.x, current_node.y):
                    # If the neighbor exists
                    if neighboring_coordinate in location_dict:
                        neighbor: Location = location_dict[neighboring_coordinate]
                        # If we've not visited this neighbor and its an eligible height
                        if neighbor not in visited_locations \
                                and ord(neighbor.height) - ord(current_node.height) <= 1:
                            next_traversal_stack.append(neighbor)
                    # Else for any of these, we do nothing

            # We've finished traversing this depth; do bookkeeping and off to the next level!
            if not target_reached:
                traversal_stack = next_traversal_stack
                next_traversal_stack = list()
                current_depth += 1

        return current_depth


class Solution1201(Solution):

    day = 12
    part = 1

    def run(self) -> int:
        locations, starting_location, ending_location = Solution12Common.parse_file(self.get_input_file())
        loc_dict = Solution12Common.parse_dict_by_coordinate(locations)

        return Solution12Common.shortest_path_from_to(starting_location, ending_location, loc_dict)


class Solution1202(Solution):
    day = 12
    part = 2

    def run(self) -> int:
        # The most efficient thing to do is to start at the end and do a BFS traversal to the first 'a' that I find.
        # Such a solution would be exactly as efficient as problem 1. I, however, am lazy and know this will still run
        # in a reasonable amount of time, so I'm going to kick off a shortest path search for every 'a' and keep track
        # of the shortest one.
        locations, _, ending_location = Solution12Common.parse_file(self.get_input_file())
        loc_dict = Solution12Common.parse_dict_by_coordinate(locations)
        starting_locations = [l for l in locations if l.height == 'a']

        shortest_path = Solution1201().run()

        for starting_location in starting_locations:
            try:
                path_len = Solution12Common.shortest_path_from_to(starting_location, ending_location, loc_dict)
            except:
                pass
            if path_len < shortest_path:
                shortest_path = path_len
        return shortest_path

import dataclasses
import functools
from typing import Dict

from aoc_2022 import Solution


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class Point:
    """
    Represents a point on the plane of trees
    """
    x: int
    y: int

    def apply_move(self, move):
        return Point(self.x + move.x, self.y + move.y)


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class Move:
    """
    Represents a move
    """
    x: int
    y: int


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class Tree:
    """
    Represents a tree
    """
    height: int
    point: Point


class Solution0801(Solution):

    day = 8
    part = 1

    @staticmethod
    def parse_trees(f) -> (Dict[Point, Tree], int, int):
        """
        Given the input file, this function will parse all of the trees and place them into a dict keyed by the tree's
        location. It also gives the dimensions of the forest in width, height order.
        :param f:
        :return:
        """
        tree_dict = dict()

        line_index = 0
        line_width = -1
        while True:
            line = f.readline().strip()
            if not line or line == '':
                break
            if line_width == -1:
                line_width = len(line)

            for row_index, height in enumerate(line.strip()):
                point = Point(x=row_index, y=line_index)
                tree = Tree(height=int(height), point=point)
                tree_dict[point] = tree
            line_index += 1

        return tree_dict, line_width, line_index

    @staticmethod
    def tree_check(tree_dict, visible_trees, x, y, tallest_tree_so_far) -> int:
        """
        Evaluates if this tree is visible; mutates visible_trees and returns the height of the tallest tree so far,
        which is either the value passed in or the height of the new tallest tree.
        :param tree_dict:
        :param visible_trees:
        :param x:
        :param y:
        :param tallest_tree_so_far:
        :return:
        """
        tree = tree_dict[Point(x, y)]
        if tree.height > tallest_tree_so_far:
            visible_trees.add(tree)
            return tree.height
        return tallest_tree_so_far

    def run(self):
        with self.get_input_file() as f:
            tree_dict, forest_width, forest_height = Solution0801.parse_trees(f)

        # Mark all trees as invisible by default
        visible_trees = set()

        # row evaluations (left and right);
        # I wrote this before I developed the apply_move() function
        for row_i in range(forest_height):
            tallest_tree = -1
            for col_i in range(forest_width):
                tallest_tree = Solution0801.tree_check(tree_dict, visible_trees, col_i, row_i, tallest_tree)

            tallest_tree = -1
            for col_i in range(forest_width):
                tallest_tree = Solution0801.tree_check(tree_dict, visible_trees, forest_width - col_i - 1, row_i, tallest_tree)

        # col evaluation (up and down)
        for col_i in range(forest_width):
            tallest_tree = -1
            for row_i in range(forest_height):
                tallest_tree = Solution0801.tree_check(tree_dict, visible_trees, col_i, row_i, tallest_tree)

            tallest_tree = -1
            for row_i in range(forest_height):
                tallest_tree = Solution0801.tree_check(tree_dict, visible_trees, col_i, forest_width - row_i - 1, tallest_tree)

        return len(visible_trees)


class Solution0802(Solution):

    day = 8
    part = 2

    @staticmethod
    def evaluate_tree(tree: Tree, tree_dict: Dict[Point, Tree], x_min, x_max, y_min, y_max) -> int:
        move_left = Move(-1, 0)
        move_right = Move(1, 0)
        move_up = Move(0, -1)
        move_down = Move(0, 1)

        distances = []

        for current_dir in (move_left, move_right, move_up, move_down):
            current_loc = dataclasses.replace(tree.point)
            dir_total = 0
            while True:
                # Move
                current_loc = current_loc.apply_move(current_dir)

                # Are we at the edge?
                if current_loc.x > x_max or current_loc.x < x_min or current_loc.y > y_max or current_loc.y < y_min:
                    distances.append(dir_total)
                    break

                # Is this tree too tall?
                if tree_dict[current_loc].height >= tree.height:
                    distances.append(dir_total+1)
                    break

                # Apparently, we can keep going
                dir_total += 1

        return functools.reduce(lambda x, y: x * y, distances, 1)

    def run(self):
        with self.get_input_file() as f:
            tree_dict, forest_width, forest_height = Solution0801.parse_trees(f)

        x_min = min([p.x for p in tree_dict.keys()])
        x_max = max([p.x for p in tree_dict.keys()])
        y_min = min([p.y for p in tree_dict.keys()])
        y_max = max([p.y for p in tree_dict.keys()])

        current_max = 0
        max_tree = None
        for tree in tree_dict.values():
            tree_total = Solution0802.evaluate_tree(tree, tree_dict, x_min, x_max, y_min, y_max)
            if tree_total > current_max:
                current_max = tree_total
                max_tree = tree

        return current_max

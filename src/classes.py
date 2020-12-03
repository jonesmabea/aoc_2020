import time
from numbers import Number
from typing import Tuple, List

import numpy as np
import pprint

pprint = pprint.PrettyPrinter().pprint


class Forest:
    def __init__(self, file_path):
        """

        :param file_path:
        """
        self.forest_grid = self.parse_forest_file(file_path)
        self.forest_shape = self.forest_grid.shape

    @staticmethod
    def parse_forest_file(file_path):
        obj_map = {"#": 1, ".": 0}
        forest_grid = []
        with open(file_path, "r") as fh:
            for line in fh.readlines():
                print(line.strip())
                mapped_line = [obj_map[obj] for obj in line.strip()]
                forest_grid.append(mapped_line)
        forest_grid = np.array(forest_grid)
        print(f"Forest has shape: {forest_grid.shape}")
        return forest_grid

    def generate_extra_grid(self, forest_grid):
        """

        :param forest_grid:
        :return:
        """
        extended_map = np.concatenate((forest_grid, self.forest_grid), axis=1)
        return extended_map


class ForestNavigator:
    def __init__(self, forest:Forest, slope:Tuple[Number,Number]):
        """

        :param forest:
        :param slope:
        """
        self.forest = forest
        self.forest_grid = forest.forest_grid.copy()
        self.slope_paths = self.build_moves(slope)

    def get_periodic_idx(self, idx:Tuple[Number,Number]):
        """

        :param idx:
        :return:
        """
        if len(idx) == len(self.forest.forest_shape):
            mod_index = tuple(((i % s + s) % s for i, s in zip(idx, self.forest.forest_shape)))
            return mod_index

    def build_path(self, coord:np.ndarray, slope:np.ndarray, rem_rows:int, num_rows:int,result:List=None):
        """

        :param coord:
        :param slope:
        :param rem_rows:
        :param num_rows:
        :param result:
        :return:
        """
        if result is None:  # create a new result if no intermediate was given
            result = []
        nxt_coord: np.ndarray = np.add(coord, slope)
        if rem_rows > 1 and nxt_coord[0] < num_rows:
            result.append(tuple(nxt_coord))
            self.build_path(nxt_coord, slope, rem_rows - 1, num_rows, result)
        return result

    def build_moves(self, slope):
        """

        :param slope:
        :return:
        """
        slope = np.array(slope)
        start = np.array([0, 0])
        num_rows, num_cols = self.forest_grid.shape
        paths = self.build_path(coord=start, slope=slope, num_rows=num_rows, rem_rows=num_rows)

        return paths

    def generate_grid(self, path_xy, grid):
        """

        :param path_xy:
        :param grid:
        :return:
        """
        try:
            grid[path_xy]
        except IndexError:
            print("Extending grid")
            grid = self.forest.generate_extra_grid(grid)
        return grid

    def get_val_at_index(self, path_xy):
        """

        :param path_xy:
        :return:
        """
        return self.forest.forest_grid[self.get_periodic_idx(path_xy)]

    def print_map(self):
        """

        """
        grid: np.ndarray = self.forest_grid.copy()
        str_map = {1: "111", 0: "101"}
        print("Generating Forest grid")
        for path in self.slope_paths:
            grid = self.generate_grid(path, grid)
            res = grid[path]
            grid[path] = str_map[res]
        print(np.array2string(grid, max_line_width=1000))


class Tobogan:
    def __init__(self, forest_navigator: ForestNavigator):
        self.navigator = forest_navigator

    def calculate_trees_hit(self):
        """

        :return:
        """
        # row_idx, col_idx = list(zip(*self.navigator.slope_path)) # Commenting in case I need to use it in next assignments
        # path_hits = self.navigator.forest_grid[(row_idx),(col_idx)]

        path_hits = list(map(self.navigator.get_val_at_index, self.navigator.slope_paths))

        return np.sum(path_hits)


if __name__ == "__main__":
    forest = Forest("forest.txt")
    forest_navigator = ForestNavigator(forest, slope=(1, 3))
    paths = forest_navigator.slope_paths
    forest_navigator.print_map()
    tobogan = Tobogan(forest_navigator)
    print(tobogan.calculate_trees_hit())

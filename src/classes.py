import time
from dataclasses import dataclass
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
    def __init__(self, forest: Forest, slope: Tuple[Number, Number]):
        """

        :param forest:
        :param slope:
        """
        self.forest = forest
        self.forest_grid = forest.forest_grid.copy()
        self.slope_paths = self.build_moves(slope)

    def get_periodic_idx(self, idx: Tuple[Number, Number]):
        """

        :param idx:
        :return:
        """
        if len(idx) == len(self.forest.forest_shape):
            mod_index = tuple(
                ((i % s + s) % s for i, s in zip(idx, self.forest.forest_shape))
            )
            return mod_index

    def build_path(
        self,
        coord: np.ndarray,
        slope: np.ndarray,
        rem_rows: int,
        num_rows: int,
        result: List = None,
    ):
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
        paths = self.build_path(
            coord=start, slope=slope, num_rows=num_rows, rem_rows=num_rows
        )

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

        path_hits = list(
            map(self.navigator.get_val_at_index, self.navigator.slope_paths)
        )

        return np.sum(path_hits)


class BatchProcessor:
    @staticmethod
    def get_dict(passport_txt):
        d = dict()
        attributes = passport_txt.split(" ")
        for attribute in attributes:
            if attribute:
                key, val = attribute.split(":")
                d[key] = val
        return d

    def parse_batch_file(self, file_path):
        with open(file_path, "r") as fh:
            lines = fh.readlines()
            idxs = [i for i, v in enumerate(lines, 1) if v == "\n"] + [len(lines)]
            entry_list = [
                " ".join(lines[i:j]).replace("\n", "") for i, j in zip([0] + idxs, idxs)
            ]
            print(entry_list)
            return [self.get_dict(entry) for entry in entry_list]


class Passport:
    _BYR = "byr"
    _IYR = "iyr"
    _EYR = "eyr"
    _HGT = "hgt"
    _HCL = "hcl"
    _ECL = "ecl"
    _PID = "pid"
    _CID = "cid"

    _HASH = "#"
    _MANDATORY_KEYS = (_BYR, _IYR, _EYR, _HGT, _HCL, _ECL, _PID)
    _NON_MANDATORY = _CID

    _RULES = {
        _BYR: [str(n) for n in range(1920, 2002 + 1)],
        _IYR: [str(n) for n in range(2010, 2020 + 1)],
        _EYR: [str(n) for n in range(2020, 2030 + 1)],
        _HGT: {
            "in": [str(n) for n in range(59, 76 + 1)],
            "cm": [str(n) for n in range(150, 193 + 1)],
        },
        _HCL: {0: _HASH, "regex": "^[a-z0-9]{6}$"},
        _ECL: ("amb", "blu", "brn", "gry", "grn", "hzl", "oth"),
        _PID: 9,
    }

    def __init__(self, passport_dict):
        self.keys = []
        self.__init_values(passport_dict)

    def __init_values(self, passport_dict):
        for key, val in passport_dict.items():
            self.keys.append(key)
            setattr(self, key, val)
        return self

    def validate_passport(self):
        check = [k in self.keys for k in self._MANDATORY_KEYS]
        return all(check)

    @property
    def height_unit(self):
        if hasattr(self, self._HGT):
            return self.hgt[-2:]
        return None

    @property
    def height(self):
        if hasattr(self, self._HGT):
            return self.hgt[:-2]
        return None

    def validate_attributes(self):
        import re

        if not hasattr(self, self._BYR) or self.byr not in self._RULES[self._BYR]:
            return False

        if not hasattr(self, self._IYR) or self.iyr not in self._RULES[self._IYR]:
            return False

        if not hasattr(self, self._EYR) or self.eyr not in self._RULES[self._EYR]:
            return False

        if (
            not hasattr(self, self._HGT)
            or not self.height_unit
            or self.height
            not in self._RULES.get(self._HGT, {}).get(self.height_unit, [])
        ):
            return False

        if (
            not hasattr(self, self._HCL)
            or self.hcl[0] != self._RULES[self._HCL][0]
            or not re.match(self._RULES[self._HCL]["regex"], self.hcl.strip(self._HASH))
        ):
            return False

        if not hasattr(self, self._ECL) or self.ecl not in self._RULES[self._ECL]:
            return False

        if not hasattr(self, self._PID) or len(self.pid) != self._RULES[self._PID]:
            return False
        return True


@dataclass
class BoardingPass:
    _row_range = tuple(range(0, 2**7))
    _col_range = tuple(range(0, 2**3))
    boarding_id: str

    def __decode(self, id_str, s_range):
        row_map = {"F": 0, "B": 1, "R": 1, "L": 0}
        ind = len(s_range) // 2
        split = s_range[:ind], s_range[ind:]
        sel_range = split[row_map[id_str[0]]]
        if len(id_str) == 1:
            return sel_range[0]

        return self.__decode(id_str[1:], sel_range)

    @property
    def row(self) -> int:
        row_index = slice(0, 7)
        row_id = self.boarding_id[row_index]
        return self.__decode(row_id, self._row_range)

    @property
    def columm(self) -> int:
        col_index = slice(7, 11)
        col_id = self.boarding_id[col_index]
        return self.__decode(col_id, self._col_range)

    @property
    def seat_id(self):
        return (self.row * 8) + self.columm

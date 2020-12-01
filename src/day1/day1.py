import numpy as np
from src.util import find_elements_with_sum, arr_mult
import pprint

pp = pprint.PrettyPrinter()
if __name__ == "__main__":
    arr = np.fromfile("input.txt", dtype=np.int, sep="\n")

    valid_res = find_elements_with_sum(arr, 2020, 2)
    mult_res = arr_mult(valid_res)
    pp.pprint(f"Part 1: {mult_res}")

    valid_res = find_elements_with_sum(arr, 2020, 3)
    mult_res = arr_mult(valid_res)
    pp.pprint(f"Part 2: {mult_res}")
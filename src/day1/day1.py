import numpy as np
from src.util import find_elements_with_sum, arr_mult, read_file
import pprint

pp = pprint.PrettyPrinter()
if __name__ == "__main__":
    arr = read_file("input.txt", int)

    valid_res = find_elements_with_sum(arr, 2020, 2)
    mult_res = arr_mult(valid_res)
    pp.pprint(f"Part 1: {mult_res}")

    valid_res = find_elements_with_sum(arr, 2020, 3)
    mult_res = arr_mult(valid_res)
    pp.pprint(f"Part 2: {mult_res}")
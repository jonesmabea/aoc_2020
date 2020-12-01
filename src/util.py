from typing import Sequence

import numpy as np
from itertools import combinations


def arr_sum(n_list: Sequence) -> np.array:
    """
    Provided list it will calculate sum

    :param n_list: array
    :return: sum of elements
    :rtype: nd.array
    """
    return np.sum(n_list,axis=1)


def find_elements_with_sum(arr, expected_sum, n):
    """

    :rtype: np.array
    :param arr: list of numbers
    :param expected: expected sum
    :param n: mum of combinations
    :return: array of numbers that add to expected sum
    """
    comb_list = np.array(list(combinations(arr, n))).reshape(-1,n)
    res = arr_sum(comb_list)
    el_index = np.where(res == expected_sum)
    assert el_index, "No valid value found"
    return comb_list[el_index]


def arr_mult(n_list):
    return np.prod(n_list)
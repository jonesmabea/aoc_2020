from typing import Sequence

import numpy as np
from itertools import combinations

def read_file(input_path, cast=None):
    lines = []
    with open(input_path,"r") as fh:
        for line in fh.readlines():
            line = cast(line) if cast is not None else line
            lines.append(line)
    return lines
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
    """
    Returns product of array elements
    :rtype: int
    :param n_list:
    :return:
    """
    return np.prod(n_list)


def parse_password_and_policy(txt_string):
    """

    :param txt_string:
    :return:
    """
    pass_policy, password = txt_string.split(":")
    letter_num_constr, letter_constr = pass_policy.split(" ")
    range_ind = [int(ind) for ind in letter_num_constr.split("-")]
    return password.strip(), letter_constr, range_ind

def get_count(pass_str):
    """

    :param pass_str:
    :return:
    """
    d = dict()
    for letter in pass_str:
        if not d.get(letter):
            d[letter]=0
        d[letter]+=1
    return d

def get_letter_ind(pass_str):
    d = dict()
    for ind, letter in enumerate(pass_str):
        if not d.get(letter):
            d[letter]=[]
        d[letter].append(ind+1)
    return  d
def verify_old_pass_validity(password, letter_constr, min_max_len):
    pass_letter_cnt = get_count(password)
    letter_cnt = pass_letter_cnt.get(letter_constr, 0)
    if letter_cnt:
        min_val, max_val = min_max_len
        return min_val <= letter_cnt <= max_val
    return False
def assert_is_valid(letter_ind, range_ind, allowed_occurences):
    intersect = set(range_ind).intersection(set(letter_ind))
    return len(intersect) == allowed_occurences


def verify_new_pass_validity(password, letter_constr, range_ind, allowed_occurences=1):
    pass_letter_ind = get_letter_ind(password)
    letter_cnt = pass_letter_ind.get(letter_constr, [])
    if letter_cnt:
        return assert_is_valid(letter_cnt,range_ind,allowed_occurences)
    return False

from src.classes import BoardingPass
from src.util import read_file


def find_missing_in_cnt_range(li, min_id=0):
    for ind, l in enumerate(li):
        if l != min_id+ind:
            return min_id+ind
    return None

if __name__ == "__main__":
    file_path = "input.txt"
    bp_ids = read_file(file_path, strip=True)
    bp_seats = sorted([BoardingPass(bp_id).seat_id for bp_id in bp_ids])
    min_id, max_id = bp_seats[0], bp_seats[-1]
    print(f"PART 1 : {max_id}")

    #seat_range = set(list(range(min_id, max_id+1)))
    #print(seat_range.difference(set(bp_seats)))
    missing = find_missing_in_cnt_range(bp_seats, min_id)
    print(f"PART 2: {missing}")
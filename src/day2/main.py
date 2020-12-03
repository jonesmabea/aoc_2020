from src.util import read_file, parse_password_and_policy, verify_new_pass_validity, verify_old_pass_validity


if __name__ == "__main__":
    lines = read_file("input.txt")
    ## PART 1
    valid_cnt=0
    for line in lines:
        password,letter_constraint, min_max_len = parse_password_and_policy(line)
        valid = verify_old_pass_validity(password, letter_constraint, min_max_len)
        valid_cnt+=valid
    print(f"Num valid passwords = {valid_cnt}")

    ## PART 2
    valid_cnt=0
    for line in lines:
        password,letter_constraint, min_max_len = parse_password_and_policy(line)
        valid = verify_new_pass_validity(password, letter_constraint, min_max_len)
        valid_cnt+=valid
    print(f"Num valid passwords 2 = {valid_cnt}")

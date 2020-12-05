from src.classes import BatchProcessor, Passport

if __name__ == "__main__":
    file_path = "input.txt"
    entries = BatchProcessor().parse_batch_file(file_path)
    passports = [Passport(entry) for entry in entries]
    valid_passports = [passport for passport in passports if passport.validate_passport()]
    passports_with_valid_attributes =  [passport for passport in valid_passports if passport.validate_attributes()]

    print(f"PART 1: {len(valid_passports)}")
    print(f"PART 2: {len(passports_with_valid_attributes)}")
import numpy as np

def check_solved_count(file_path, target_string="Solved!", expected_count=6):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        actual_count = content.count(target_string)

        if actual_count == expected_count:
            print(f'{file_path}: The string "{target_string}" appears exactly {expected_count} times.')
            return True
        else:
            print(f'{file_path}: The string "{target_string}" appears {actual_count} times (expected {expected_count}).')
            return False

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False

"""
Checked:
- 0.0 - 100.0
- 70.00 - 100.00
"""
for i in range(9400, 10000, 1):
    index = i/100
    index = "{:.2f}".format(index)
    html_file = f"bruteforce_folder/response_{index}.html"
    # check_solved_count(html_file)
    if check_solved_count(html_file, expected_count=4) is True:
        break
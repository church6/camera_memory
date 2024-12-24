#!/usr/bin/python3
# pylint: disable=C0301
"""
# @filename    :  pytest3_log.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-08-06T14:04:00+08:00
# @require     :  Python 3.12.3
"""

import os
import time
import argparse
import csv
import re
import csv_table_head


PYTEST3_LOG_CONFTEST_SETUP_BATTERY_CAPACITY_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera conftest.py setup \s*[\d]+ battery_capacity=[\d]+$"
)
PYTEST3_LOG_CONFTEST_TEARDOWN_BATTERY_CAPACITY_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera conftest.py teardown \s*[\d]+ battery_capacity=[\d]+$"
)

# PYTEST3_LOG_OPEN_CAMERA_REGEX = re.compile(r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera base.py open_camera \s*[\d]+ leave$")
# PYTEST3_LOG_CLOSE_CAMERA_REGEX = re.compile(r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera base.py close_camera \s*[\d]+ enter$")

PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera conftest.py setup \s*[\d]+ \[setup\](\S*),(\S*)\[[\d]+\]$"
)
PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera conftest.py teardown \s*[\d]+ \[teardown\](\S*),(\S*)\[[\d]+\]$"
)
PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera (test_.*\.py) (test_\S*) \s*[\d]+ \[enter\]count=[\d]+$"
)
PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) ([\d]+) camera (test_.*\.py) (test_\S*) \s*[\d]+ \[leave\]count=[\d]+$"
)


def truncate(pathname):
    """
    Function :
    """
    # sanity check
    assert pathname is not None
    normal_path = os.path.normpath(pathname)
    array = normal_path.split(os.sep)
    found = 0
    for index, each in enumerate(array):
        if each == "camera" and array[index + 1] == "cases":
            found = index + 1
            break
    # print(f"found = {found}")
    return os.sep.join(array[found + 1 :])


def parse(input_file):
    """
    Function :
    """
    # pylint: disable=R0915
    # sanity check
    assert input_file is not None
    lines = []
    with open(input_file, mode="r", encoding="utf-8") as file:
        lines = file.read().splitlines()

    length = len(csv_table_head.PYTEST3_LOG_CASE_CAMERA_HEAD)
    assert length == 4
    testcase = ["", "", "", ""]
    rows = []

    # testcase : Dict[str, str] = {"filename": "", "casename": "", "case setup": "", "case teardown": ""}
    battery_capacity_count = 0
    for line in lines:
        if "test_warmup_000" in line or "test_000_warmup_camera" in line:
            continue

        if battery_capacity_count < 2:
            matched = re.match(PYTEST3_LOG_CONFTEST_SETUP_BATTERY_CAPACITY_REGEX, line)
            if matched:
                # print(matched.groups())
                battery_capacity_count += 1
                continue
            matched = re.match(PYTEST3_LOG_CONFTEST_TEARDOWN_BATTERY_CAPACITY_REGEX, line)
            if matched:
                # print(matched.groups())
                battery_capacity_count += 1
                continue
        # print(f"battery_capacity_count={battery_capacity_count}")
        if battery_capacity_count < 2:
            continue

        matched = re.match(PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX, line)
        if matched:
            # print(f"file={matched.groups()}")
            node_fspath = truncate(matched.groups()[2])
            node_name = matched.groups()[3]
            # print(f"PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX: {node_fspath},{node_name}")
            if testcase[0] != "":
                #### print(testcase)
                testcase = ["", "", "", ""]

            assert testcase[0] == "", "PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX"
            assert testcase[1] == "", "PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX"
            assert testcase[2] == "", "PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX"
            assert testcase[3] == "", "PYTEST3_LOG_CONFTEST_FUNCTION_SETUP_REGEX"

            testcase[0] = node_fspath
            testcase[1] = node_name
            testcase[2] = matched.groups()[0]
            continue
        matched = re.match(PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX, line)
        if matched:
            # print(f"enter={matched.groups()}")
            filename = matched.groups()[2]
            casename = matched.groups()[3]
            # print(f"PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX: {filename},{casename}")

            assert testcase[0] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            assert testcase[1] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            assert testcase[2] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            assert testcase[3] == "", "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            assert filename in testcase[0], "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            assert casename == testcase[1], "PYTEST3_LOG_TESTCASE_FUNCTION_ENTER_REGEX"
            continue
        matched = re.match(PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX, line)
        if matched:
            # print(f"leave={matched.groups()}")
            filename = matched.groups()[2]
            casename = matched.groups()[3]
            # print(f"PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX: {filename},{casename}")

            assert testcase[0] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            assert testcase[1] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            assert testcase[2] != "", "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            assert testcase[3] == "", "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            assert filename in testcase[0], "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            assert casename == testcase[1], "PYTEST3_LOG_TESTCASE_FUNCTION_LEAVE_REGEX"
            continue

        matched = re.match(PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX, line)
        if matched:
            # print(f"file={matched.groups()}")
            node_fspath = truncate(matched.groups()[2])
            node_name = matched.groups()[3]
            # print(f"PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX: {node_fspath},{node_name}")

            assert testcase[0] != "", "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            assert testcase[1] != "", "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            assert testcase[2] != "", "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            assert testcase[3] == "", "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            assert node_fspath == testcase[0], "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            assert node_name == testcase[1], "PYTEST3_LOG_CONFTEST_FUNCTION_TEARDOWN_REGEX"
            testcase[3] = matched.groups()[0]
            rows.append(testcase)
            testcase = ["", "", "", ""]
            continue

    return rows


def process(input_file, output_dir):
    """
    Function :
    """
    # sanity check
    assert input_file is not None
    assert output_dir is not None
    stemname = "pytest3"
    rows = parse(input_file)
    filename = os.path.join(output_dir, f"{stemname}_0.csv")
    # print(filename)
    with open(file=filename, mode="w", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(csv_table_head.PYTEST3_LOG_CASE_CAMERA_HEAD)
        for row in rows:
            csvwriter.writerow(row)
    filename = os.path.join(output_dir, f"{stemname}_0.py")
    # print(filename)
    write_list_module(filename, csv_table_head.PYTEST3_LOG_CASE_CAMERA_HEAD, "PYTEST3_LOG_CASE_CAMERA_HEAD", rows)


def get_files_size(filename):
    """
    Function :
    """
    # sanity check
    assert filename is not None
    input_files_dict = {}
    if not os.path.exists(filename):
        return input_files_dict
    with open(file=filename, mode="r", encoding="utf-8") as file:
        for line in file:
            matched = re.match(re.compile(r"^    \"([\S]+)\" = ([\d]+),$"), line)
            if matched:
                file_name = matched.groups()[0]
                file_size = int(matched.groups()[1])
                input_files_dict[file_name] = file_size
    return input_files_dict


def write_files_size(filename, input_files_dict):
    """
    Function :
    """
    # sanity check
    assert filename is not None
    assert input_files_dict is not None
    with open(file=filename, mode="w", encoding="utf-8") as file:
        file.write("# pylint: disable=C0302\n")
        file.write('"""\n')
        file.write(f"# This file is generated automatically by {__file__}\n")
        # file.write(f'# date: {datetime.now()}\n')
        file.write('"""\n')
        file.write("__all__ = ['FILE_SIZE']\n")
        file.write("FILE_SIZE = {\n")
        for file_name, file_size in input_files_dict.items():
            file.write(f'    "{file_name}" = {file_size},\n')
        file.write("}\n")


def write_list_module(filename, header, name, rows):
    """
    Function :
    """
    # sanity check
    assert filename is not None
    assert header is not None
    assert name is not None
    assert rows is not None
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write("# pylint: disable=C0302\n")
        file.write('"""\n')
        file.write(f"# This file is generated automatically by {__file__}\n")
        # file.write(f'# date: {datetime.now()}\n')
        file.write('"""\n')
        file.write(f"__all__ = ['{name}']\n")
        file.write(f"{name} = [\n")
        count = 0
        for row in rows:
            nvps = []
            for index, value in enumerate(header):
                if value.lower() in ["filename", "casename", "case setup", "case teardown"]:
                    nvps.append(f"'{value}': '{row[index]}'")
                else:
                    nvps.append(f"'{value}': {row[index]}")
            file.write(f"    {{{','.join(nvps)}}},")
            count += 1
            if count % 16 == 0:
                file.write("\n")
        file.write("\n]\n")


def check_files_size_same(input_file, output_dir) -> bool:
    """
    Function :
    """
    # sanity check
    assert input_file is not None
    assert output_dir is not None
    file_size = os.path.getsize(input_file)
    filename = os.path.join(output_dir, "pytest3_log_size.py")
    input_files_dict = get_files_size(filename)
    if input_files_dict is not None and input_file in input_files_dict:
        if file_size == input_files_dict[input_file]:
            print(f"# {input_file} = {file_size}")
            print("duplicated")
            return True
    input_files_dict[input_file] = file_size
    write_files_size(filename, input_files_dict)
    return False


def work():
    """
    Function : work
    """
    # sanity check
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, action="store", default=None, dest="input", help="input file")
    parser.add_argument("-o", "--output", type=str, action="store", default=None, dest="output", help="output file")
    given = parser.parse_args()
    if None in [given.input]:
        parser.print_help()
        return

    if not os.path.exists(given.input):
        print(f"{given.input}: No such file or directory")
        return
    print(f"# input  = {given.input}")
    print(f"# output = {given.output}")

    # if check_files_size_same(given.input, given.output):
    #    return
    process(given.input, given.output)


def measurer(func):
    """
    Function : measurer
    """

    def wrapper(*args, **kwargs):
        """
        Function : wrapper
        """
        start = time.time()
        func(*args, **kwargs)
        print(f"# elapsed time:{time.time() - start}")

    return wrapper


# @measurer
def main():
    """
    Function : main
    """
    work()


if __name__ == "__main__":
    main()

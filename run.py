#!/usr/bin/python3
"""
# @filename    :  run.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-12-12T12:37:38+08:00
# @require     :  Python 3.12.3
"""

from typing import Dict, Union
import os
import re
import argparse
from utils.constants import PYTEST_LOGS_DIRECTORY, PROJECT_ROOT_DIRECTORY
from utils.run import run

PYTEST_DIRECTORY_REGEX = re.compile(r"^pytest_([0-9A-Za-z:\.]{6,20})_([\d]{8}_[\d]{6})$")


def get_logger_directories(serial_number: Union[str, None] = None):
    """
    Function :
    """
    # sanity check
    directories: Dict[str, str] = {}
    for entry in os.scandir(PYTEST_LOGS_DIRECTORY):
        if entry.is_dir(follow_symlinks=False):
            matched = re.match(PYTEST_DIRECTORY_REGEX, entry.name)
            if not matched:
                # print(entry.name)
                continue
            pytest_directory_serial_number = matched.groups()[0]
            pytest_directory_timestamp = matched.groups()[1]
            if serial_number is not None and serial_number != pytest_directory_serial_number:
                # filter by serial_number
                continue
            directories[entry.path] = [pytest_directory_serial_number, pytest_directory_timestamp]
    return directories


def traverse(serial_number: Union[str, None] = None, output_filename: Union[str, None] = None):
    """
    Function :
    """
    # sanity check
    assert output_filename is not None
    assert output_filename != ""
    logger_directories = get_logger_directories(serial_number)
    # print(logger_directories)
    with open(file=output_filename, mode="w", encoding="utf-8") as file:
        for logger_directory in logger_directories:
            # print(logger_directory)
            command = ["python3", os.path.join(PROJECT_ROOT_DIRECTORY, "analyze.py"), "-p", logger_directory]
            file.write(" ".join(command) + "\n")
            get = run(command=" ".join(command), timeout=None)
            file.write(get.capture)
            file.flush()


def main():
    """
    Function : main
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--serial_number", action="store", default=None, dest="serial_number", help="serial_number")
    parser.add_argument("-o", "--output", action="store", default=None, dest="output", help="output")
    given = parser.parse_args()
    if given.output is None or given.output == "":
        parser.print_help()
        return

    self_output_filename = os.path.join(given.output, "camera_memory.txt")
    print(self_output_filename)
    traverse(serial_number=given.serial_number, output_filename=self_output_filename)


if __name__ == "__main__":
    main()

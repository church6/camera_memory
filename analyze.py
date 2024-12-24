#!/usr/bin/python3
"""
# @filename    :  analyze.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-08-06T17:01:59+08:00
# @require     :  Python 3.12.3
# @function    :
"""

import os
import re
import argparse
import shutil
from utils.run import measurer, run

PROJECT_ROOT_DIRECTORY = os.path.dirname(os.path.abspath(os.path.realpath(__file__)))
APPINFO_LOG_REGEX = re.compile(r"^appinfo\.log.*$")
PYTEST_DIRECTORY_REGEX = re.compile(r"^pytest_([0-9A-Za-z:\.]{6,20})_([\d]{8}_[\d]{6})$")


def work():
    """
    Function : work
    """
    # sanity check
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pytest", action="store", default=None, dest="pytest", help="pytest directory")
    parser.add_argument("-c", "--console", action="store_true", default=False, dest="console", help="console log")
    parser.add_argument("-g", "--graph", action="store_true", default=False, dest="graph", help="graph")
    given = parser.parse_args()

    if given.pytest is None:
        parser.print_help()
        return
    if not os.path.exists(given.pytest):
        print(f"{given.pytest}: No such file or directory")
        return
    print(f"# pytest directory = {given.pytest}")
    pytest_directory_basename = os.path.basename(os.path.abspath(given.pytest))
    matched = re.match(PYTEST_DIRECTORY_REGEX, pytest_directory_basename)
    if not matched:
        print(f"{given.pytest}: Invalid pytest directory")
        return

    appinfo_dir = os.path.join(given.pytest, "appinfo")
    if not os.path.exists(appinfo_dir):
        print(f"{appinfo_dir}: No such file or directory")
        return
    appinfo_logs = []
    for entry in os.scandir(appinfo_dir):
        if entry.is_file(follow_symlinks=False):
            matched = re.match(APPINFO_LOG_REGEX, entry.name)
            if matched:
                appinfo_logs.append(entry.path)
    graphs_dir = os.path.join(appinfo_dir, f"{pytest_directory_basename}_graphs")
    os.makedirs(graphs_dir, exist_ok=True)
    shutil.copy2(os.path.join(PROJECT_ROOT_DIRECTORY, "graphbig.py"), graphs_dir)
    shutil.copy2(os.path.join(PROJECT_ROOT_DIRECTORY, "graphcase.py"), graphs_dir)
    shutil.copytree(
        os.path.join(PROJECT_ROOT_DIRECTORY, "trends"),
        os.path.join(graphs_dir, "trends"),
        symlinks=False,
        ignore=None,
        dirs_exist_ok=True,
    )
    shutil.copytree(
        os.path.join(PROJECT_ROOT_DIRECTORY, "pymannkendall"),
        os.path.join(graphs_dir, "pymannkendall"),
        symlinks=False,
        ignore=None,
        dirs_exist_ok=True,
    )
    command = ["python3", os.path.join(PROJECT_ROOT_DIRECTORY, "appinfo_log.py")]
    for each in sorted(appinfo_logs):
        command.append("-i")
        command.append(each)
    command.append("-o")
    command.append(graphs_dir)
    # print(" ".join(command))
    get = run(" ".join(command), timeout=None)
    print(get.capture, flush=True)

    if given.console:
        command = [
            "python3",
            os.path.join(PROJECT_ROOT_DIRECTORY, "pytest3_log.py"),
            "-i",
            os.path.join(given.pytest, "camera", "pytest.log"),
            "-o",
            graphs_dir,
        ]
        # print(" ".join(command))
        get = run(" ".join(command), timeout=None)
        print(get.capture, flush=True)

    if given.graph:
        command = ["python3", os.path.join(graphs_dir, "graphbig.py")]
        # print(" ".join(command))
        get = run(" ".join(command), timeout=None)
        print(get.capture, flush=True)

        command = ["python3", os.path.join(graphs_dir, "graphcase.py")]
        # print(" ".join(command))
        get = run(" ".join(command), timeout=None)
        print(get.capture, flush=True)


@measurer(logger=None)
def main():
    """
    Function : main
    """
    work()


if __name__ == "__main__":
    main()

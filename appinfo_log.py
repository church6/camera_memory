#!/usr/bin/python3
# pylint: disable=C0301
"""
# @filename    :  appinfo_log.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-08-06T14:04:00+08:00
# @require     :  Python 3.12.3
"""

import os
import time
import argparse
import csv
import re
from collections import OrderedDict
import csv_table_head

FOREGROUND_RED = "\033[31m"
ENDCOLOR = "\033[0m"

APPINFO_LOG_DUMPSYS_MEMINFO_PID_REGEX = re.compile(r"^\*\* MEMINFO in pid ([\d]+) \[com.hmdglobal.app.camera\] \*\*$")
APPINFO_LOG_DUMPSYS_MEMINFO_TIMESTAMP_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) com\.hmdglobal\.app\.camera=([\d]+)$"
)
#           Pss  Private  Private     Swap      Rss     Heap     Heap     Heap
#         Total    Dirty    Clean    Dirty    Total     Size    Alloc     Free
#        ------   ------   ------   ------   ------   ------   ------   ------
# TOTAL    48191    27504    15076      148   184440    31057    19536     6854

# [enter]MEMINFO
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0_STATS_REGEX = re.compile(
    r"^\s*TOTAL\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*([\d]+)\s*$"
)
# [leave]MEMINFO

# Objects
#           Views:      227         ViewRootImpl:        1
#     AppContexts:       16           Activities:        1
#          Assets:       52        AssetManagers:        0
#   Local Binders:       37        Proxy Binders:       51
#   Parcel memory:       19         Parcel count:       68
# Death Recipients:        5             WebViews:        0

# [enter]Objects
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_0_REGEX = re.compile(r"^\s*Views:\s*([\d]+)\s*ViewRootImpl:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_1_REGEX = re.compile(r"^\s*AppContexts:\s*([\d]+)\s*Activities:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_2_REGEX = re.compile(r"^\s*Assets:\s*([\d]+)\s*AssetManagers:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_3_REGEX = re.compile(r"^\s*Local Binders:\s*([\d]+)\s*Proxy Binders:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_4_REGEX = re.compile(r"^\s*Parcel memory:\s*([\d]+)\s*Parcel count:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_5_REGEX = re.compile(r"^\s*Death Recipients:\s*([\d]+)\s*WebViews:\s*([\d]+)$")
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_LIST = (
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_0_REGEX,
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_1_REGEX,
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_2_REGEX,
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_3_REGEX,
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_4_REGEX,
    APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_5_REGEX,
)
# [leave]Objects


# [enter][procrank]
APPINFO_LOG_PROCRANK_MEMORY_TIMESTAMP_REGEX = re.compile(
    r"^([\d]{4}-[\d]{2}-[\d]{2} [\d]{2}:[\d]{2}:[\d]{2}.[\d]{6}) vendor\.qti\.camera\.provider@2\.7\-service_64=([\d]+)$"
)
#  PID       Vss      Rss      Pss      Uss     Swap    PSwap    USwap    ZSwap  cmdline
# 1290  14373960K  106864K  100111K  100044K   39700K   39700K   39700K   11106K  /vendor/bin/hw/vendor.qti.camera.provider@2.7-service_64
VENDOR_QTI_CAMERA_PROVIDER_FILENAME = "vendor.qti.camera.provider@2.7-service_64"
VENDOR_QTI_CAMERA_PROVIDER_FULLNAME = os.path.join("/vendor/bin/hw", VENDOR_QTI_CAMERA_PROVIDER_FILENAME)
APPINFO_LOG_PROCRANK_MEMORY_STATS_REGEX = re.compile(
    rf"^\s*([\d]+)\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*([\d]+)K\s*({re.escape(VENDOR_QTI_CAMERA_PROVIDER_FULLNAME)})$"
)
# [leave][procrank]


def parse(input_files):
    """
    Function :
    """
    # pylint: disable=R0912
    # pylint: disable=R0914
    # sanity check
    assert input_files is not None
    assert len(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0) == 10
    assert len(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1) == 14
    timestamp_dumpsys, row_dumpsys, rows0_dumpsys, rows1_dumpsys = None, [False] * 14, [], []

    assert len(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2) == 11
    row_procrank, rows_procrank = [0] * 11, OrderedDict()
    lines = []
    for each in input_files:
        with open(file=each, mode="r", encoding="utf-8") as file:
            lines.extend(file.read().splitlines())
    for line in lines:
        # [enter][procrank]
        matched = re.match(APPINFO_LOG_PROCRANK_MEMORY_TIMESTAMP_REGEX, line)
        if matched:
            # print(matched.groups())
            row_procrank[0] = matched.groups()[0]
            continue
        matched = re.match(APPINFO_LOG_PROCRANK_MEMORY_STATS_REGEX, line)
        if matched:
            # print(matched.groups())
            pid, pss, uss = int(matched.groups()[0]), int(matched.groups()[3]), int(matched.groups()[4])
            if pss > 786432:  # 768*1024KB
                print(f"{row_procrank[0]} {VENDOR_QTI_CAMERA_PROVIDER_FILENAME} Pss: {pss} > threshold 768MB")
            if uss > 786432:  # 768*1024KB
                print(f"{row_procrank[0]} {VENDOR_QTI_CAMERA_PROVIDER_FILENAME} Uss: {uss} > threshold 768MB")
            row_procrank = [row_procrank[0]] + list(matched.groups())
            row_procrank[10] = VENDOR_QTI_CAMERA_PROVIDER_FILENAME
            if pid in rows_procrank:
                rows_procrank[pid].append(row_procrank)
            else:
                rows_procrank[pid] = [row_procrank]
            row_procrank = [0] * 11
            continue
        # [leave][procrank]

        # [enter][dumpsys]
        matched = re.match(APPINFO_LOG_DUMPSYS_MEMINFO_PID_REGEX, line)
        if matched:
            # print(matched.groups())
            row_dumpsys[1] = matched.groups()[0]
            continue
        matched = re.match(APPINFO_LOG_DUMPSYS_MEMINFO_TIMESTAMP_REGEX, line)
        if matched:
            # print(matched.groups())
            row_dumpsys[0] = matched.groups()[0]
            timestamp_dumpsys = matched.groups()[0]
            continue
        matched = re.match(APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0_STATS_REGEX, line)
        if matched:
            # print(matched.groups())
            rows0_dumpsys.append([timestamp_dumpsys, row_dumpsys[1]] + list(matched.groups()))
            continue
        for index, regex in enumerate(APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_LIST):
            matched = re.match(regex, line)
            if matched:
                # print(matched.groups())
                row_dumpsys[2 + 2 * index], row_dumpsys[3 + 2 * index] = matched.groups()[0], matched.groups()[1]
                if index == len(APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1_STATS_LIST) - 1 and False not in row_dumpsys:
                    rows1_dumpsys.append(row_dumpsys)
                    row_dumpsys = [False] * 14
        # [leave][dumpsys]

    return rows0_dumpsys, rows1_dumpsys, rows_procrank


def process(input_files, output_dir):
    """
    Function :
    """
    # sanity check
    assert input_files is not None
    assert output_dir is not None
    stemname = "appinfo"
    rows0, rows1, rows2 = parse(input_files)
    filename = os.path.join(output_dir, f"{stemname}_0.csv")
    # print(filename)
    with open(file=filename, mode="w", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0)
        for row in rows0:
            csvwriter.writerow(row)
    filename = os.path.join(output_dir, f"{stemname}_0.py")
    # print(filename)
    write_list_module(filename, csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0, "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0", rows0)

    filename = os.path.join(output_dir, f"{stemname}_1.csv")
    # print(filename)
    with open(file=filename, mode="w", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1)
        for row in rows1:
            csvwriter.writerow(row)
    filename = os.path.join(output_dir, f"{stemname}_1.py")
    # print(filename)
    write_list_module(filename, csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1, "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1", rows1)

    filename = os.path.join(output_dir, f"{stemname}_2.csv")
    # print(filename)
    with open(file=filename, mode="w", encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2)
        for key in sorted(rows2):
            for row in rows2[key]:
                csvwriter.writerow(row)
    filename = os.path.join(output_dir, f"{stemname}_2.py")
    # print(filename)
    write_dict_module(filename, csv_table_head.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2, "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2", rows2)
    if len(rows2.keys()) > 1:
        print(f"{FOREGROUND_RED}provider crashed{ENDCOLOR}")
    for pid in rows2:
        print(f"pid = {pid}")


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
                if value.lower() in ["time", "cmdline"]:
                    nvps.append(f"'{value}': '{row[index]}'")
                else:
                    nvps.append(f"'{value}': {row[index]}")
            file.write(f"    {{{','.join(nvps)}}},")
            count += 1
            if count % 16 == 0:
                file.write("\n")
        file.write("\n]\n")


def write_dict_module(filename, header, name, rows):
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
        file.write(f"{name} = {{\n")

        for key in sorted(rows.keys()):
            file.write(f'    "{key}": [\n')
            count = 0
            for row in rows[key]:
                nvps = []
                for index, value in enumerate(header):
                    if value.lower() in ["time", "cmdline"]:
                        nvps.append(f"'{value}': '{row[index]}'")
                    else:
                        nvps.append(f"'{value}': {row[index]}")
                file.write(f"    {{{','.join(nvps)}}},")
                count += 1
                if count % 16 == 0:
                    file.write("\n")
            file.write("\n    ],\n")
        file.write("\n}\n")


def check_files_size_same(input_files, output_dir) -> bool:
    """
    Function :
    """
    # sanity check
    assert input_files is not None
    assert output_dir is not None
    filename = os.path.join(output_dir, "appinfo_log_size.py")
    input_files_dict = get_files_size(filename)
    if input_files_dict is not None:
        matched = True
        for each in input_files:
            updated = os.path.getsize(each)
            if each not in input_files_dict:
                input_files_dict[each] = updated
                matched = False
                continue
            if updated != input_files_dict[each]:
                input_files_dict[each] = updated
                matched = False
                print(f"# {each} = {input_files_dict[each]}")
                continue
        if matched:
            print("duplicated")
            return True
    write_files_size(filename, input_files_dict)
    return False


def work():
    """
    Function : work
    """
    # sanity check
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, action="append", default=None, dest="input", help="input file")
    parser.add_argument("-o", "--output", type=str, action="store", default=None, dest="output", help="output file")
    given = parser.parse_args()
    if None in [given.input] or len(given.input) == 0:
        parser.print_help()
        return

    for each in given.input:
        if not os.path.exists(each):
            print(f"{each}: No such file or directory")
            return
    # print(f"# input  = {given.input}")
    # print(f"# output = {given.output}")

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

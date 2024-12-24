#!/usr/bin/python3
"""
# @filename    :  pytest3_log.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-08-06T14:04:00+08:00
# @require     :  Python 3.12.3
"""

from trends import get_trends


def work():
    """
    Function : work
    """
    data1 = [1, 2, 2, 1, 3, 4, 5, 8, 6, 9, 10]
    data2 = [2, 2, 3, 2, 5, 4, 3, 2, 6, 3, 4, 2, 3, 2, 3]
    nvps = get_trends(data1)
    for name, value in nvps.items():
        print(f"{name:32s} = {value}")
    nvps = get_trends(data2)
    for name, value in nvps.items():
        print(f"{name:32s} = {value}")


def main():
    """
    Function : main
    """
    work()


if __name__ == "__main__":
    main()

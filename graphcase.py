#!/usr/bin/python3
"""
# @filename    :  graphs.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

import os
import sys
import random
import time
from datetime import datetime
import numpy
import matplotlib
import matplotlib.pyplot as plot
from trends import get_trends

# import matplotlib.dates as mdates
# import re
# from datetime import datetime
# from datetime import timedelta

try:
    import appinfo_0
except ModuleNotFoundError as error:
    print(error)
    sys.exit(2)


try:
    import appinfo_1
except ModuleNotFoundError as error:
    print(error)
    sys.exit(2)


try:
    import pytest3_0
except ModuleNotFoundError as error:
    print(error)
    sys.exit(2)


WORK_DIR = os.path.dirname(os.path.abspath(__file__))
DRAW_ENABLED = False


def clean_plot(figure, plt):
    """
    Function :
    """
    # sanity check
    assert figure is not None
    assert plt is not None
    figure.clear()
    plt.close("all")
    plt.cla()
    plt.clf()


def draw_1lines(directory, title, xaxis, label1, y1axis):
    """
    Function :
    """
    # sanity check
    assert directory is not None
    assert title is not None
    assert xaxis is not None
    assert label1 is not None
    assert y1axis is not None
    if not DRAW_ENABLED:
        return
    if len(xaxis) == 0:
        print(f"truncated: {title}")
        return
    assert len(xaxis) == len(y1axis)
    if len(xaxis) == 1:
        xaxis = [xaxis[0] - 1, xaxis[0], xaxis[0] + 1]
        y1axis = [y1axis[0] - 1, y1axis[0], y1axis[0] + 1]

    filename = os.path.join(directory, f"{title}.svg")

    fig = plot.figure(figsize=(32, 18))
    # plotting the line 1 points
    plot.scatter(xaxis, y1axis, label=label1, color="red", s=2)

    samples = random.sample(range(0, len(y1axis)), min([len(y1axis), 5]))
    integers = [isinstance(y1axis[x], int) for x in samples]
    if all(integers):
        minimum = min(y1axis)
        maximum = max(y1axis)
        # print(f'# minimum = {minimum} , maximum = {maximum}')
        if maximum > 40:
            plot.yticks(numpy.arange(minimum, maximum + 1, int(maximum / 40)))

    # naming the x axis
    plot.xlabel("time")
    # naming the y axis
    plot.ylabel("Y")
    # giving a title to my graph
    plot.title(title)

    plot.gca().title.set_color("lime")
    plot.gca().set_axisbelow(True)
    plot.gca().xaxis.grid(color="gray", linestyle="dashed")
    plot.gca().yaxis.grid(color="gray", linestyle="dashed")
    # plot.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    # plot.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=2))
    # plot.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=5))
    # plot.gcf().autofmt_xdate()
    plot.gca().xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(500))
    plot.gca().yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.0f}"))
    plot.xticks(rotation=90)

    # show a legend on the plot
    plot.legend()

    # https://stackoverflow.com/questions/32428193
    # QT backend
    # manager = plot.get_current_fig_manager()
    # manager.window.showMaximized()

    plot.tight_layout()
    plot.margins(x=0)
    # function to show the plot
    # plot.show()

    plot.savefig(filename, bbox_inches="tight")
    clean_plot(fig, plot)


def write_appinfo_ini(output_file, filename, casename, ynaxis):
    """
    Function :
    """
    header = list(ynaxis.keys())
    with open(file=output_file, mode="w", encoding="utf-8") as file:
        file.write("[case]\n")
        file.write(f"filename={filename}\n")
        file.write(f"casename={casename}\n")
        for key in header:
            file.write(f'[appinfo_{key.replace(" ", "_")}]\n')
            nvps = get_trends(ynaxis[key])
            for name, value in nvps.items():
                file.write(f"{name:32s} = {value}\n")


def draw_meminfo_0(index, timestamp_range, data, filename, casename):
    """
    Function :
    """
    # sanity check
    enter_txt, leave_txt = timestamp_range
    ynaxis = {
        # "Time",
        "Pss Total": [],  # Kilobytes
        "Private Dirty": [],  # Kilobytes
        "Private Clean": [],  # Kilobytes
        "Swap Dirty": [],  # Kilobytes
        "Rss Total": [],  # Kilobytes
        "Heap Size": [],  # Kilobytes
        "Heap Alloc": [],  # Kilobytes
        "Heap Free": [],  # Kilobytes
    }
    header = list(ynaxis.keys())
    for each in data:
        for key in header:
            ynaxis[key].append(each[key])
    xaxis = list(range(len(data)))
    directory = os.path.join(WORK_DIR, f"case_{index:04d}_{enter_txt}_{leave_txt}")
    os.makedirs(directory, exist_ok=True)
    for key in header:
        draw_1lines(directory, f'appinfo_0_{key.replace(" ", "_")}', xaxis, key, ynaxis[key])
    output_file = os.path.join(directory, "appinfo_0_trends.ini")
    write_appinfo_ini(output_file, filename, casename, ynaxis)


def draw_meminfo_1(index, timestamp_range, data, filename, casename):
    """
    Function :
    """
    # sanity check
    enter_txt, leave_txt = timestamp_range
    ynaxis = {
        # "Time",
        "Views": [],
        "ViewRootImpl": [],
        "AppContexts": [],
        "Activities": [],
        "Assets": [],
        "AssetManagers": [],
        "Local Binders": [],
        "Proxy Binders": [],
        "Parcel memory": [],
        "Parcel count": [],
        "Death Recipients": [],
        "WebViews": [],
    }
    header = list(ynaxis.keys())
    for each in data:
        for key in header:
            ynaxis[key].append(each[key])
    xaxis = list(range(len(data)))
    directory = os.path.join(WORK_DIR, f"case_{index:04d}_{enter_txt}_{leave_txt}")
    os.makedirs(directory, exist_ok=True)
    for key in header:
        draw_1lines(directory, f'appinfo_1_{key.replace(" ", "_")}', xaxis, key, ynaxis[key])
    output_file = os.path.join(directory, "appinfo_1_trends.ini")
    write_appinfo_ini(output_file, filename, casename, ynaxis)


def draw_pytest3_0():
    """
    Function :
    """
    # sanity check
    for index, each in enumerate(pytest3_0.PYTEST3_LOG_CASE_CAMERA_HEAD):
        enter_time = datetime.strptime(each["case setup"], "%Y-%m-%d %H:%M:%S.%f")
        leave_time = datetime.strptime(each["case teardown"], "%Y-%m-%d %H:%M:%S.%f")

        appinfo_0_data = []
        for item in appinfo_0.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0:
            item_time = datetime.strptime(item["Time"], "%Y-%m-%d %H:%M:%S.%f")
            if item_time < enter_time:
                continue
            if item_time > leave_time:
                break
            if enter_time <= item_time <= leave_time:
                appinfo_0_data.append(item)

        appinfo_1_data = []
        for item in appinfo_1.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1:
            item_time = datetime.strptime(item["Time"], "%Y-%m-%d %H:%M:%S.%f")
            if item_time < enter_time:
                continue
            if item_time > leave_time:
                break
            if enter_time <= item_time <= leave_time:
                appinfo_1_data.append(item)

        enter_txt = enter_time.strftime("%Y%m%d_%H%M%S")
        leave_txt = leave_time.strftime("%Y%m%d_%H%M%S")
        if len(appinfo_0_data) > 0:
            draw_meminfo_0(index, (enter_txt, leave_txt), appinfo_0_data, each["filename"], each["casename"])
        if len(appinfo_1_data) > 0:
            draw_meminfo_1(index, (enter_txt, leave_txt), appinfo_1_data, each["filename"], each["casename"])


def work():
    """
    Function : work
    """
    # sanity check
    draw_pytest3_0()


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

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
    import appinfo_2
except ModuleNotFoundError as error:
    print(error)
    sys.exit(2)


WORK_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPHS_DIR = os.path.join(WORK_DIR, "graphs")
os.makedirs(GRAPHS_DIR, exist_ok=True)


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


def draw_1lines(title, xaxis, label1, y1axis):
    """
    Function :
    """
    # sanity check
    assert title is not None
    assert xaxis is not None
    assert label1 is not None
    assert y1axis is not None
    if len(xaxis) == 0:
        print(f"truncated: {title}")
        return
    assert len(xaxis) == len(y1axis)
    if len(xaxis) == 1:
        xaxis = [xaxis[0] - 1, xaxis[0], xaxis[0] + 1]
        y1axis = [y1axis[0] - 1, y1axis[0], y1axis[0] + 1]

    filename = os.path.join(GRAPHS_DIR, f"{title}.svg")

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


def draw_meminfo_0():
    """
    Function :
    """
    # sanity check
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
    for each in appinfo_0.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0:
        for key in header:
            ynaxis[key].append(each[key])
    xaxis = list(range(len(appinfo_0.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0)))
    for key in header:
        draw_1lines(f'appinfo_0_{key.replace(" ", "_")}', xaxis, key, ynaxis[key])


def draw_meminfo_1():
    """
    Function :
    """
    # sanity check
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
    for each in appinfo_1.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1:
        for key in header:
            ynaxis[key].append(each[key])
    xaxis = list(range(len(appinfo_1.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1)))
    for key in header:
        draw_1lines(f'appinfo_1_{key.replace(" ", "_")}', xaxis, key, ynaxis[key])


def draw_meminfo_2(pid, data):
    """
    Function :
    """
    # sanity check
    assert pid is not None
    assert data is not None
    ynaxis = {
        # "Time",
        "PID": [],
        "Vss": [],
        "Rss": [],
        "Pss": [],
        "Uss": [],
        "Swap": [],
        "PSwap": [],
        "USwap": [],
        "ZSwap": [],
    }
    header = list(ynaxis.keys())
    for each in data:
        for key in header:
            ynaxis[key].append(each[key])
    xaxis = list(range(len(data)))
    for key in header:
        draw_1lines(f'appinfo_2_{pid}_{key.replace(" ", "_")}', xaxis, key, ynaxis[key])

    with open(file=os.path.join(GRAPHS_DIR, f"appinfo_2_{pid}_trends.ini"), mode="w", encoding="utf-8") as file:
        for key in header:
            if key not in ["Rss", "Vss", "Pss", "Uss"]:
                continue
            file.write(f'[appinfo_2_{pid}_{key.replace(" ", "_")}]\n')
            nvps = get_trends(ynaxis[key])
            for name, value in nvps.items():
                file.write(f"{name:32s} = {value}\n")


def work():
    """
    Function : work
    """
    # sanity check
    # draw_meminfo_0()
    # draw_meminfo_1()
    for key, value in appinfo_2.APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2.items():
        draw_meminfo_2(key, value)


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

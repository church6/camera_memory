"""
# @filename    :  csv_table_head.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-08-06T14:04:00+08:00
# @require     :  Python 3.12.3
"""

__all__ = [
    "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0",
    "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1",
    "APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2",
    "PYTEST3_LOG_CASE_CAMERA_HEAD",
]
# MEMINFO
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_0 = (
    "Time",
    "pid",
    "Pss Total",  # Kilobytes
    "Private Dirty",  # Kilobytes
    "Private Clean",  # Kilobytes
    "Swap Dirty",  # Kilobytes
    "Rss Total",  # Kilobytes
    "Heap Size",  # Kilobytes
    "Heap Alloc",  # Kilobytes
    "Heap Free",  # Kilobytes
)
# Objects
APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_1 = (
    "Time",
    "pid",
    "Views",
    "ViewRootImpl",
    "AppContexts",
    "Activities",
    "Assets",
    "AssetManagers",
    "Local Binders",
    "Proxy Binders",
    "Parcel memory",
    "Parcel count",
    "Death Recipients",
    "WebViews",
)

APPINFO_LOG_DUMPSYS_MEMINFO_HEAD_2 = ("Time", "PID", "Vss", "Rss", "Pss", "Uss", "Swap", "PSwap", "USwap", "ZSwap", "cmdline")
PYTEST3_LOG_CASE_CAMERA_HEAD = ("filename", "casename", "case setup", "case teardown")

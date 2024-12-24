"""
# @filename    :  constants.py
# @author      :  Copyright (C) Church.ZHONG
"""

import os
from pathlib import Path

################################################################
PROJECT_ROOT_DIRECTORY = str(Path(__file__).parent.parent)
DISK_ROOT_DIRECTORY = str(Path(PROJECT_ROOT_DIRECTORY).anchor)
PYTEST_LOGS_DIRECTORY = os.path.join(DISK_ROOT_DIRECTORY, "data", "ro", "camera_test_logs")
################################################################

################################################################
DUT_CAMERA_TEST_DCIM_DIRECTORY = "/sdcard/DCIM/Camera"
DUT_CAMERA_TEST_ADB_DIRECTORY = "/sdcard/Documents/camera_test"
DUT_CAMERA_TEST_BEGIN_TIMESTAMP_FILE = os.path.join(DUT_CAMERA_TEST_ADB_DIRECTORY, "pytest3_begin_timestamp.txt")
DUT_CAMERA_TEST_END_TIMESTAMP_FILE = os.path.join(DUT_CAMERA_TEST_ADB_DIRECTORY, "pytest3_end_timestamp.txt")
DUT_CAMERA_TEST_QUIT_INDICATOR_FILE = os.path.join(DUT_CAMERA_TEST_ADB_DIRECTORY, "pytest3_quit_indicator.txt")
################################################################

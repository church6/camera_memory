#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
import numpy


def get_trend(data: Union[List[int], None] = None):
    """
    Function :
    """
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    cusum = numpy.cumsum(numpy.diff(data))
    assert len(cusum) > 0
    return cusum[-1] > 0

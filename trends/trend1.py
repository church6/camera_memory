#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
import numpy


def moving_average(data: Union[List[int], None] = None, window_size: int = 3):
    """
    Function :
    """
    # sanity check
    return numpy.convolve(data, numpy.ones(window_size), "valid") / window_size


def get_trend(data: Union[List[int], None] = None) -> bool:
    """
    Function :
    """
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    mav = moving_average(data)
    assert len(mav) >= 2
    return mav[-1] > mav[0]

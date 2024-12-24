#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
import numpy
from statsmodels.nonparametric.smoothers_lowess import lowess


def get_trend(data: Union[List[int], None] = None, frac: float = 0.3):
    """
    Function :
    """
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    smoothed = lowess(data, numpy.arange(len(data)), frac=frac)
    assert len(smoothed) >= 2
    return smoothed[-1, 1] > smoothed[0, 1]

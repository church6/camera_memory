#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
import numpy
from scipy.stats import linregress


def get_trend(data: Union[List[int], None] = None) -> bool:
    """
    Function :
    """
    # pylint: disable=W0612
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    xaxis = numpy.arange(len(data))  # Independent variable
    yaxis = numpy.array(data)  # dependent variable
    # linear regression
    slope, intercept, r_value, p_value, std_err = linregress(xaxis, yaxis)
    if slope >= 0.2:
        # print(f"[trend0]{slope:.4f}, {intercept:.4f}, {r_value:.4f}, {p_value:.4f}, {std_err:.4f}")
        pass
    return slope > 0

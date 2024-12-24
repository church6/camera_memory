#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
from pymannkendall import original_test as mk_test


def get_trend(data: Union[List[int], None] = None) -> bool:
    """
    Function :
    """
    # pylint: disable=W0612
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    trend, h, p, z, tau, s, var_s, slope, intercept = mk_test(data)
    if trend == "increasing":
        # print(f"[trend2]{h}, {p:4f}, {z:.4f}, {tau:.4f}, {s:.4f}, {var_s:.4f}, {slope:.4f}, {intercept:.4f}")
        pass
    return trend == "increasing"

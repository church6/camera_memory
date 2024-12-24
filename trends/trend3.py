#!/usr/bin/python3
"""
# @filename    :  trend.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2023-04-28T15:48:32+08:00
"""

from typing import List, Union
import pandas


def get_trend(data: Union[List[int], None] = None, span: int = 3):
    """
    Function :
    """
    # sanity check
    assert data is not None
    if len(data) < 2:
        return False

    series = pandas.Series(data)
    ema = series.ewm(span=span, adjust=False).mean()
    assert len(ema) >= 2
    return ema.iloc[-1] > ema.iloc[0]

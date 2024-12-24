"""
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-04-08T16:09:59+08:00
"""

__version__ = "0.0.1"
__author__ = "Church ZHONG"

__all__ = ["get_trends"]

from typing import Dict, List, Union
import numpy
from .trend0 import get_trend as get_trend0
from .trend1 import get_trend as get_trend1
from .trend2 import get_trend as get_trend2
from .trend3 import get_trend as get_trend3
from .trend4 import get_trend as get_trend4
from .trend5 import get_trend as get_trend5


def get_trends(data: Union[List[int], None] = None) -> Dict[str, bool]:
    """
    Function :
    """
    # sanity check
    assert data is not None
    assert len(data) > 0
    vote0 = get_trend0(data=data)
    # vote1 = get_trend1(data=data)
    vote2 = get_trend2(data=data)
    # vote3 = get_trend3(data=data)
    # vote4 = get_trend4(data=data)
    array = []
    for frac in [0.3, 0.5, 0.7, 0.9, 1]:
        array.append(get_trend5(data=data, frac=frac))
    vote5 = numpy.mean(array) > 0.5
    voted = numpy.mean([vote0, vote2, vote5]) > 0.5
    return {
        "Linear Regression": vote0,
        # "Moving Average": vote1,
        "Mann-Kendall Trend Test": vote2,
        # "Exponential Moving Average": vote3,
        # "Cumulative Sum": vote4,
        "statsmodels LOWESS": vote5,
        "Voted": voted,
    }

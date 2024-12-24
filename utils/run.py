"""
# @filename    :  run.py
# @author      :  Copyright (C) Church.ZHONG
# @date        :  2024-01-04T11:16:46+08:00
# @require     :  Python 3.11.6
"""

import time
from typing import Union, List
import subprocess
import functools


class Result:
    """
    Class :
    """

    def __init__(self, status: bool = False, capture: str = "", error=None):
        self.status = status
        self.capture = capture
        self.error = error

    def __str__(self):
        returncode = -1
        output = ""
        if self.error:
            returncode = self.error.returncode
            output = self.error.output
        return f"Result: status={self.status},capture={self.capture},returncode={returncode},output={output}"

    def __repr__(self):
        returncode = -1
        output = ""
        if self.error:
            returncode = self.error.returncode
            output = self.error.output
        return f"Result({self.status}, {self.capture}, {returncode}, {output})"


def run(
    command: Union[List[str], str, None] = None, stdin=None, stderr=None, shell: bool = True, timeout=1024, block: bool = True
) -> Result:
    """
    Function :
    """
    # pylint: disable=W0012
    # pylint: disable=R0913
    # pylint: disable=R0917
    # sanity check
    assert command is not None
    status = False
    capture = ""
    error = None
    try:
        if block:
            capture = subprocess.check_output(
                command, stdin=stdin, stderr=stderr, shell=shell, timeout=timeout, encoding="utf-8"
            ).strip()
        else:
            with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell) as process:
                error = process.returncode
        status = True
    except subprocess.TimeoutExpired:
        cmdline = command if isinstance(command, str) else " ".join(command)
        print(f"TimeoutExpired: {cmdline}")
    except subprocess.CalledProcessError as err:
        error = err
    except subprocess.SubprocessError as err:
        error = err
    return Result(status, capture, error)


def measurer(logger=None):
    """
    Function : decorator
    """

    def measurer_wrapper(func):
        """
        Function :
        """

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            Function :
            """
            start = time.time()
            tail = func(*args, **kwargs)
            log_fn = logger.info if logger else print
            log_fn(f"# {func.__name__} elapsed time:{time.time() - start}")
            return tail

        return wrapper

    return measurer_wrapper

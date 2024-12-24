[![License: MIT](https://cdn.prod.website-files.com/5e0f1144930a8bc8aace526c/65dd9eb5aaca434fac4f1c34_License-MIT-blue.svg)](/LICENSE)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
![Pylint](https://github.com/church6/camera_memory/actions/workflows/pylint.yml/badge.svg)


# Camera Automated Test
[A pure Python3 automated tool suite for camera App testing, using pytest3+uiautomator2+allure2](https://github.com/church6/camera_test)


# Camera Memory Analyse
[Analyse memory/crash of camera app testing](https://github.com/church6/camera_memory)


# Static Code Analysis
* [x] ruff format --silent --config line-length=128 *.py
* [x] python3 -m black --line-length=128 --skip-string-normalization --skip-magic-trailing-comma *.py
* [x] python3 -m flake8 --jobs 4 --max-line-length=128 --indent-size=4 --extend-ignore=W191,E101,E203,E265,E266,E501,F401 --statistics *.py
* [x] pylint --jobs 4 --max-line-length={} --indent-after-paren=4 *.py
* [x] python3 -m mypy --check-untyped-defs *.py

# Thanks
* [pytest](https://github.com/pytest-dev/pytest)
* [uiautomator2](https://github.com/openatx/uiautomator2)
* [allure2](https://github.com/allure-framework/allure2)
* [numpy](https://github.com/numpy/numpy)
* [pandas](https://github.com/pandas-dev/pandas)
* [scipy](https://github.com/scipy/scipy)
* [retry](https://github.com/invl/retry)
* [pylint](https://github.com/pylint-dev/pylint)
* [ruff](https://github.com/astral-sh/ruff)
* [mypy](https://github.com/python/mypy)
* [procrank](https://android.googlesource.com/platform/system/extras/+/android-7.1.1_r45/procrank/procrank.c)
* [what is the best way of implementing singleton in python](https://stackoverflow.com/questions/6760685)


# About
analyse memory/crash of camera app testing


# Topics
memory numpy pandas python3 scipy pylint automated-testing procrank


# About
A pure Python3 automated tool suite for camera App testing, using pytest3+uiautomator2+allure2


# Topics
python3 pytest allure pylint mypy automated-testing uiautomator2 procrank

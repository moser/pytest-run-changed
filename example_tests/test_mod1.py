import time

from . import foo


def test_slow():
    foo.x()
    time.sleep(0.05)


def test_kind_of_slow():
    time.sleep(0.03)


def test_fastest():
    pass

import logging
import os.path
from ..code.main import Range, MappingRange

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))


def test_range_cut(caplog):
    caplog.set_level(logging.INFO)

    # Following Allen's interval algebra 13 relations

    # X < Y (X precedes Y)
    x = Range(0, 10)
    y = Range(50, 60)
    assert y.split(x) == [x]

    # X m Y (X meets Y in the boundary)
    x = Range(0, 100)
    y = Range(100, 200)
    assert y.split(x) == [Range(0, 99), Range(100, 100)]

    # X o Y (X overlaps with Y)
    x = Range(0, 150)
    y = Range(50, 200)
    assert y.split(x) == [Range(0, 49), Range(50, 150)]

    # X s Y (X starts Y)
    x = Range(0, 100)
    y = Range(0, 200)
    assert y.split(x) == [Range(0, 100)]

    # X d Y (X during Y, or Y contains X)
    x = Range(50, 100)
    y = Range(0, 150)
    assert y.split(x) == [Range(50, 100)]

    # X f Y (X finishes Y)
    x = Range(50, 100)
    y = Range(0, 100)
    assert y.split(x) == [Range(50, 100)]

    # X == Y
    x = Range(0, 100)
    y = Range(0, 100)
    assert y.split(x) == [Range(0, 100)]

    # Other cases
    x = Range(57, 69)
    y = Range(53, 60)
    assert y.split(x) == [Range(57, 60), Range(61, 69)]

    subject = Range(0, 100)
    cutter = Range(0, 100)
    assert cutter.split(subject) == [Range(0, 100)]

    subject = Range(0, 100)
    cutter = Range(20, 100)
    assert cutter.split(subject) == [Range(0, 19), Range(20, 100)]

    subject = Range(0, 101)
    cutter = Range(20, 100)
    assert cutter.split(subject) == [Range(0, 19), Range(20, 100), Range(101, 101)]

    subject = Range(0, 100)
    cutter = Range(0, 50)
    assert cutter.split(subject) == [Range(0, 50), Range(51, 100)]

    subject = Range(0, 100)
    cutter = Range(100, 200)
    assert cutter.split(subject) == [Range(0, 99), Range(100, 100)]

    subject = Range(100, 200)
    cutter = Range(0, 100)
    assert cutter.split(subject) == [Range(100, 100), Range(101, 200)]


def test_range_before():
    subject = Range(0, 100)
    cutter = Range(200, 300)
    assert cutter.split(subject) == [Range(0, 100)]


def test_range_after():
    subject = Range(100, 200)
    cutter = Range(0, 50)
    assert cutter.split(subject) == [Range(100, 200)]

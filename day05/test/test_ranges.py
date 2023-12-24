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
    assert y.cut(x) == [x]

    # X m Y (X meets Y in the boundary)
    x = Range(0, 100)
    y = Range(100, 200)
    assert y.cut(x) == [Range(0, 99), Range(100, 100)]

    # X o Y (X overlaps with Y)
    x = Range(0, 150)
    y = Range(50, 200)
    assert y.cut(x) == [Range(0, 49), Range(50, 150)]

    # X s Y (X starts Y)
    x = Range(0, 100)
    y = Range(0, 200)
    assert y.cut(x) == [Range(0, 100)]

    # X d Y (X during Y, or Y contains X)
    x = Range(50, 100)
    y = Range(0, 150)
    assert y.cut(x) == [Range(50, 100)]

    # X f Y (X finishes Y)
    x = Range(50, 100)
    y = Range(0, 100)
    assert y.cut(x) == [Range(50, 100)]

    # X == Y
    x = Range(0, 100)
    y = Range(0, 100)
    assert y.cut(x) == [Range(0, 100)]



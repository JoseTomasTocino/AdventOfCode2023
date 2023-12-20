import logging
import os.path
from ..code.main import part_one, part_two, RangeMap

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test_range_map(caplog):
    caplog.set_level(logging.INFO)
    m = RangeMap()

    m.add_range(50, 98, 2)
    m.add_range(52, 50, 48)

    assert m[0] == 0
    assert m[1] == 1
    assert m[50] == 52
    assert m[51] == 53
    assert m[96] == 98
    assert m[98] == 50
    assert m[99] == 51


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 35
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 424490994
        # assert part_two(content) == None

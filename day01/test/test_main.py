import logging
import os.path
from ..code.main import part_one, part_two, part_two_alt

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

sample_input2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

sample_input3 = """mhdzcmmsseven4three3bngxxqzclpkmcppxtwo"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    # assert part_one(sample_input) == 142
    # assert part_two_alt(sample_input2) == 281
    assert part_two(sample_input3) == 72


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 55712
        assert part_two(content) == 55413

import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """Time:      7  15   30
Distance:  9  40  200"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 288
    assert part_two(sample_input) == 71503


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 861300
        assert part_two(content) == 28101347

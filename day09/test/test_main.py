import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 114
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 1757008019
        # assert part_two(content) == None

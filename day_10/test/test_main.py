import logging
import os.path
from ..code.main import part_one, part_two

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """.....
.S-7.
.|.|.
.L-J.
....."""

sample_input_2 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""

def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 4
    assert part_one(sample_input_2) == 8
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == None
        # assert part_two(content) == None

import logging
import os.path

from ..code.main import part_one, part_two, Hand, HandType

logger = logging.getLogger(__name__)
local_path = os.path.abspath(os.path.dirname(__file__))

sample_input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test_hand_type(caplog):
    caplog.set_level(logging.INFO)

    assert Hand("AAAAA").hand_type == HandType.FiveOfAKind
    assert Hand("AA8AA").hand_type == HandType.FourOfAKind
    assert Hand("23332").hand_type == HandType.FullHouse
    assert Hand("TTT98").hand_type == HandType.ThreeOfAKind
    assert Hand("23432").hand_type == HandType.TwoPair
    assert Hand("A23A4").hand_type == HandType.OnePair
    assert Hand("23456").hand_type == HandType.HighCard

    assert HandType.FiveOfAKind > HandType.TwoPair


def test_hand_sorting(caplog):
    caplog.set_level(logging.INFO)

    assert Hand("AAAAA") > Hand("AA8AA")
    assert Hand("KK677") > Hand("KTJJT")
    assert Hand("QQQJA") > Hand("T55J5")


def test_sample_input(caplog):
    caplog.set_level(logging.INFO)

    assert part_one(sample_input) == 6440
    # assert part_two(sample_input) == None


def test_big_input(caplog):
    caplog.set_level(logging.INFO)
    with open(os.path.join(local_path, "input"), "r") as f:
        content = f.read()

        assert part_one(content) == 250474325
        # assert part_two(content) == None

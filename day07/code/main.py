import functools
import logging
from collections import Counter
from enum import IntEnum

logger = logging.getLogger(__name__)


class HandType(IntEnum):
    FiveOfAKind = 7
    FourOfAKind = 6
    FullHouse = 5
    ThreeOfAKind = 4
    TwoPair = 3
    OnePair = 2
    HighCard = 1


@functools.total_ordering
class Hand:

    def __init__(self, definition, bid=None, use_jokers=False):
        self.definition = definition
        self.bid = bid
        self.use_jokers = use_jokers

        mc = Counter(definition).most_common()

        if mc[0][1] == 5:
            self.hand_type = HandType.FiveOfAKind

        elif mc[0][1] == 4:
            self.hand_type = HandType.FourOfAKind

            if use_jokers and 'J' in definition:
                self.hand_type = HandType.FiveOfAKind


        elif mc[0][1] == 3:
            if mc[1][1] == 2:
                self.hand_type = HandType.FullHouse

                if use_jokers and 'J' in definition:
                    self.hand_type = HandType.FiveOfAKind
            else:
                self.hand_type = HandType.ThreeOfAKind

                if use_jokers and 'J' in definition:
                    self.hand_type = HandType.FourOfAKind

        elif mc[0][1] == 2 and mc[1][1] == 2:
            self.hand_type = HandType.TwoPair

            if use_jokers:
                if mc[0][0] == 'J' or mc[1][0] == 'J':
                    self.hand_type = HandType.FourOfAKind

                elif mc[2][0] == 'J':
                    self.hand_type = HandType.FullHouse

        elif mc[0][1] == 2:
            self.hand_type = HandType.OnePair

            if use_jokers and 'J' in self.definition:
                self.hand_type = HandType.ThreeOfAKind

        else:
            self.hand_type = HandType.HighCard

            if use_jokers and 'J' in self.definition:
                self.hand_type = HandType.OnePair

    def __lt__(self, other):
        if self.hand_type != other.hand_type:
            return self.hand_type < other.hand_type

        for card_a, card_b in zip(self.definition, other.definition):
            cmp = self.compare_cards(card_a, card_b)
            if cmp == 0:
                continue

            return True if cmp == 1 else False

    def __repr__(self):
        return f"Hand: {self.definition} ({self.hand_type} - bid: {self.bid})"

    def compare_cards(self, card_a, card_b):
        card_types = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

        if self.use_jokers:
            card_types = ['J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A']

        if card_types.index(card_a) < card_types.index(card_b):
            return 1
        elif card_types.index(card_a) > card_types.index(card_b):
            return -1
        else:
            return 0


def part_one(inp, use_jokers=False):
    hands = []
    for line in inp.splitlines():
        hand_def, hand_bid = line.split()
        hands.append(Hand(hand_def, int(hand_bid), use_jokers=use_jokers))

    sorted_hands = list(sorted(hands))
    value_sum = sum(hand.bid * (i + 1) for i, hand in enumerate(sorted_hands))

    return value_sum


def part_two(inp):
    return part_one(inp, use_jokers=True)

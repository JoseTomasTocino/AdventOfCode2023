import logging

logger = logging.getLogger(__name__)


class Scratchcard:

    def __init__(self, definition: str):
        card_id, card_content = definition.split(":")
        self.number = int(card_id.split()[1])

        winning_numbers, my_numbers = card_content.split("|")
        self.winning_numbers = set(int(x) for x in winning_numbers.strip().split())
        self.my_numbers = set(int(x) for x in my_numbers.strip().split())
        self.matches = self.winning_numbers & self.my_numbers
        self.match_count = len(self.matches)

        logger.info(f"Created card number {self.number}, with {self.match_count} matches")


def part_one(inp):
    total_points = 0

    for line in inp.splitlines():
        current_card = Scratchcard(line)

        if current_card.match_count:
            total_points += 2 ** (current_card.match_count - 1)

    return total_points


def part_two(inp):
    card_definitions = {}

    # Build instances of Scratchcard
    for line in inp.splitlines():
        current_card = Scratchcard(line)
        card_definitions[current_card.number] = current_card

    card_derivations = {}

    # Process card definitions in reverse order
    for number in reversed(card_definitions):
        current_card = card_definitions[number]
        this_derivation = current_card.match_count

        for i in range(number + 1, number + current_card.match_count + 1):
            this_derivation += card_derivations[i]

        card_derivations[number] = this_derivation
        logger.info(f"Processing derivation for card {number}, with {this_derivation}")

    # Remember to add the number of initial cards
    return sum(card_derivations.values()) + len(card_definitions)

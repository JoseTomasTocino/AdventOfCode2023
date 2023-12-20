import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    total_points = 0

    for line in inp.splitlines():
        card_id, card_content = line.split(":")
        winning_numbers, my_numbers = card_content.split("|")
        winning_numbers = set(int(x) for x in winning_numbers.strip().split())
        my_numbers = set(int(x) for x in my_numbers.strip().split())

        matches = winning_numbers & my_numbers
        if matches:
            total_points += 2 ** (len(matches) - 1)

    return total_points


def part_two(inp):
    pass

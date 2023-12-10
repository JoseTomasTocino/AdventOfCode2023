import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    total = 0
    for line in inp.splitlines():
        # Filter non decimal characters
        line = [int(x) for x in line if x.isdecimal()]
        logger.debug(line)
        if not line:
            continue

        total += int(f"{line[0]}{line[-1]}")

    return total


def part_two_alt(inp):
    # Alternative implementation of part two using str.index and str.rindex
    # to enumerate all the number appearances

    replacements = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    tokens = list(replacements.keys()) + list(replacements.values())
    logger.debug(f"List of tokens: {tokens}")

    total = 0

    for line in inp.splitlines():
        logger.debug(f"Processing line: {line}")

        left_digit = None
        right_digit = None

        # From the left
        tind = [(line.index(tok), tok) for tok in tokens if tok in line]
        tind = list(sorted(tind, key=lambda x: x[0]))

        left_digit = tind[0][1]
        left_digit = replacements.get(left_digit, left_digit)

        # From the right
        tind = [(line.rindex(tok), tok) for tok in tokens if tok in line]
        tind = list(sorted(tind, key=lambda x: x[0], reverse=True))

        right_digit = tind[0][1]
        right_digit = replacements.get(right_digit, right_digit)

        logger.debug(f"Processed as: {left_digit} {right_digit}")

        total += int(left_digit + right_digit)

    return total


def part_two(inp: str):
    replacements = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
    }

    total = 0

    for line in inp.splitlines():
        logger.debug(f"Processing line: {line}")

        left_digit = None
        right_digit = None
        stack = ""

        # Left to right sweep
        for c in line:
            # If it's a digit, store it and call it a day
            if c.isdecimal():
                left_digit = c
                break

            # Otherwise add it to the temporary stack and check if it matches a replacement
            stack += c

            for k in replacements:
                if k in stack:
                    left_digit = str(replacements[k])
                    break

            if left_digit is not None:
                break

        stack = ""
        # Right to left sweep
        for c in line[::-1]:
            # If it's a digit, store it and call it a day
            if c.isdecimal():
                right_digit = c
                break

            # Otherwise add it to the temporary stack and check if it matches a replacement
            stack += c
            logger.debug(f"Current stack: {stack}")
            for k in replacements:
                if k in stack[::-1]:
                    right_digit = str(replacements[k])
                    break

            if right_digit is not None:
                break

        logger.debug(f"Processed as {left_digit} {right_digit}")
        total += int(left_digit + right_digit)

    return total

import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    final_sum = 0

    for sequence in inp.splitlines():
        sequence = [int(x) for x in sequence.split()]

        rows = [sequence]

        while True:
            sequence = [sequence[i+1] - sequence[i] for i in range(len(sequence) - 1)]
            rows.append(sequence)

            if all(x == 0 for x in sequence):
                break

        for i in range(len(rows) - 1, 0, -1):
            rows[i-1].append(rows[i-1][-1] + rows[i][-1])

        final_sum+= rows[0][-1]

    return final_sum

def part_two(inp):
    pass

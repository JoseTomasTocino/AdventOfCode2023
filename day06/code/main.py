import logging

logger = logging.getLogger(__name__)


def part_one(inp):
    inp = inp.splitlines()
    times = [int(x) for x in inp[0].split(":")[1].split()]
    distances = [int(x) for x in inp[1].split(":")[1].split()]

    ways = 1
    for t, d in zip(times, distances):
        logger.info(f"Considering race with time = {t}, distance = {d}")

        local_ways = 0

        for sub_t in range(t + 1):
            sub_d = sub_t * (t - sub_t)
            logger.info(f"\tConsidering holding the button for {sub_t} ms: it would travel {sub_d} mm")

            if sub_d > d:
                local_ways += 1

        logger.info(f"\tLocal ways: {local_ways}")

        ways *= local_ways

    return ways


def part_two(inp):
    pass

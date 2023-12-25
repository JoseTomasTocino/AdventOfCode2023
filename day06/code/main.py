import logging
from math import sqrt, ceil, floor

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


def part_two(inp:str):
    inp = inp.splitlines()
    t = int(inp[0].split(":")[1].replace(" ", ""))
    d = int(inp[1].split(":")[1].replace(" ", ""))

    # (t - x) * x > d
    # tx - x² > d
    # tx -x² -d > 0
    # x² - tx + d < 0
    # --
    # Para resolver, aplicamos la fórmula de la ecuación de segundo grado
    # x = (t +- sqrt(t² -4d) / 2
    # --
    # Según el valor del argumento de la raíz, habrá o no solución real

    if t*t - 4 * d < 0:
        return 0

    sol_a = (t + sqrt(t * t - 4 * d)) / 2
    sol_b = (t - sqrt(t * t - 4 * d)) / 2

    sol_a, sol_b = ceil(min(sol_a, sol_b)), floor(max(sol_a, sol_b))

    logger.info(f"Sol A: {sol_a}")
    logger.info(f"Sol B: {sol_b}")

    return sol_b - sol_a + 1








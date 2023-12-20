import logging

logger = logging.getLogger(__name__)


class RangeMap:
    def __init__(self, name=""):
        self.ranges = []
        self.name = name

    def add_range(self, dest_start, source_start, range_length):
        self.ranges.append((dest_start, source_start, range_length))

    def __getitem__(self, item):
        for dest_start, source_start, range_length in self.ranges:
            if item >= source_start and item <= source_start + range_length:
                return dest_start + (item - source_start)

        return item


def part_one(inp: str):
    inp = inp.splitlines()

    seeds = [int(x) for x in inp.pop(0).split(": ")[1].split()]

    # skip empty line
    inp.pop(0)

    maps = []

    while inp:
        line = inp.pop(0)
        map_name = line.split(" ")[0]

        the_map = RangeMap(map_name)
        maps.append(the_map)

        while inp and (line := inp.pop(0)):
            the_map.add_range(*[int(x) for x in line.split()])

        logger.info(f"Built {map_name} map")

    locations = []
    for seed in seeds:
        for map in maps:
            seed = map[seed]

        locations.append(seed)

    return min(locations)


def part_two(inp):
    pass

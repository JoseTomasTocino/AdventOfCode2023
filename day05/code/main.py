import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class MappingRange:
    start: int
    end: int
    delta: int

    rstart: int = field(init=False)
    rend: int = field(init=False)

    def contains(self, element):
        return self.start <= element <= self.end

    def __post_init__(self):
        self.rstart = self.start + self.delta
        self.rend = self.end + self.delta


class Mapping:
    def __init__(self, name=""):
        self.ranges: list[MappingRange] = []
        self.reversed_ranges: list[MappingRange] = []
        self.name = name

    def add_range(self, dest_start, source_start, range_length):
        self.ranges.append(
            MappingRange(start=source_start, end=source_start + range_length - 1, delta=dest_start - source_start))

    def __getitem__(self, item):
        for r in self.ranges:
            if r.contains(item):
                return item + r.delta

        return item

    def sort_ranges(self):
        self.ranges = list(sorted(self.ranges, key=lambda x: x.start))
        self.reversed_ranges = list(sorted(self.ranges, key=lambda x: x.rstart))


def part_one(inp: str, seeds_as_ranges: bool = False):
    inp = inp.splitlines()

    seeds = [int(x) for x in inp.pop(0).split(": ")[1].split()]

    # skip empty line
    inp.pop(0)

    maps = []

    # Build the mappings with their ranges
    while inp:
        line = inp.pop(0)
        map_name = line.split(" ")[0]

        the_map = Mapping(map_name)
        maps.append(the_map)

        while inp and (line := inp.pop(0)):
            the_map.add_range(*[int(x) for x in line.split()])

        the_map.sort_ranges()

        logger.info(f"Read mapping: {the_map.name}")
        for r in the_map.ranges:
            logger.info(f"\t- {r.start} to {r.end} (delta = {r.delta})")
        # for i in range(len(the_map.ranges) - 1):
        #     logger.info(the_map.ranges[i].end - the_map.ranges[i+1].start)

    if seeds_as_ranges:
        candidate_seeds = []

        # Sort input seed ranges
        input_ranges = [(x, x + y - 1) for x, y in sorted(zip(seeds[::2], seeds[1::2]), key=lambda x: x[0])]

        for the_map in maps:
            logger.info(f"Processing map: {the_map.name}")

            new_input_ranges = []

            for first_seed, last_seed in input_ranges:
                logger.info(f"\tInput seed range: from {first_seed} to {last_seed}")

                # First check the seeds with values below any range in the mapping
                if first_seed < the_map.ranges[0].start:
                    logger.info(f"\t\tInput seed range starts below the first range: {first_seed}")
                    candidate_seeds.append(first_seed)

                    # If this seed range ends before reaching any of the mapping ranges, jump to the next input seed range
                    if last_seed < the_map.ranges[0].start:
                        logger.info(f"\t\tInput seed range ends below the first range: {last_seed}")
                        new_input_ranges.append((first_seed, last_seed))
                        continue

                    else:
                        new_input_ranges.append((first_seed, the_map.ranges[0].start - 1))
                        first_seed = the_map.ranges[0].start

                    logger.info(f"\t\tAdded new splitted range (before mapping): {new_input_ranges[-1]}")

                # At this point we're sure this input range enters, at least, in to any of the ranges of the mapping!
                for the_range in the_map.ranges:
                    logger.info(f"\t\tComparing input seed range ({first_seed}, {last_seed}) against mapping range from {the_range.start} to {the_range.end} (delta = {the_range.delta})")

                    if the_range.start <= first_seed <= the_range.end:
                        if last_seed <= the_range.end:
                            new_input_ranges.append((the_map[first_seed], the_map[last_seed]))
                            logger.info(f"\t\tAdded new splitted range: ({first_seed}, {last_seed}), processed = {new_input_ranges[-1]}")
                            break

                        else:
                            new_input_ranges.append((the_map[first_seed], the_map[the_range.end]))
                            logger.info(f"\t\tAdded new splitted range: ({first_seed}, {the_range.end}), processed = {new_input_ranges[-1]}")
                            first_seed = the_range.end + 1

                # Finally, check for seeds that overflow past the ranges in the mapping
                if first_seed > the_map.ranges[-1].end:
                    new_input_ranges.append((first_seed, last_seed))
                    logger.info(f"\t\tAdded new splitted range (after mapping, non-processed): {new_input_ranges[-1]}")

            logger.info(f"New input ranges: {new_input_ranges}")
            input_ranges = sorted(new_input_ranges, key=lambda x: x[0])

        logger.info(f"\tFinal input ranges: {input_ranges}")

        seeds = set(x[0] for x in input_ranges)

    locations = []

    # Map each seed through the chain of maps, saving all the locations and getting the min
    for seed in seeds:
        for map in maps:
            seed = map[seed]

        locations.append(seed)

    return min(locations)


def part_two(inp):
    return part_one(inp, True)

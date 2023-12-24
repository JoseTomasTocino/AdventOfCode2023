import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class Range:
    start: int
    end: int

    def contains(self, element):
        return self.start <= element <= self.end

    def __str__(self):
        return f"({self.start:_}, {self.end:_})"

    def cut(self, other):
        cuts = []

        if other.start < self.start:
            cuts.append(Range(other.start, min(other.end, self.start - 1)))

            if other.end >= self.start:
                cuts.append(Range(self.start, min(other.end, self.end)))

        if other.end > self.end:
            cuts.append(Range(max(self.end + 1, other.start), other.end))

        if not cuts:
            cuts = [other]

        return cuts


@dataclass
class MappingRange(Range):
    delta: int

    def __str__(self):
        return f"({self.start:_}, {self.end:_}) (delta = {self.delta})"


class Mapping:
    def __init__(self, name=""):
        self.ranges: list[MappingRange] = []
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
        for i in range(len(the_map.ranges) - 1):
            logger.info(the_map.ranges[i].end - the_map.ranges[i + 1].start)

    if seeds_as_ranges:
        # Sort input seed ranges
        initial_input_ranges = [Range(x, x + y - 1) for x, y in sorted(zip(seeds[::2], seeds[1::2]), key=lambda x: x[0])]
        final_ranges = []

        for seed in initial_input_ranges:
            logger.info(f"Input seed range: {seed} ")

            input_ranges = [(seed_start, seed_end)]
            processed_input_ranges = []

            for the_map in maps:
                logger.info(f"Processing map: {the_map.name}")

                for the_range in the_map.ranges:
                    logger.info(f"\tProcessing range: {the_range}")

                    unprocessed_input_ranges = []

                    if not input_ranges:
                        logger.info("\t\tNo input ranges left")

                    while input_ranges:
                        logger.info(f"\t\t{processed_input_ranges=}")
                        logger.info(f"\t\t{input_ranges=}")

                        seed_start, seed_end = input_ranges.pop()

                        if seed_start < the_range.start:
                            if seed_end < the_range.start:
                                logger.info("\t\tInput range completely below mapping range")
                                unprocessed_input_ranges.append((seed_start, seed_end))

                            else:
                                logger.info("\t\tInput range partially below mapping range - splitting")
                                unprocessed_input_ranges.append((seed_start, the_range.start - 1))

                                seed_start = the_range.start

                        if the_range.start <= seed_start <= the_range.end:
                            if seed_end < the_range.end:
                                logger.info("\t\tInput range completely within mapping range")
                                processed_input_ranges.append((the_map[seed_start], the_map[seed_end]))

                            else:
                                logger.info("\t\tInput range partially within mapping range and beyond - splitting")
                                processed_input_ranges.append((the_map[seed_start], the_map[the_range.end]))

                                seed_start = the_range.end + 1

                        if the_range.end < seed_start:
                            logger.info("\t\tInput range completely above mapping range")
                            unprocessed_input_ranges.append((seed_start, seed_end))

                    input_ranges = unprocessed_input_ranges

                    logger.info(f"\tEnded processing mapping range")
                    logger.info("-------------------------------------------------------")

                input_ranges = unprocessed_input_ranges + processed_input_ranges
                processed_input_ranges = []
                unprocessed_input_ranges = []

                logger.info(f"Ended processing mapping")
                logger.info(f"Ranges: {input_ranges}")
                logger.info(f"***************************************************************************")

            logger.info(f"Ended processing initial input range")
            logger.info(f"\t{input_ranges=}")
            final_ranges.extend(input_ranges)
            logger.info("###################################################")

        logger.info(f"\tFinal input ranges: {final_ranges}")

        seeds = set(x[0] for x in final_ranges)

    locations = []

    # Map each seed through the chain of maps, saving all the locations and getting the min
    for seed in seeds:
        for map in maps:
            seed = map[seed]

        locations.append(seed)

    return min(locations)


def part_two(inp):
    return part_one(inp, True)

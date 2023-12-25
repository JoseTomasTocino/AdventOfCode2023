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

    def __repr__(self):
        return f"({self.start:_}, {self.end:_})"

    def collides_with(self, other_range):
        return self.end >= other_range.start and other_range.end >= self.start

    def contained_within(self, other_range):
        return other_range.start <= self.start <= other_range.end and \
            other_range.start <= self.end <= other_range.end

    def split(self, subject):

        if subject.end < self.start or self.end < subject.start:
            return [subject]

        cuts = []

        if subject.start < self.start:
            cuts.append(Range(subject.start, self.start - 1))
            cuts.append(Range(self.start, min(self.end, subject.end)))

        else:
            cuts.append(Range(subject.start, min(self.end, subject.end)))

        if self.end < subject.end:
            cuts.append(Range(self.end + 1, subject.end))

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

    # Postprocess mappings to fill holes
    for the_map in maps:
        for i in range(len(the_map.ranges) - 1):
            if the_map.ranges[i + 1].start - the_map.ranges[i].end > 1:
                the_map.add_range(the_map.ranges[i].end + 1, the_map.ranges[i].end + 1, the_map.ranges[i + 1].start - 1 - the_map.ranges[i].end)
                logger.info(f"Filling hole in map {the_map.name} with range: {(the_map.ranges[i].end + 1, the_map.ranges[i + 1].start - 1)}")
                logger.info(the_map.ranges[i])
                logger.info(the_map.ranges[-1])
                logger.info(the_map.ranges[i+1])

        the_map.sort_ranges()

    for the_map in maps:
        logger.info(f"Reviewing map {the_map.name}")
        for i in range(len(the_map.ranges)):
            if i == 0:
                logger.info(f"\tRange: {the_map.ranges[i]}")
            else:
                logger.info(f"\tRange: {the_map.ranges[i]} - from prev: {the_map.ranges[i].start - the_map.ranges[i-1].end}")

    locations = []

    if seeds_as_ranges:
        # Sort input seed ranges
        initial_input_ranges = [Range(x, x + y - 1) for x, y in zip(seeds[::2], seeds[1::2])]
        final_ranges = []

        for seed_range in initial_input_ranges:
            logger.info(f"Input seed range: {seed_range} ")

            input_ranges = [seed_range]

            processed_input_ranges = []
            unprocessed_input_ranges = []

            for i_map, the_map in enumerate(maps):
                logger.info("-------------------------------------------------------------------")
                logger.info(f"Processing map {i_map + 1}: {the_map.name}")

                logger.info(f"Initial inputs: {input_ranges}")

                for the_range in the_map.ranges:
                    logger.info(f"\tProcessing range: {the_range}")

                    while input_ranges:
                        # logger.info(f"\t\t{processed_input_ranges=}")
                        logger.info(f"\t\t{input_ranges=}")

                        seed_range = input_ranges.pop()
                        cuts = the_range.split(seed_range)

                        logger.info(f"\t\tGenerated cuts: {cuts}")

                        for cut in cuts:
                            if cut.contained_within(the_range):
                                processed_input_ranges.append(Range(the_map[cut.start], the_map[cut.end]))
                                logger.info(f"\t\t\tProcessed cut: {cut} => {processed_input_ranges[-1]}")

                            else:
                                logger.info(f"\t\t\tReinserted cut as is: {cut}")
                                unprocessed_input_ranges.append(cut)

                    input_ranges = unprocessed_input_ranges
                    unprocessed_input_ranges = []

                input_ranges += processed_input_ranges
                processed_input_ranges = []

            input_ranges = list(sorted(input_ranges, key=lambda x: x.start))
            final_ranges.extend(input_ranges)
            logger.info(f"Final ranges for this input range: {input_ranges}")

        logger.info("##############################################################################################################")
        logger.info(f"TOTAL Final input ranges: {final_ranges}")
        logger.info("##############################################################################################################")

        locations = set(x.start for x in final_ranges)

    else:
        # Map each seed through the chain of maps, saving all the locations and getting the min
        for seed in seeds:
            for map in maps:
                seed = map[seed]

            locations.append(seed)

    return min(locations)


def part_two(inp):
    return part_one(inp, True)

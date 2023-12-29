from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class PipeShape(Enum):
    VerticalPipe = 1
    HorizontalPipe = 2
    NorthEastBend = 3
    NorthWestBend = 4
    SouthEastBend = 5
    SouthWestBend = 6
    Ground = 7
    Unknown = 8


@dataclass
class Tile:
    shape: PipeShape
    is_start: bool
    x_coord: int
    y_coord: int

    left: Optional[Tile] = None
    top: Optional[Tile] = None
    right: Optional[Tile] = None
    bottom: Optional[Tile] = None

    def __repr__(self):
        return f"Tile(shape={self.shape.name}, is_start={self.is_start}, x={self.x_coord}, y={self.y_coord})"


def part_one(inp):
    inp = inp.splitlines()
    matrix = defaultdict(
        lambda: defaultdict(lambda: Tile(shape=PipeShape.Ground, is_start=False, x_coord=None, y_coord=None)))

    start_x, start_y = 0, 0

    height = len(inp)
    width = len(inp[0])

    neigh_delta = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    for y, row in enumerate(inp):
        for x, elem in enumerate(row):
            match elem:
                case '|':
                    t = Tile(shape=PipeShape.VerticalPipe, is_start=False, x_coord=x, y_coord=y)
                case '-':
                    t = Tile(shape=PipeShape.HorizontalPipe, is_start=False, x_coord=x, y_coord=y)
                case 'L':
                    t = Tile(shape=PipeShape.NorthEastBend, is_start=False, x_coord=x, y_coord=y)
                case 'J':
                    t = Tile(shape=PipeShape.NorthWestBend, is_start=False, x_coord=x, y_coord=y)
                case '7':
                    t = Tile(shape=PipeShape.SouthWestBend, is_start=False, x_coord=x, y_coord=y)
                case 'F':
                    t = Tile(shape=PipeShape.SouthEastBend, is_start=False, x_coord=x, y_coord=y)
                case '.':
                    t = Tile(shape=PipeShape.Ground, is_start=False, x_coord=x, y_coord=y)
                case 'S':
                    t = Tile(shape=PipeShape.Unknown, is_start=True, x_coord=x, y_coord=y)
                    start_x, start_y = x, y

            matrix[x][y] = t

    # Determine the shape type of starting tile
    start_neighbours = [matrix[start_x + dx][start_y + dy] for dx, dy in neigh_delta]
    start_tile = matrix[start_x][start_y]

    # Left neighbour
    if start_neighbours[0].shape in (PipeShape.NorthEastBend, PipeShape.SouthEastBend, PipeShape.HorizontalPipe):

        # Top neighbour
        if start_neighbours[1].shape in (PipeShape.SouthEastBend, PipeShape.SouthWestBend, PipeShape.VerticalPipe):
            start_tile.shape = PipeShape.NorthWestBend

        # Right neighbour
        elif start_neighbours[2].shape in (PipeShape.SouthWestBend, PipeShape.NorthWestBend, PipeShape.HorizontalPipe):
            start_tile.shape = PipeShape.HorizontalPipe

        # Bottom neighbour
        if start_neighbours[3].shape in (PipeShape.NorthEastBend, PipeShape.NorthWestBend, PipeShape.VerticalPipe):
            start_tile.shape = PipeShape.SouthWestBend

    # Right neighbour
    elif start_neighbours[2].shape in (PipeShape.SouthWestBend, PipeShape.NorthWestBend, PipeShape.HorizontalPipe):

        # Top neighbour
        if start_neighbours[1].shape in (PipeShape.SouthEastBend, PipeShape.SouthWestBend, PipeShape.VerticalPipe):
            start_tile.shape = PipeShape.NorthEastBend

        # Bottom neighbour
        if start_neighbours[3].shape in (PipeShape.NorthEastBend, PipeShape.NorthWestBend, PipeShape.VerticalPipe):
            start_tile.shape = PipeShape.SouthEastBend

    elif start_neighbours[1].shape in (PipeShape.SouthEastBend, PipeShape.SouthWestBend, PipeShape.VerticalPipe) and \
            start_neighbours[3].shape in (PipeShape.NorthEastBend, PipeShape.NorthWestBend, PipeShape.VerticalPipe):
        start_tile.shape = PipeShape.VerticalPipe

    logger.info(f"Start tile shape type determined to be: {start_tile.shape.name}")

    # Connect the tiles together
    for x in range(width):
        for y in range(height):
            t = matrix[x][y]

            nle = matrix[x-1][y]
            nto = matrix[x][y-1]
            nri = matrix[x+1][y]
            nbo = matrix[x][y+1]

            if nle.shape in (PipeShape.NorthEastBend, PipeShape.SouthEastBend, PipeShape.HorizontalPipe):
                t.left = nle

            if nto.shape in (PipeShape.SouthEastBend, PipeShape.SouthWestBend, PipeShape.VerticalPipe):
                t.top = nto

            if nri.shape in (PipeShape.NorthWestBend, PipeShape.SouthWestBend, PipeShape.HorizontalPipe):
                t.right = nri

            if nbo.shape in (PipeShape.NorthWestBend, PipeShape.NorthEastBend, PipeShape.VerticalPipe):
                t.bottom = nbo

    # Navigate the loop counting the steps
    current = start_tile
    prev = None
    steps = 0

    while True:
        logger.info(f"Current tile: {current}")

        if current.left is not None and current.left != prev:
            prev = current
            current = current.left

        elif current.top is not None and current.top != prev:
            prev = current
            current = current.top

        elif current.right is not None and current.right != prev:
            prev = current
            current = current.right

        elif current.bottom is not None and current.bottom != prev:
            prev = current
            current = current.bottom

        steps += 1

        if current == start_tile:
            break

    logger.info(f"Cycle found after {steps} steps")

    return steps / 2



def part_two(inp):
    pass

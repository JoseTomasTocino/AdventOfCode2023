from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Tile:
    is_start: bool
    x_coord: int
    y_coord: int

    con_left: bool = False
    con_top: bool = False
    con_right: bool = False
    con_bottom: bool = False
    con_none: bool = False

    left: Optional[Tile] = None
    top: Optional[Tile] = None
    right: Optional[Tile] = None
    bottom: Optional[Tile] = None

    def __repr__(self):
        return f"Tile(left: {self.con_left}, top: {self.con_top}, right: {self.con_right}, bottom: {self.con_bottom} is_start={self.is_start}, x={self.x_coord}, y={self.y_coord})"


def part_one(inp):
    inp = inp.splitlines()
    matrix = defaultdict(
        lambda: defaultdict(lambda: Tile(con_none=True, is_start=False, x_coord=None, y_coord=None)))

    start_x, start_y = 0, 0

    height = len(inp)
    width = len(inp[0])

    for y, row in enumerate(inp):
        for x, elem in enumerate(row):
            match elem:
                case '|':
                    t = Tile(con_top=True, con_bottom=True, is_start=False, x_coord=x, y_coord=y)
                case '-':
                    t = Tile(con_right=True, con_left=True, is_start=False, x_coord=x, y_coord=y)
                case 'L':
                    t = Tile(con_top=True, con_right=True, is_start=False, x_coord=x, y_coord=y)
                case 'J':
                    t = Tile(con_top=True, con_left=True, is_start=False, x_coord=x, y_coord=y)
                case '7':
                    t = Tile(con_left=True, con_bottom=True, is_start=False, x_coord=x, y_coord=y)
                case 'F':
                    t = Tile(con_right=True, con_bottom=True, is_start=False, x_coord=x, y_coord=y)
                case '.':
                    t = Tile(con_none=True, is_start=False, x_coord=x, y_coord=y)
                case 'S':
                    t = Tile(con_none=True, is_start=True, x_coord=x, y_coord=y)
                    start_x, start_y = x, y

            matrix[x][y] = t

    # Determine the shape type of starting tile
    start_tile = matrix[start_x][start_y]

    neighbour_left = matrix[start_x - 1][start_y]
    neighbour_top = matrix[start_x][start_y - 1]
    neighbour_right = matrix[start_x + 1][start_y]
    neighbour_bottom = matrix[start_x][start_y + 1]

    start_tile.con_left = neighbour_left.con_right
    start_tile.con_right = neighbour_right.con_left
    start_tile.con_top = neighbour_top.con_bottom
    start_tile.con_bottom = neighbour_bottom.con_top

    # Connect the tiles together
    for x in range(width):
        for y in range(height):
            t = matrix[x][y]

            if t.con_left:
                t.left = matrix[x - 1][y]

            if t.con_top:
                t.top = matrix[x][y - 1]

            if t.con_right:
                t.right = matrix[x + 1][y]

            if t.con_bottom:
                t.bottom = matrix[x][y + 1]

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

    return steps // 2


def part_two(inp):
    pass

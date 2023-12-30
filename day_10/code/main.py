from __future__ import annotations

import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


def pmat(inp):
    repl = {
        '.': '.',
        'L': '└',
        'J': '┘',
        'F': '┌',
        '7': '┐',
        '|': '│',
        '-': '─',
        '#': '#',
        ' ': ' '
    }

    logger.info("\n" + '\n'.join(''.join(repl[x] for x in inpline) for inpline in inp))


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

    char: str = '.'
    inside_hor: bool = False
    inside_ver: bool = False

    def __repr__(self):
        return f"Tile(is_start={self.is_start}, x={self.x_coord}, y={self.y_coord})"  # left: {self.con_left}, top: {self.con_top}, right: {self.con_right}, bottom: {self.con_bottom}


def part_one(inp):
    inp = [list(x) for x in inp.splitlines()]

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

            t.char = elem
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

    if start_tile.con_left:
        if start_tile.con_right:
            inp[start_y][start_x] = '-'

        elif start_tile.con_top:
            inp[start_y][start_x] = 'J'

        elif start_tile.con_bottom:
            inp[start_y][start_x] = '7'

    elif start_tile.con_right:
        if start_tile.con_top:
            inp[start_y][start_x] = 'L'

        elif start_tile.con_bottom:
            inp[start_y][start_x] = 'F'

    else:
        inp[start_y][start_x] = '|'

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

    loop_coords = set()

    while True:
        loop_coords.add((current.x_coord, current.y_coord))

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

    sol_part_one = steps // 2

    pmat(inp)

    logger.info("Removing pipes that are not connected to the main loop")
    for x in range(width):
        for y in range(height):
            if (x, y) not in loop_coords:
                inp[y][x] = '.'
                # matrix[x][y] ...

    pmat(inp)

    inside_nodes = 0

    for x in range(width):
        for y in range(height):
            t = inp[y][x]

            if t != '.':
                continue

            pipes_left = ''.join([inp[y][i] for i in range(0, x) if inp[y][i] in ['L', 'J', 'F', '7', '|']])
            pipes_right = ''.join([inp[y][i] for i in range(x, width) if inp[y][i] in ['L', 'J', 'F', '7', '|']])
            pipes_top = ''.join([inp[i][x] for i in range(0, y) if inp[i][x] in ['L', 'J', 'F', '7', '-']])
            pipes_bottom = ''.join([inp[i][x] for i in range(y, height) if inp[i][x] in ['L', 'J', 'F', '7', '-']])

            # In pipes_left and pipes_right a combination of LJ equals to a wall, same with F7, so remove those
            pipes_left = pipes_left.replace('LJ', '').replace('F7', '')
            pipes_right = pipes_right.replace('LJ', '').replace('F7', '')

            # Also L7 equals to wall and FJ too
            pipes_left = pipes_left.replace('L7', '|').replace('FJ', '|')
            pipes_right = pipes_right.replace('L7', '|').replace('FJ', '|')

            # In pipes_top and pìpes_bottom, a combination of FL equals to nothing, same with 7J
            pipes_top = pipes_top.replace('FL', '').replace('7J', '')
            pipes_bottom = pipes_bottom.replace('FL', '').replace('7J', '')

            # Replace FJ and 7L with horizontal wall
            pipes_top = pipes_top.replace('FJ', '-').replace('7L', '-')
            pipes_bottom = pipes_bottom.replace('FJ', '-').replace('7L', '-')

            logger.info(
                f"Tile, '{elem}', at {x}, {y}      left: {pipes_left}, right: {pipes_right}, top: {pipes_top}, bottom: {pipes_bottom}")

            # inplocal = deepcopy(inp)
            # inplocal[y][x] = "#"
            # pmat(inplocal)

            plp = len(pipes_left) % 2
            prp = len(pipes_right) % 2
            ptp = len(pipes_top) % 2
            pbp = len(pipes_bottom) % 2

            if plp or prp or ptp or pbp:
                logger.info(f"\tINSIDE NODE")
                inside_nodes += 1

    sol_part_two = inside_nodes

    return sol_part_one, sol_part_two

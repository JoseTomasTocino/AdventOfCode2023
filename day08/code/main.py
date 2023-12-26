from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Node:
    label: str
    left: Optional[Node]
    right: Optional[Node]


def part_one(inp):
    inp = inp.splitlines()

    instructions = itertools.cycle(inp.pop(0))

    inp.pop(0)
    nodes = {}

    for nodeline in inp:
        label, rest = nodeline.split(" = ")
        nodes[label] = Node(label=label, left=None, right=None)

    for nodeline in inp:
        label, rest = nodeline.split(" = ")
        left, right = rest.strip("()").split(", ")

        nodes[label].left = nodes[left]
        nodes[label].right = nodes[right]

    step_count = 0
    current_node = nodes['AAA']
    for instruction in instructions:
        current_node = current_node.left if instruction == "L" else current_node.right
        step_count += 1
        if current_node.label == 'ZZZ':
            break

    return step_count


def part_two(inp):
    pass

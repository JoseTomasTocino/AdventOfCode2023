from __future__ import annotations

import itertools
import logging
from dataclasses import dataclass
from math import lcm
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Node:
    label: str
    left: Optional[Node]
    right: Optional[Node]


def part_one(inp, ghost_mode=False):
    inp = inp.splitlines()

    instructions = inp.pop(0)

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

    if ghost_mode == False:
        current_node = nodes['AAA']
        for instruction in itertools.cycle(instructions):
            current_node = current_node.left if instruction == "L" else current_node.right
            step_count += 1
            if current_node.label == 'ZZZ':
                break

    else:
        starting_labels = [x for x in nodes.keys() if x.endswith('A')]
        currents = [nodes[x] for x in starting_labels]
        to_calc_lcm = []

        # For every possible starting Node, compute the steps needed to reach a cycle, then find how many ending nodes are visited
        # Seemingly only one...
        for node in currents:
            steps_taken = []
            initial_node = node
            for instruction_index, instruction in itertools.cycle(enumerate(instructions)):
                token = (node.label, instruction_index)
                if token in steps_taken:
                    break
                steps_taken.append(token)
                node = node.left if instruction == 'L' else node.right

            logger.info(f"Starting node: {initial_node.label}, found cycle after {len(steps_taken)} steps")
            steps_taken = [x[0] for x in steps_taken]
            finishing_node_indices = [steps_taken.index(x) for x in steps_taken if x.endswith('Z')]
            logger.info(f"Possible finishing nodes: {finishing_node_indices}")
            to_calc_lcm.append(finishing_node_indices[0])

        return lcm(*to_calc_lcm)

    return step_count


def part_two(inp):
    return part_one(inp, ghost_mode=True)

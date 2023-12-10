from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class Hand:
    red: int = 0
    green: int = 0
    blue: int = 0

    def within_limits(self, r, g, b):
        return self.red <= r and self.green <= g and self.blue <= b


@dataclass
class Game:
    id: int
    hands: list[Hand] = field(default_factory=list)


def parse_games(inp):
    for game in inp.splitlines():
        game_id, game_desc = game.split(":")
        game_id = int("".join([x for x in game_id if x.isdecimal()]))

        game = Game(id=game_id)

        for hand_desc in game_desc.split(";"):
            hand = Hand()

            for hand_elem in hand_desc.split(","):
                count, typ = hand_elem.strip().split(" ")
                setattr(hand, typ, int(count))

            game.hands.append(hand)

        yield game


def part_one(inp):
    limit_red = 12
    limit_green = 13
    limit_blue = 14

    valid_game_ids_sum = 0

    for game in parse_games(inp):
        if all(hand.within_limits(limit_red, limit_green, limit_blue) for hand in game.hands):
            valid_game_ids_sum += game.id

    return valid_game_ids_sum


def part_two(inp: int):
    power_sum = 0

    for game in parse_games(inp):
        min_red = max(h.red for h in game.hands)
        min_green = max(h.green for h in game.hands)
        min_blue = max(h.blue for h in game.hands)

        power = min_red * min_green * min_blue
        power_sum += power

    return power_sum

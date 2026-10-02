import random
from ship import Ship


class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []
        self.shots = set()

    def add_ship(self, name, cells):
        ship = Ship(name, cells)
        self.ships.append(ship)
        return ship

    def place_fleet(self, fleet):
        """fleet: list of (name, length) tuples.
        Randomly places each ship, non-overlapping, inside the board.
        Raises RuntimeError if it can't place after many attempts.
        """
        occupied = set()
        for name, length in fleet:
            cells = self._random_placement(length, occupied)
            if cells is None:
                raise RuntimeError(f"Could not place ship {name}")
            self.add_ship(name, cells)
            occupied |= cells

    def _random_placement(self, length, occupied, max_attempts=200):
        for _ in range(max_attempts):
            horizontal = random.choice([True, False])
            if horizontal:
                # row in [0, SIZE-1], col such that col+length <= SIZE
                r = random.randrange(self.SIZE)
                c = random.randrange(self.SIZE - length + 1)
                cells = {(r, c + i) for i in range(length)}
            else:
                r = random.randrange(self.SIZE - length + 1)
                c = random.randrange(self.SIZE)
                cells = {(r + i, c) for i in range(length)}

            if cells.isdisjoint(occupied):
                return cells
        return None

    def already_shot(self, pos):
        return pos in self.shots

    def fire(self, pos):
        if pos in self.shots:
            return "repeat", None
        self.shots.add(pos)
        for ship in self.ships:
            if ship.hit(pos):
                if ship.is_sunk():
                    return "hit", ship.name
                return "hit", None
        return "miss", None

    def all_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def ships_remaining(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())

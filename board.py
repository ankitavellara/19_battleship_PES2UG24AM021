import random


class Ship:
    def __init__(self, name, cells):
        self.name = name
        self.cells = set(cells)
        self.hits = set()

    def hit(self, pos):
        if pos in self.cells:
            self.hits.add(pos)
            return True
        return False

    def is_sunk(self):
        return self.cells <= self.hits


class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []          # list of Ship
        self.shots = set()       # all cells fired at

    # --- placement ---
    def add_ship(self, name, cells):
        ship = Ship(name, cells)
        self.ships.append(ship)
        return ship

    def place_fleet(self, fleet):
        """fleet: list of (name, length) tuples.
        Randomly places each ship, non-overlapping, inside the board.
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

    # --- firing ---
    def already_shot(self, pos):
        return pos in self.shots

    def fire(self, pos):
        """The ONLY place a shot resolves.
        Returns (result, sunk_ship_name_or_None).
        result in {'hit', 'miss', 'repeat'}.
        Never prints anything.
        """
        if pos in self.shots:
            return "repeat", None
        self.shots.add(pos)
        for ship in self.ships:
            if ship.hit(pos):
                if ship.is_sunk():
                    return "hit", ship.name
                return "hit", None
        return "miss", None

    # --- win conditions ---
    def all_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def ships_remaining(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())

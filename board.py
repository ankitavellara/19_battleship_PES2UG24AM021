from ship import Ship


class Board:
    SIZE = 6

    def __init__(self):
        self.ships = []          # list of Ship
        self.shots = set()       # all cells fired at

    def add_ship(self, name, cells):
        ship = Ship(name, cells)
        self.ships.append(ship)
        return ship

    def already_shot(self, pos):
        return pos in self.shots

    def fire(self, pos):
        """Returns (result, sunk_ship_name_or_None).
        result is 'hit', 'miss', or 'repeat'.
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

    def all_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def ships_remaining(self):
        return sum(1 for ship in self.ships if not ship.is_sunk())

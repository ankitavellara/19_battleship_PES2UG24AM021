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

import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()          # every cell the AI has fired at
        self.candidates = []        # cells to prefer (neighbors of hits)
        self.hits = set()           # cells the AI has hit

    def _in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def _neighbors(self, pos):
        r, c = pos
        return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    def _add_candidates(self, pos):
        """Queue untried orthogonal neighbors of a hit."""
        for n in self._neighbors(pos):
            if self._in_bounds(*n) and n not in self.tried and n not in self.candidates:
                self.candidates.append(n)

    def choose(self):
        # Drop any candidates that were already fired at.
        self.candidates = [c for c in self.candidates if c not in self.tried]

        # Target mode
        while self.candidates:
            pos = self.candidates.pop()
            if pos not in self.tried:
                self.tried.add(pos)
                return pos

        # Hunt mode
        options = [(r, c) for r in range(self.size) for c in range(self.size)
                   if (r, c) not in self.tried]
        if not options:
            return None
        pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def report(self, pos, result):
        """Tell the AI what happened so it can adapt.
        result: 'hit', 'miss', or 'sunk'
        """
        if result in ("hit", "sunk"):
            self.hits.add(pos)
            self._add_candidates(pos)

        if result == "sunk":
            # The whole ship is gone; drop candidates touching any
            # of its cells (approximation: drop candidates adjacent
            # to this hit). Good enough for small boards.
            # A more thorough version would need the ship's cells.
            for n in self._neighbors(pos):
                if n in self.candidates:
                    self.candidates.remove(n)

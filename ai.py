import random


class AI:
    def __init__(self, size=6):
        self.size = size
        self.tried = set()
        self.candidates = []
        self.hits = set()

    def _in_bounds(self, r, c):
        return 0 <= r < self.size and 0 <= c < self.size

    def _neighbors(self, pos):
        r, c = pos
        return [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    def _add_candidates(self, pos):
        for n in self._neighbors(pos):
            if self._in_bounds(*n) and n not in self.tried and n not in self.candidates:
                self.candidates.append(n)

    def choose(self):
        """Pick the next cell to shoot. Pure decision — no feedback.
        Returns a 0-indexed (row, col) or None if no cells remain.
        """
        self.candidates = [c for c in self.candidates if c not in self.tried]
        while self.candidates:
            pos = self.candidates.pop()
            if pos not in self.tried:
                self.tried.add(pos)
                return pos

        options = [(r, c) for r in range(self.size) for c in range(self.size)
                   if (r, c) not in self.tried]
        if not options:
            return None
        pos = random.choice(options)
        self.tried.add(pos)
        return pos

    def report(self, pos, result):
        """Tell the AI how a shot that ALREADY happened resolved.
        result in {'hit', 'miss', 'sunk'}. Must not print or return anything.
        """
        if result in ("hit", "sunk"):
            self.hits.add(pos)
            self._add_candidates(pos)

        if result == "sunk":
            for n in self._neighbors(pos):
                if n in self.candidates:
                    self.candidates.remove(n)

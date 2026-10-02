from board import Board
from ai import AI


FLEET = [
    ("Destroyer", 3),
    ("Submarine", 2),
    ("Patrol",    3),
]


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        self.player.place_fleet(FLEET)
        self.enemy.place_fleet(FLEET)

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enemy ships remaining:", self.enemy.ships_remaining())

    # --- Player turn: exactly one feedback line per actual shot ---
    def player_turn(self):
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                return "quit"
            try:
                r, c = map(int, raw.split(","))
                pos = (r - 1, c - 1)
            except ValueError:
                print("Use row,col (e.g., 2,3).")
                continue

            if not (0 <= pos[0] < Board.SIZE and 0 <= pos[1] < Board.SIZE):
                print("Outside board.")
                continue

            result, sunk = self.enemy.fire(pos)

            if result == "repeat":
                print("Already fired there.")
                continue  # no shot consumed, no hit/miss feedback
            elif result == "hit":
                print(f"HIT! You sank the enemy {sunk}!" if sunk else "HIT!")
            else:
                print("MISS!")

            if self.enemy.all_sunk():
                print("You sank the entire enemy fleet. You win!")
                return "win"
            return "ok"

    # --- AI turn: exactly one feedback line per actual shot ---
    def ai_turn(self):
        ai_pos = self.ai.choose()
        if ai_pos is None:
            print("AI has no moves left. Draw.")
            return "draw"

        print("AI fired at", f"{ai_pos[0] + 1},{ai_pos[1] + 1}")
        result, sunk = self.player.fire(ai_pos)

        if result == "hit":
            print(f"AI sank your {sunk}!" if sunk else "AI scored a hit.")
            self.ai.report(ai_pos, "sunk" if sunk else "hit")
        else:
            print("AI missed.")
            self.ai.report(ai_pos, "miss")

        if self.player.all_sunk():
            print("AI sank your entire fleet. You lose.")
            return "lose"
        return "ok"

    def run(self):
        print("Battleship")
        while True:
            outcome = self.player_turn()
            if outcome == "quit":
                print("Goodbye.")
                return
            if outcome == "win":
                return

            outcome = self.ai_turn()
            if outcome == "draw":
                return
            if outcome == "lose":
                return

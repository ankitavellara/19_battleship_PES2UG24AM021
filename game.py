from board import Board
from ai import AI


class Battleship:
    def __init__(self):
        self.player = Board()
        self.enemy = Board()
        self.ai = AI()
        self._setup()

    def _setup(self):
        # Enemy fleet (player shoots at this)
        self.enemy.add_ship("Destroyer",  {(2, 2), (2, 3), (2, 4)})
        self.enemy.add_ship("Submarine",  {(0, 0), (1, 0)})
        self.enemy.add_ship("Patrol",     {(4, 4), (4, 5), (5, 5)})

        # Player fleet (AI shoots at this)
        self.player.add_ship("Destroyer", {(1, 1), (1, 2), (1, 3)})
        self.player.add_ship("Submarine", {(3, 0), (4, 0)})
        self.player.add_ship("Patrol",    {(5, 2), (5, 3), (5, 4)})

    def show(self):
        print("\nYour shots are coordinates like 2,3.")
        print("Enemy ships remaining:", self.enemy.ships_remaining())

    def run(self):
        print("Battleship")
        while True:
            self.show()
            raw = input("> ").strip().lower()
            if raw == "q":
                print("Goodbye.")
                return
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
                continue
            elif result == "hit":
                if sunk:
                    print(f"HIT! You sank the enemy {sunk}!")
                else:
                    print("HIT!")
            else:
                print("MISS!")

            if self.enemy.all_sunk():
                print("You sank the entire enemy fleet. You win!")
                return

            # --- AI turn ---
            ai_pos = self.ai.choose()
            if ai_pos is None:
                print("AI has no moves left. Draw.")
                return
            print("AI fired at", f"{ai_pos[0] + 1},{ai_pos[1] + 1}")

            ai_result, ai_sunk = self.player.fire(ai_pos)
            if ai_result == "hit":
                if ai_sunk:
                    print(f"AI sank your {ai_sunk}!")
                else:
                    print("AI scored a hit.")
            else:
                print("AI missed.")

            if self.player.all_sunk():
                print("AI sank your entire fleet. You lose.")
                return

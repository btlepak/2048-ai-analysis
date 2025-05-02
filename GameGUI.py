import tkinter as tk
import time
from Grid_3 import Grid
from PlayerAI_3 import PlayerAI
from ComputerAI_3 import ComputerAI

TILE_COLORS = {
    0: ("#cdc1b4", "#776e65"),
    2: ("#eee4da", "#776e65"),
    4: ("#ede0c8", "#776e65"),
    8: ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
    32: ("#f67c5f", "#f9f6f2"),
    64: ("#f65e3b", "#f9f6f2"),
    128: ("#edcf72", "#f9f6f2"),
    256: ("#edcc61", "#f9f6f2"),
    512: ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2")
}

FONT = ("Helvetica", 40, "bold")

class Game2048GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 AI Game")
        self.grid = Grid()
        self.playerAI = PlayerAI()
        self.computerAI = ComputerAI()
        self.tiles = [[None]*4 for _ in range(4)]
        self.setupUI()
        self.startGame()

    def setupUI(self):
        self.frame = tk.Frame(self.master, bg="#bbada0")
        self.frame.grid(sticky="nsew")
        for i in range(4):
            for j in range(4):
                label = tk.Label(self.frame, text="", width=4, height=2, font=FONT, bg="#cdc1b4")
                label.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                self.tiles[i][j] = label

    def updateUI(self):
        for i in range(4):
            for j in range(4):
                value = self.grid.map[i][j]
                bg_color, fg_color = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                self.tiles[i][j].configure(text=str(value) if value != 0 else "", bg=bg_color, fg=fg_color)
        self.master.update_idletasks()

    def startGame(self):
        for _ in range(2):
            self.grid.insertTile(self.computerAI.getMove(self.grid), 2)
        self.updateUI()
        self.master.after(500, self.step)

    def step(self):
        if not self.grid.canMove():
            print("Game Over. Max tile: {}".format(self.grid.getMaxTile()))
            return

        move = self.playerAI.getMove(self.grid.clone())
        if move is not None:
            self.grid.move(move)
            pos = self.computerAI.getMove(self.grid)
            if pos:
                self.grid.insertTile(pos, 2)
        self.updateUI()
        self.master.after(25, self.step)

if __name__ == '__main__':
    root = tk.Tk()
    game = Game2048GUI(root)
    root.mainloop()

import tkinter as tk
import tkinter.font as tkFont
import time
import os
import csv
import random
from datetime import datetime
from Grid_3 import Grid
from PlayerAI_3 import PlayerAI
from ComputerAI_3 import ComputerAI

class GameTrackerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Simulation Tracker")
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.base_font = tkFont.Font(family="Helvetica", size=12)
        self.tile_font = tkFont.Font(family="Helvetica", size=18)

        self.total_games = 0
        self.max_games = 10
        self.completed_games = 0
        self.highest_tile_ever = 0
        self.current_weights = [40, 200, 270, 500]
        self.paused = False
        self.speed = 100
        self.allow_edit_weights = True
        self.in_single_simulation = False
        self.simulation_started = False
        self.game_start_time = None
        self.MIN_SPEED = 1
        self.MAX_SPEED = 2000

        self.log_file = None
        self.csv_writer = None

        self.grid = Grid()
        self.playerAI = PlayerAI()
        self.playerAI.weights = self.current_weights[:]
        self.computerAI = ComputerAI()

        self.setupUI()
        self.updateWeightInputs()
        self.toggleSimulationControls(active=False)
        self.master.bind("<Configure>", self.on_resize)

    def setupUI(self):
        for i in range(4):
            self.master.rowconfigure(i, weight=1)
            self.master.columnconfigure(i, weight=1)

        self.tile_labels = [[tk.Label(self.master, text='', width=5, height=2,
                                      font=self.tile_font, borderwidth=1, relief="solid")
                             for _ in range(4)] for _ in range(4)]

        for i in range(4):
            for j in range(4):
                self.tile_labels[i][j].grid(row=i, column=j, padx=3, pady=3, sticky="nsew")

        self.info_frame = tk.Frame(self.master)
        self.info_frame.grid(row=0, column=5, rowspan=9, padx=20, sticky="nsew")
        for i in range(20):
            self.info_frame.rowconfigure(i, weight=1)
        self.info_frame.columnconfigure(0, weight=1)

        self.high_tile_label = tk.Label(self.info_frame, text="Current Game High Tile: 0", font=self.base_font)
        self.high_tile_label.grid(row=0, column=0, sticky="ew", pady=5)

        self.best_tile_label = tk.Label(self.info_frame, text="All-Time Highest Tile: 0", font=self.base_font)
        self.best_tile_label.grid(row=1, column=0, sticky="ew", pady=5)

        self.weights_label = tk.Label(self.info_frame, text="Heuristic Weights:", font=self.base_font)
        self.weights_label.grid(row=2, column=0, sticky="ew", pady=5)

        self.weight_entries = []
        for i in range(4):
            entry = tk.Entry(self.info_frame, width=10)
            entry.grid(row=3+i, column=0, pady=2, sticky="ew")
            self.weight_entries.append(entry)

        self.status_frame = tk.Frame(self.info_frame)
        self.status_frame.grid(row=7, column=0, pady=5, sticky="ew")
        self.status_frame.columnconfigure(0, weight=1)
        self.status_frame.columnconfigure(1, weight=1)

        self.status_waiting = tk.Label(self.status_frame, text="● Waiting", fg="gray", font=self.base_font)
        self.status_waiting.grid(row=0, column=0, padx=5, sticky="ew")

        self.status_applied = tk.Label(self.status_frame, text="● Applied", fg="gray", font=self.base_font)
        self.status_applied.grid(row=0, column=1, padx=5, sticky="ew")

        self.change_weights_button = tk.Button(self.info_frame, text="Apply New Heuristics", font=self.base_font,
                                               command=self.applyWeightChanges)
        self.change_weights_button.grid(row=8, column=0, pady=10, sticky="ew")

        self.game_count_label = tk.Label(self.info_frame, text="Games Completed: 0", font=self.base_font)
        self.game_count_label.grid(row=9, column=0, pady=5, sticky="ew")

        self.speed_control_frame = tk.Frame(self.info_frame)
        self.speed_control_frame.grid(row=10, column=0, pady=5, sticky="ew")
        self.speed_control_frame.columnconfigure(1, weight=1)

        self.decrease_button = tk.Button(self.speed_control_frame, text="-", font=self.base_font, command=self.decreaseSpeed, width=2)
        self.decrease_button.grid(row=0, column=0, padx=2)

        self.speed_slider = tk.Scale(self.speed_control_frame, from_=self.MIN_SPEED, to=self.MAX_SPEED,
                                     label="Speed (ms per move)", orient=tk.HORIZONTAL, command=self.adjustSpeed)
        self.speed_slider.set(self.speed)
        self.speed_slider.grid(row=0, column=1, sticky="ew")

        self.increase_button = tk.Button(self.speed_control_frame, text="+", font=self.base_font, command=self.increaseSpeed, width=2)
        self.increase_button.grid(row=0, column=2, padx=2)

        tk.Label(self.info_frame, text="Total Games to Run:", font=self.base_font).grid(row=11, column=0, sticky="ew")
        self.max_games_entry = tk.Entry(self.info_frame)
        self.max_games_entry.insert(0, str(self.max_games))
        self.max_games_entry.grid(row=12, column=0, pady=5, sticky="ew")

        self.pause_button = tk.Button(self.info_frame, text="Pause", font=self.base_font, command=self.togglePause)
        self.pause_button.grid(row=13, column=0, pady=10, sticky="ew")

        self.start_button = tk.Button(self.info_frame, text="Start Full Simulation", font=self.base_font, command=self.startFullSimulation)
        self.start_button.grid(row=14, column=0, pady=10, sticky="ew")

        self.single_sim_button = tk.Button(self.info_frame, text="Start Single Simulation", font=self.base_font, command=self.startSingleSimulation)
        self.single_sim_button.grid(row=15, column=0, pady=10, sticky="ew")

    def on_resize(self, event):
        new_base = max(10, event.width // 60)
        self.base_font.configure(size=new_base)
        self.tile_font.configure(size=new_base + 6)

    def adjustSpeed(self, val):
        val = int(val)
        if val <= self.MIN_SPEED:
            self.speed_slider.config(label="Speed (MIN)")
        elif val >= self.MAX_SPEED:
            self.speed_slider.config(label="Speed (MAX)")
        else:
            self.speed_slider.config(label="Speed (ms per move)")
        self.speed = val

    def increaseSpeed(self):
        val = self.speed_slider.get()
        if val < self.MAX_SPEED:
            self.speed_slider.set(val + 10)

    def decreaseSpeed(self):
        val = self.speed_slider.get()
        if val > self.MIN_SPEED:
            self.speed_slider.set(val - 10)

    def togglePause(self):
        if not self.simulation_started:
            return
        self.paused = not self.paused
        self.pause_button.config(text="Resume" if self.paused else "Pause")
        if not self.paused:
            self.step()

    def applyWeightChanges(self):
        try:
            new_weights = [int(entry.get()) for entry in self.weight_entries]
            self.current_weights = new_weights[:]
            if self.simulation_started:
                self.allow_edit_weights = True
                self.status_waiting.config(fg="gold")
                self.status_applied.config(fg="gray")
            else:
                self.status_waiting.config(fg="gray")
                self.status_applied.config(fg="green")
            self.updateWeightInputs()
        except ValueError:
            pass

    def updateWeightInputs(self):
        for i, entry in enumerate(self.weight_entries):
            entry.delete(0, tk.END)
            entry.insert(0, str(self.current_weights[i]))

    def initLogFile(self, directory):
        os.makedirs(directory, exist_ok=True)
        date_str = datetime.now().strftime("%Y_%m_%d_%I-%M-%S_%p")
        self.log_file_path = os.path.join(directory, f"results_{date_str}.csv")
        self.log_file = open(self.log_file_path, 'w', newline='')
        self.csv_writer = csv.writer(self.log_file)
        self.csv_writer.writerow(["Game #", "Max Tile", "Weights", "Time (s)"])

    def startFullSimulation(self):
        try:
            self.max_games = int(self.max_games_entry.get())
        except ValueError:
            self.max_games = 10
        self.total_games = 0
        self.completed_games = 0
        self.game_count_label.config(text="Games Completed: 0")
        self.highest_tile_ever = 0
        self.best_tile_label.config(text="All-Time Highest Tile: 0")
        self.in_single_simulation = False
        self.simulation_started = True
        self.toggleSimulationControls(active=True)
        self.status_waiting.config(fg="gray")
        self.status_applied.config(fg="gray")
        self.initLogFile(os.path.join(os.getcwd(), "FullSimulationResults"))
        self.newGame(use_current_weights=True)

    def startSingleSimulation(self):
        self.max_games = 1
        self.total_games = 0
        self.completed_games = 0
        self.game_count_label.config(text="Games Completed: 0")
        self.in_single_simulation = True
        self.simulation_started = True
        self.toggleSimulationControls(active=True)
        self.status_waiting.config(fg="gray")
        self.status_applied.config(fg="gray")
        self.initLogFile(os.path.join(os.getcwd(), "SingleSimulationResults"))
        self.newGame(use_current_weights=True)

    def toggleSimulationControls(self, active):
        state = 'normal' if active else 'disabled'
        self.pause_button.config(state=state)
        self.start_button.config(state='disabled' if active else 'normal')
        self.single_sim_button.config(state='disabled' if active else 'normal')
        self.max_games_entry.config(state='disabled' if active else 'normal')

    def updateUI(self):
        max_tile = 0
        for i in range(4):
            for j in range(4):
                value = self.grid.map[i][j]
                self.tile_labels[i][j].config(text=str(value) if value else '')
                max_tile = max(max_tile, value)

        self.high_tile_label.config(text=f"Current Game High Tile: {max_tile}")

        if max_tile > self.highest_tile_ever:
            self.highest_tile_ever = max_tile
            self.best_tile_label.config(text=f"All-Time Highest Tile: {self.highest_tile_ever}")

        self.weights_label.config(text=f"Heuristic Weights: {self.playerAI.weights}")
        return max_tile

    def newGame(self, use_current_weights=False):
        if self.total_games >= self.max_games:
            if self.log_file:
                self.log_file.close()
            self.toggleSimulationControls(active=False)
            self.simulation_started = False
            return

        if self.allow_edit_weights:
            self.playerAI = PlayerAI()
            self.playerAI.weights = self.current_weights[:]
            self.allow_edit_weights = False
            self.status_waiting.config(fg="gray")
            self.status_applied.config(fg="green")
        else:
            self.playerAI = PlayerAI()
            if use_current_weights or self.in_single_simulation:
                self.playerAI.weights = self.current_weights[:]
            else:
                self.playerAI.weights = [random.randint(0, 500) for _ in range(4)]

        self.grid = Grid()
        self.grid.insertTile(self.computerAI.getMove(self.grid), 2)
        self.grid.insertTile(self.computerAI.getMove(self.grid), 2)

        self.total_games += 1
        self.updateWeightInputs()
        self.updateUI()
        self.game_start_time = time.time()
        self.step()

    def step(self):
        if self.paused:
            return

        if not self.grid.canMove():
            max_tile = self.updateUI()
            elapsed = round(time.time() - self.game_start_time, 3) if self.game_start_time else 0
            if self.csv_writer:
                self.completed_games += 1
                self.csv_writer.writerow([self.completed_games, max_tile, self.playerAI.weights, elapsed])
                self.game_count_label.config(text=f"Games Completed: {self.completed_games}")
            self.master.after(1000, lambda: self.newGame(use_current_weights=False))
            return

        move = self.playerAI.getMove(self.grid.clone())
        if move is not None:
            self.grid.move(move)
            pos = self.computerAI.getMove(self.grid)
            if pos:
                self.grid.insertTile(pos, 2)
        self.updateUI()
        self.master.after(self.speed, self.step)

if __name__ == '__main__':
    root = tk.Tk()
    tracker = GameTrackerGUI(root)
    root.mainloop()

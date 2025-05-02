import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
from PlayerAI_3 import PlayerAI
from GameManager_3 import GameManager
from Displayer_3 import Displayer
from ComputerAI_3 import ComputerAI

class SilentDisplayer:
    def display(self, grid):
        pass

def run_simulation(weight_sets, num_games=10, log_file="results.csv"):
    results = []

    with open(log_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["w1", "w2", "w3", "w4", "game", "max_tile", "duration_sec"])

        for weights in weight_sets:
            print(f"Testing weights: {weights}")
            for i in range(num_games):
                playerAI = PlayerAI()
                playerAI.weights = list(weights)
                gm = GameManager(4, playerAI, ComputerAI(), SilentDisplayer())
                start_time = time.time()
                max_tile = gm.start()
                end_time = time.time()
                duration = round(end_time - start_time, 3)
                writer.writerow([*weights, i + 1, max_tile, duration])
                results.append((*weights, i + 1, max_tile, duration))

    return results


def plot_results(log_file="results.csv"):
    df = pd.read_csv(log_file)
    df["weight_combo"] = df[["w1", "w2", "w3", "w4"]].astype(str).agg("-".join, axis=1)
    grouped = df.groupby("weight_combo")["max_tile"].mean().sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    grouped.plot(kind='bar', color='skyblue')
    plt.title("Average Max Tile by Heuristic Weight Combination")
    plt.ylabel("Average Max Tile")
    plt.xlabel("Weight Combination (w1-w2-w3-w4)")
    plt.tight_layout()
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis='y')
    plt.show()

if __name__ == '__main__':
    from itertools import product

    # Define a small sample grid of weights for quick testing
    weight_sets = list(product([100, 200], [200, 300], [200, 300], [400, 500]))

    # Run simulations and log results
    run_simulation(weight_sets, num_games=5, log_file="results.csv")

    # Plot results
    plot_results("results.csv")

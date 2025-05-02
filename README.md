# 🎮 2048 Puzzle AI Player
## Introduction
The 2048 Puzzle AI Player is an intelligent agent designed to play the 2048 puzzle efficiently, utilizing advanced AI techniques like Expectiminimax and heuristics to achieve high scores. This ReadMe provides an overview of the project, including its purpose, algorithmic approach, and usage instructions

![](https://i.imgur.com/InwVwFK.png)

![](https://i.imgur.com/FxkLPRi.png)


## 🧠 Algorithmic                 
### Minimax Algorithm
The AI player employs the minimax algorithm, which is used in adversarial search scenarios to minimize potential losses assuming optimal opponent behavior.

```python
def getMove(self, grid):
    best_value = maxsize * -1
    for move in grid.getAvailableMoves():
        temp_grid = grid.clone()
        temp_grid.move(move)
        value = self.min(Node(move=move, grid=temp_grid, depth=DEPTH-1))
        if value > best_value:
            best_move = move
```


### Alpha-Beta Pruning
To improve the efficiency of the minimax algorithm, the AI player utilizes alpha-beta pruning. Alpha-beta pruning reduces the number of nodes evaluated in the search tree by eliminating branches that are guaranteed to be irrelevant to the final decision.

```python
def min(self, node, alpha, beta):
    for child in children:
        value = self.max(child, alpha, beta)
        if value < beta:
            beta = value
        if alpha >= beta:
            break
    return beta
```

### Heuristic Functions
Custom heuristics guide the AI by evaluating the desirability of game states. This includes factors like:

- The number of empty cells.
- Monotonicity of the tile arrangement.
- Whether the highest tile is in a corner

```python
def evaluate(grid):
    number_of_blank_tiles = len(grid.getAvailableCells())
    max_tile = grid.getMaxTile()
    bonus = 10 if max_tile in [grid.map[0][0], grid.map[0][3]] else 0
    return number_of_blank_tiles + bonus
```

## 🚀 Instrutions
Run the game

```python
python GameManager.py
```
## 📂 Files Overview

- PlayerAI_3.py: Implements AI logic with Expectiminimax and heuristics.
- ComputerAI_3.py: Controls computer moves by inserting tiles randomly.
- Grid_3.py: Handles all operations related to the game board (e.g., tile movement, merging).
- Displayer_3.py: Manages grid display.
- GameManager_3.py: Manages game flow, alternating between AI and computer turns.

## 📊 Code Overview
The AI explores all possible game moves using the Expectiminimax algorithm. Each state is evaluated using a weighted function to prioritize empty tiles, grid monotonicity, and corner positions for high-value tiles.

```python
def evaluate(grid):
    # Return a weighted sum of the heuristic factors
    return len(grid.getAvailableCells()) + monotonicity_score + corner_bonus
```
## Conclusion
The 2048 Puzzle AI Player project showcases the power of algorithms like minimax and alpha-beta pruning in solving game challenges. With the provided structure, you can easily modify and improve the AI for better performance.

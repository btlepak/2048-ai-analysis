# 🧠 2048 AI Agent with Enhanced GUI and Simulation Toolkit

> 🔗 **Base Source**: This project is built upon the base Python AI logic cloned from  
> [https://github.com/gksdusql94/AI_2048](https://github.com/gksdusql94/AI_2048)

---

## 📈 Overview

This project extends the base implementation of a Minimax/Expectiminimax-based AI agent that plays the 2048 game. The AI evaluates possible moves using heuristics and depth-limited search, and the game logic is governed by a grid-based representation of the 2048 board.

Significant features and tooling upgrades have been implemented to support interactive visualization, simulation control, dynamic heuristic configuration, and detailed logging of results for performance analysis.

---

## 🧠 AI: Expectiminimax Agent

The core AI agent uses the **Expectiminimax search algorithm**, a variant of the classic Minimax algorithm used for stochastic games. The agent alternates between:

- **Maximizing Player Moves** – Choosing the best direction (UP/DOWN/LEFT/RIGHT)
- **Minimizing Computer Moves** – Random tile placement of 2 or 4
- **Chance Nodes** – Weighted evaluation of random outcomes (90% chance of 2, 10% of 4)

### 🔧 Heuristics Used

Each game state is evaluated using a weighted sum of:
- Grid smoothness (penalizes tile gaps)
- Tile monotonicity
- Available moves
- Open cells
- Grid value map (prefers higher tiles in corners)

Weights are adjustable in real-time.

---

## 🚀 Features & Enhancements Beyond the Base Project

### 🗁️ Graphical User Interface (GUI)
- Real-time tile updates using `tkinter`
- Interactive grid display for each move
- Color-coded tiles consistent with 2048 style

### 🎛️ Dynamic Simulation Controls
- **Speed Slider**: Adjustable move delay from 1ms to 2000ms
- **Increment/Decrement Buttons**: Fine-tune move speed with “MIN”/“MAX” indicators
- **Pause/Resume**: Toggle simulation at any time
- **Single or Full Simulation Modes**: Run one game or hundreds of them in a batch

### 📊 Heuristic Configuration
- View and **edit AI heuristic weights**
- Apply changes dynamically:
  - Yellow ⚪ `Waiting`: Will be used in next game
  - Green 🟢 `Applied`: Now in use
- Locked during active game to prevent inconsistency

### 📁 Automated Logging
- Every game’s result is saved to a timestamped CSV file
- Logs include:
  - Game number
  - Max tile reached
  - Heuristic weights used
  - Time taken per game
- Logs are saved to:
  - `SingleSimulationResults/` for one-off runs
  - `FullSimulationResults/` for batch runs

### 🧪 Game Count Tracking
- Live counter for games completed in a simulation
- Resets to `0` with each new run

---

## 📂 Project Structure

```
.
├── BaseAI_3.py
├── ComputerAI_3.py
├── FullSimulationResults/
├── Grid_3.py
├── PlayerAI_3.py
├── README.md
├── SingleSimulationResults/
├── simulation_tracker_gui.py
```

---

## 🛠️ Setup & Run

### ✅ Requirements

- Python 3.7+
- `tkinter` (usually included with Python)
- `pandas` and `matplotlib` (optional for further analysis)

### ▶️ To Run the GUI:

```bash
python simulation_tracker_gui.py
```

---

## 🧹 Future Improvements (Ideas)
- Add bar graphs of performance over time
- Save/load weight configurations
- Multiplayer or custom grid sizes
- Integration with ML models (e.g., reinforcement learning)

---

## 🤝 Credits

- Original logic: [https://github.com/gksdusql94/AI_2048](https://github.com/gksdusql94/AI_2048)
- Visualization, control logic, and simulation enhancements by [Your Name]


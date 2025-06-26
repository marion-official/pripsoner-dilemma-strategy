# 🕹️ Prisoner's Dilemma: Repeated Game Engine

## 📜 Game Description

A mysterious banker invites two players to compete in a strategic game of trust and betrayal. In each round, both players must independently choose one of two actions:

- **Cooperate (C)**
- **Defect (D)**

The players cannot communicate. Their choices are made in secret and revealed simultaneously. The game is repeated over several rounds, allowing players to adapt their strategies based on previous outcomes.

The goal: **collect as many coins as possible** by the end of the game.

---

## 💰 Rules & Payoff Table

The outcome of each round depends on both players' decisions:

| Player 1 | Player 2 | Player 1 Coins | Player 2 Coins |
|----------|----------|----------------|----------------|
| Cooperate | Cooperate | 3              | 3              |
| Cooperate | Defect    | 0              | 5              |
| Defect    | Cooperate | 5              | 0              |
| Defect    | Defect    | 1              | 1              |

---

## 🧠 Game Features

- 🎮 **Repeated Rounds**: You decide how many rounds to play.
- 👤 **Flexible Player Types**: Each player can be a:
  - **Human** (manual input)
  - **Algorithm** (predefined strategy, e.g. Tit for Tat, Always Defect)
- 🧮 **Score Tracking**: The banker keeps track of each player’s choices and cumulative scores.
- 🗂️ **History Awareness**: Strategies can react based on the opponent’s past actions.
- 💻 **Console Interface**: Simple CLI interaction for humans, extendable for bots.

---

## 🏆 Tournament Mode

All strategies play against each other in every possible pairing. Each match runs for a set number of rounds (default: 300). Final scores and a leaderboard are printed at the end.

This mode is ideal for observing which strategies perform best in a competitive environment.

---

## 🚀 How to Run

```bash
python3 es.py


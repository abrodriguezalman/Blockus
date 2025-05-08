# CMSC 14200 Course Project - Blockus

## Blokus Game
### Description

Blokus is a strategy board game that challenges players to place their pieces on the board while blocking their opponents. The game can be played in several configurations: Blokus Mono, Blokus Duo, and Blokus Classic (with 2, 3, or 4 players). You can play the game using either a **Graphical User Interface (GUI)** or a **Text User Interface (TUI)**, or even simulate games using **bots**.

This repository provides a complete implementation of the game with the ability to play interactively and programmatically. Below is a guide on how to get the game running and explore its features.

---

## Features

- **Multiple Game Configurations**: Choose between Blokus Mono, Blokus Duo, and Blokus Classic with 2, 3, or 4 players.
- **Piece Selection**: Select which piece to play using keyboard shortcuts.
- **Piece Manipulation**: Flip or rotate pieces during your turn.
- **Bot Simulation**: Simulate a game between different strategies using a bot (Satisfactory, Needs Improvement, Unsatisfactory).
- **Retirement**: Allow players to retire during the game if they wish.
- **Customizable Game Settings**: Adjust the number of players, board size, and start positions.

---

## How to Run the Game

### Prerequisites

- **Python 3**: Ensure Python 3 is installed on your system.
- **Dependencies**: Install the required libraries by running:
  ```bash
  pip install click
  
## Running the Game
You can run the game using either the GUI, TUI, or Bot.

### 1. Using the GUI

To start a game with the GUI, use the following command-line options:

- Blokus Mono (1 player): python3 src/gui.py --game=mono

- Blokus Duo (2 players): python3 src/gui.py --game=duo

- Blokus Classic (3 players): python3 src/gui.py --game=classic-3

- Custom Game Setup (e.g., 2 players on a 14x14 board, start positions at (4,9) and (9,4)):
python3 src/gui.py -n 2 -s 14 -p 4 9 -p 9 4

### 2. Using the TUI

If you prefer the Text User Interface (TUI), you can use the following command:

python3 src/tui.py --game=duo

The command-line options are the same as those for the GUI.

### 3. Playing with the Bot

Simulate a game with bots by using the following parameters:

Play a 2-player game with bot 1 as 'S' strategy (satisfactory) and bot 2 as 'N' strategy (random):

python3 src/bot.py -1 S -2 N -n 100

You can choose different bot strategies:

S (Satisfactory)
N (Needs Improvement)
U (Unsatisfactory)

The -n NUM_GAMES parameter specifies how many games to run (default: 20).

## Command-Line Options
### General Options:

* -n NUM_PLAYERS or --num-players NUM_PLAYERS (default: 2): Specifies the number of players.
* -s BOARD_SIZE or --size BOARD_SIZE (default: 14): Specifies the size of the board.
* -p X Y or --start-position X Y: Defines the starting positions for players. Multiple start positions can be given, for example: -p 4 9 -p 9 4.
* --game=mono: Specifies Blokus Mono configuration.
* --game=duo: Specifies Blokus Duo configuration.
* --game=classic-2, --game=classic-3, --game=classic-4: Specifies Blokus Classic with 2, 3, or 4 players.
  
### Bot Options:

* -1 STRATEGY or --player1 STRATEGY: Strategy for player 1 (Satisfactory, Needs Improvement, or Unsatisfactory). Default: N.
* -2 STRATEGY or --player2 STRATEGY: Strategy for player 2 (Satisfactory, Needs Improvement, or Unsatisfactory). Default: N.
* -n NUM_GAMES or --num-games NUM_GAMES: Specifies the number of games to simulate (default: 20).

## Game Features and Interactions

### Piece Selection:
* Press the corresponding number or letter key to select a piece (e.g., pressing 1 selects the piece "ShapeKind.ONE").

* #### Flips and Rotations:
- r: Rotate right
- e: Rotate left
- space: Flip horizontally

* #### Retirement:
- Press q to retire from the game.

* #### Display:
- Displays the current player, their score, and whether they are retired.

* #### End Game:
- When all players have either retired or placed all their pieces, the game ends and the winner is displayed.

## Notes

You can adjust the board size, player count, and start positions using the command-line parameters.
Players can retire during the game, and the game ends when all players have either retired or placed all their pieces.
To test the bots, you can experiment with the different strategies and simulate various game scenarios.

## Collaborators
- TUI: Abril Rodriguez Almanzar (abrodriguezalman)
- GUI: Avni Gupta (avnig)
- Bot: Aybala Esmer (aybala)
- QA: Sarah Murad (samurad)

## Acknowledgments

This project was completed as part of the University of Chicago curriculum for the CMSC 14200: Introduction to Computer Science II course led by Professor Ravi Chug during Spring 2024.

## License

This project is licensed under the MIT License


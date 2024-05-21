# CMSC 14200 Course Project

Team members:
- TUI: Abril Rodriguez Almanzar (abrodriguezalman)
- GUI: Avni Gupta (avnig)
- Bot: Aybala Esmer (aybala)
- QA: Sarah Murad (samurad)

## Improvements

### Game Logic
This component received two S scores in Milestone 2.

### GUI
This component received an N in Milestone 2 for the rubric item "Enter Key not completed as required." This was a misunderstanding - the grader did not look in the correct method. More details in the linked Ed Thread: https://edstem.org/us/courses/56801/discussion/4972775

### TUI
This component received an N in Milestone 2 for the following rubric items:
"Running python3 src/{g,t}ui.py 20 doesn’t correctly display the board, start positions, and initial randomly selected piece"
"Same as previous but for python3 src/{g,t}ui.py duo"
"Same as previous but for python3 src/{g,t}ui.py mono"

These failures were likely  due to an issue with terminal sizing. This ED Discussion post discusses the error I encountered: https://edstem.org/us/courses/56801/discussion/4931634.
To fix this issue, I utilized the curses function resize_term() to set a default terminal size for all game board configurations. This change was implemented in line 130 of tui.py.

### Bot
This component received two S scores in Milestone 2.

### QA
This component received two S scores in Milestone 2.


## Enhancements
GUI
- Display remaining pieces as shapes rather than letters. Clicking on a piece in the piece bank will select it and display it on the board.
- Added support for hints with `available_moves()`. Pressing "h" on the keyboard will randomly pick a piece to play and display it on the board. If there are no available moves, pressing "h" prints "No available moves for player {n}" to the terminal.

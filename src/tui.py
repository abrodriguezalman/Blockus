import sys
from fakes import BlokusStub

size = int(sys.argv[1])
start_positions = {(int(size/2 - 1), int(size/2 - 1)), (int(size/2),int(size/2))}
game = BlokusStub(2, size, start_positions)

print("┌──┐" * size)

for i, r in enumerate(game.grid):
    row: list[str] = []
    for j, c in enumerate(r):
        if c is None:
            if (i, j) in start_positions:
                row.append("│\x1b[1;30m██\x1b[1;30m│")
            else:
                row.append("│  │")
        elif c[0] == 1:
            row.append("│\x1b[1;34m██\x1b[1;30m│")
        else:
            row.append("│\x1b[1;31m██\x1b[1;30m│")
    print(''.join(row))
    if i != size - 1:
        print("├──┤" * size)

print("└──┘" * size)

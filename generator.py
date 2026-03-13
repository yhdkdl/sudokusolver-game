"""Puzzle generation helpers for Sudoku.

Exposes:
- rearrange(grid) -> list of 9 lists representing 3x3 blocks (non-zero values only)
- generate_puzzle(grid, amount=20) -> modifies grid in place and returns it
"""
import random
from validators import duplicate_checker


def rearrange(a):
    """Create a list of 9 lists representing the 3x3 subgrids.
    Each entry contains non-zero values within that subgrid, preserving insertion order.
    """
    temp = [[], [], [], [], [], [], [], [], []]
    count = 0
    ch = 0

    for e in range(len(a)):
        for x in range(3):
            if a[e][x] != 0:
                temp[ch].append(a[e][x])
        count += 1
        if count == 3:
            ch += 1
            count = 0

    for e in range(len(a)):
        for x in range(3, 6):
            if a[e][x] != 0:
                temp[ch].append(a[e][x])
        count += 1
        if count == 3:
            ch += 1
            count = 0

    for e in range(len(a)):
        for x in range(6, 9):
            if a[e][x] != 0:
                temp[ch].append(a[e][x])
        count += 1
        if count == 3:
            ch += 1
            count = 0

    return temp


def generate_puzzle(grid, amount=20):
    """Generate a puzzle by randomly placing `amount` numbers (best-effort).
    Modifies `grid` in-place and returns it.

    The generator preserves the original logic: attempts random placements and
    validates using rearranged subgrid duplication checks.
    """
    size = len(grid)
    for _ in range(amount):
        y = random.randint(0, size - 1)
        x = random.randint(0, size - 1)
        num = random.randint(1, size)
        allow = 0
        for e in range(size):
            if num not in grid[x] and num != grid[e][y]:
                allow += 1
        grid[x][y] = num
        tempo = rearrange(grid)
        for e in range(size):
            if duplicate_checker(tempo[e]):
                allow = 0
        if allow != size:
            grid[x][y] = 0
    return grid
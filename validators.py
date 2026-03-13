"""Validator helpers for Sudoku grid operations.

Functions:
- duplicate_checker(row_or_list) -> bool
- stay(grid, num, x, y) -> bool
- checkrow_horz(grid) -> bool
- checkrow_vert(grid) -> bool
- checkcol(grid) -> bool
"""
from typing import List


def duplicate_checker(a: List[int]) -> bool:
    """Return True if the list contains duplicates (ignoring zeros)."""
    filtered = [x for x in a if x != 0]
    return len(filtered) != len(set(filtered))


def stay(grid: List[List[int]], num: int, x: int, y: int) -> bool:
    """Return True if num can be placed at position (y, x) in grid without violating constraints."""
    # Check row
    for e in range(9):
        if grid[y][e] == num:
            return False
    # Check column
    for e in range(9):
        if grid[e][x] == num:
            return False
    # Check 3x3 box
    for i in range(3):
        for e in range(3):
            if grid[((y // 3) * 3) + i][((x // 3) * 3) + e] == num:
                return False
    return True


def checkrow_horz(a: List[List[int]]) -> bool:
    """Return True if any horizontal row contains duplicates."""
    for x in a:
        if duplicate_checker(x):
            return True
    return False


def checkrow_vert(a: List[List[int]]) -> bool:
    """Return True if any column contains duplicates."""
    for y in range(len(a)):
        temp = []
        for x in a:
            temp.append(x[y])
        if duplicate_checker(temp):
            return True
    return False


def checkcol(a: List[List[int]]) -> bool:
    """Return True if any 3x3 block contains duplicates."""
    # adapted from original logic: iterate over 3 block columns
    for y in range(3):
        temp = []
        for x in range(int(len(a) / 3)):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if duplicate_checker(temp):
            return True
        temp = []
        for x in range(3, (int(len(a) / 3)) * 2):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if duplicate_checker(temp):
            return True
        temp = []
        for x in range(6, (int(len(a) / 3)) * 3):
            temp.append(a[x][3 * y])
            temp.append(a[x][3 * y + 1])
            temp.append(a[x][3 * y + 2])
        if duplicate_checker(temp):
            return True
    return False

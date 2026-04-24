# Sudoku Solver and Generator

A comprehensive Sudoku application built in Python featuring a Constraint Satisfaction Problem (CSP) based solver, puzzle generator, and an interactive graphical user interface.

## Features

- **CSP-Based Solver**: Implements Minimum Remaining Values (MRV) heuristic, forward checking, and backtracking for efficient puzzle solving
- **Puzzle Generator**: Randomly generates valid Sudoku puzzles with configurable difficulty
- **Interactive GUI**: User-friendly Tkinter interface with real-time input validation
- **Game Features**:
  - Timer functionality
  - New Game generation
  - Reset board option
  - Hint system
  - Solution validation
- **Validation**: Comprehensive checks for Sudoku constraints (rows, columns, 3x3 boxes)

## Requirements

- Python 3.10 or higher (tested with Python 3.14)
- Tkinter (included with standard Python installations on Windows)

## Installation

1. Clone or download the project files
2. Ensure Python 3.10+ is installed on your system
3. No additional dependencies required - Tkinter comes bundled with Python

## Usage

### Running the Application

From the project root directory:

```bash
python GUI.py


or

```bash
python ui.py
``

### How to Play

1. **New Game**: Click "New Game" to generate a random Sudoku puzzle
2. **Fill Cells**: Click on any empty cell and enter numbers 1-9
3. **Solve**: Click "Solve" to automatically solve the current puzzle
4. **Reset**: Click "Reset" to clear all entered numbers
5. **Help**: Click "Help" for assistance
6. **Submit**: Click "Submit" to validate your solution

### Input Validation

- Only single digits (1-9) are accepted
- Invalid entries are automatically blocked
- The timer tracks your solving time

## How It Works

### Solver Algorithm

The solver uses a Constraint Satisfaction Problem approach:

1. **Domain Computation**: For each empty cell, calculates possible values based on Sudoku rules
2. **MRV Selection**: Chooses the cell with fewest remaining possibilities first
3. **Forward Checking**: Updates domains of related cells after each assignment
4. **Backtracking**: Recursively tries values, backtracking on conflicts

### Puzzle Generation

The generator creates puzzles by:
1. Starting with an empty grid
2. Randomly placing numbers while maintaining validity
3. Using validation checks to ensure no rule violations

## Project Structure

```
sudokusolver/
├── GUI.py          # Main GUI launcher
├── ui.py           # User interface and event handling
├── solver.py       # CSP-based Sudoku solver implementation
├── generator.py    # Puzzle generation utilities
├── validators.py   # Sudoku validation functions
├── README.md       # This file
└── __pycache__/    # Python bytecode cache
```

### Key Files

- **`solver.py`**: Core solving logic with MRV, forward checking, and backtracking
- **`ui.py`**: Tkinter GUI implementation with input validation and game controls
- **`generator.py`**: Random puzzle generation with validity checks
- **`validators.py`**: Constraint validation for rows, columns, and boxes

## Technical Details

- **Algorithm Complexity**: Exponential in worst case, but MRV and forward checking significantly improve performance
- **GUI Framework**: Tkinter for cross-platform compatibility
- **Threading**: Solver runs on background thread to prevent UI freezing
- **Memory Usage**: Minimal - operates on 9x9 integer grids

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

## License

This project is open source and available under the MIT License.


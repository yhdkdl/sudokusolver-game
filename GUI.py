import tkinter
from tkinter import *
import random
from validators import duplicate_checker, stay, checkrow_horz, checkrow_vert, checkcol

import sys
if __name__ == "__main__":
    from ui import main
    main()
    sys.exit()

root = Tk()
root.title("Sudoku")
root.minsize(width=700, height=550)
root.configure(bg="#f4f6f8")


title = Label(root, text='SUDOKU', fg="#382888", bg="#f4f6f8", font=("Helvetica", 32, "bold"))
title.pack(pady=8) 


entry_list = [[],[],[]]
var =[]
done = False
# Define a variable to keep track of the elapsed time
elapsed_time = 0
update_id = None

#guess = str()
grid = [
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0]
]

initial_grid = None


def update_time():
    global elapsed_time, done, update_id
    if not done:
        elapsed_time += 1
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        time_label.config(text=time_string)
        update_id = root.after(1000, update_time)

def submit():
    global done,update_id
    update_id = None
    done = True


def one_grid(row, row_index):
    global grid, entry_list
    entries = []
    
    for i in range(9):
        # create a new Entry widget for this cell in the grid
        entry = Entry(row, textvariable=var, width=2, highlightbackground="#888888", fg="#1a237e", font=("Helvetica", 20, "bold"), bg="white", justify=CENTER, bd=0, relief="flat")
        # position the cell within the grid using its index
        entry.place(x=(i % 3) * 47 + 5, y=(i // 3) * 47 + 5)
        # bind the show_possible_numbers function to the "<Button-1>" event of the Entry widget
        entry.bind("<Button-1>", show_possible_numbers)
        # add the new Entry widget to the list of entries for this row
        entries.append(entry)
        # add the new Entry widget to the global list of entries for the whole grid
        entry_list[i // 3].append(entry)

        entry_list[i // 3][row_index * 3 + i % 3] = entry
        # set the custom attribute "position" of the Entry widget to its position in the grid
        entry.position = (row_index, i)


    return entries

def display_val():
    global entry_list

    # Display values in the first three rows
    u=0
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(grid[u][y] != 0):
                a_splited[0][y].insert(0,grid[u][y]) 
        u+=1
    # Display values in the second three rows
    u=3
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(grid[u][y] != 0):
                a_splited[1][y].insert(0,grid[u][y]) 
        u+=1
    # Display values in the last three rows   
    u=6
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(grid[u][y] != 0):
                a_splited[2][y].insert(0,grid[u][y]) 
        u+=1

def clear():
    global grid
    grid = [[0] * 9 for _ in range(9)]


def reset_game():
    """Restore the board to the initial puzzle (if any) and reset timer."""
    global grid, initial_grid, elapsed_time, done, update_id
    # restore initial puzzle or clear
    if initial_grid is not None:
        grid = [row.copy() for row in initial_grid]
    else:
        clear()
    # refresh entries
    for a in entry_list:
        for b in a:
            b.delete(first=0, last=100)
    display_val()
    # reset and restart timer
    elapsed_time = 0
    time_label.config(text="00:00")
    if update_id is not None:
        try:
            root.after_cancel(update_id)
        except Exception:
            pass
    update_id = root.after(1000, update_time)
    done = False
    title.config(fg="#382888", text="Sudoku")
    posnum.config(text="")

def scramble():
    """Reset timer/UI then generate a new puzzle using generator.generate_puzzle."""
    global grid, initial_grid, elapsed_time, done, update_id
    elapsed_time = 0
    done = False
    if not update_id:
        update_id = root.after(1000, update_time)

    # clear GUI entries and grid
    clear()
    for a in entry_list:
        for b in a:
            b.delete(first=0, last=100)

    # generate puzzle (preserves previous generation logic)
    from generator import generate_puzzle
    generate_puzzle(grid, amount=20)

    # save the starting puzzle so Reset can restore it
    initial_grid = [row.copy() for row in grid]

    display_val()

# rearrange() moved to generator.py; use generator.rearrange when needed
# validator functions moved to validators.py; imported at top

def pressed_solve():
    """Attempt to solve the current grid using CSP (backtracking + forward checking + MRV)."""
    global grid, done, update_id
    done = False
    update_id = None

    if solve_csp(grid):
        done = True
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        display_val()
    else:
        title.config(fg="#990000", text="No solution")


from solver import solve_csp, compute_domains, select_mrv_cell


def pressed_solve():
    """Attempt to solve the current grid using the CSP solver module."""
    global grid, done, update_id
    done = False
    update_id = None

    if solve_csp(grid):
        done = True
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        display_val()
    else:
        title.config(fg="#990000", text="No solution")


def pressed_hint():
    """Fill one cell: choose MRV cell and set one of its possible values (uses solver module)."""
    global grid
    domains = compute_domains(grid)
    cell = select_mrv_cell(grid, domains)
    if cell is None:
        return
    r, c = cell
    candidates = domains.get((r, c), set())
    if candidates:
        grid[r][c] = next(iter(candidates))
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        display_val()
        return
    
def show_possible_numbers(event):
    global grid
    widget = event.widget

    row, col = widget.position

     #convert widget position to girt position
    x = (row // 3) * 3 + col // 3
    y = (row % 3) * 3 + col % 3

    numbers = [i for i in range(1,10)]
    exist  = []
    for i in range(9):
        # Check row
        if grid[x][i] in numbers:
            numbers.remove(grid[x][i])
        # Check column
        if grid[i][y] in numbers:
            numbers.remove(grid[i][y])
        # Check subgrid
        subgrid_x, subgrid_y = (x // 3) * 3, (y // 3) * 3
        for j in range(3):
            for k in range(3):
                if grid[subgrid_x + j][subgrid_y + k] in numbers:
                    numbers.remove(grid[subgrid_x + j][subgrid_y + k])
    for i in range(1,10):
        if i not in numbers:
            exist.append(i)
    posnum.config(text="Exist numbers: " + " ".join(str(num) for num in exist))

# validation logic moved to validators.py; imported at top (checkrow_horz, checkrow_vert, checkcol)

def submit():
    global entry_list
    
    temp = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    u=0
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(a_splited[0][y].get() != '' ):
                temp[u][y]= int(a_splited[0][y].get())
        u+=1
    u=3
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(a_splited[1][y].get() != '' ):
                temp[u][y]= int(a_splited[1][y].get())
        u+=1
        
    u=6
    for a in entry_list:
        a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
        for y in range(9):
            if(a_splited[2][y].get() != '' ):
                temp[u][y]= int(a_splited[2][y].get())
        u+=1
             
    if(checkrow_horz(temp) == True or checkrow_vert(temp) ==True or checkcol(temp) ==True):
        wrong()
    else:
        correct()

def wrong():
    title.config(fg="#990000", text="Try Again")
    rows = [canvas for canvas in box.winfo_children() if isinstance(canvas, Canvas)]
    for row in rows:
        row.config(highlightbackground="#990000")
        row.after(2100, lambda row=row: row.config(highlightbackground="white"))
    title.after(2100, lambda: title.config(fg="#382888", text="Sudoku"))


def correct():
    global done
    done = True
    highlight_color = "#288888"
    normal_color = "white"
    title.config(fg="#288888", text="Correct")
    rows = [canvas for canvas in box.winfo_children() if isinstance(canvas, Canvas)]
    for row in rows:
        row.config(highlightbackground=highlight_color)
        row.after(2100, lambda row=row: row.config(highlightbackground=normal_color))
    title.after(2100, lambda: title.config(fg="#382888", text="Sudoku"))


posnum = Label(root,text="", font=("Helvetica", 20, "bold"), bg="#f4f6f8")
posnum.pack()
#create a box (canvas) in the root master
box = Canvas(root, width=435, height=435, bd=6, highlightthickness=0, bg="#ffffff")
box.pack(side=LEFT, padx=20, pady=20)


coordinates = [(0, 0), (150, 0), (300, 0), (0, 150), (150, 150), (300, 150), (0, 300), (150, 300), (300, 300)]
#Create rows for the grid
for i in range(9):
    canvas = Canvas(box, width=120, height=120, background="#ffffff", bd=2, highlightthickness=2, highlightbackground="#888888")
    one_grid(canvas,i)
    canvas.place(x=coordinates[i][0], y=coordinates[i][1])
    globals()["row" + str(i+1)] = canvas



time_label = Label(root, text="00:00", font=("Helvetica", 28, "bold"), bg="#f4f6f8", fg="#1a237e")
time_label.pack(pady=12)

but = Frame(root, bg="#f4f6f8")
but.pack(padx=20, pady=10, anchor="n")
submitbtn = Button(but, text="Submit", fg="#282828", command=submit, font=("Helvetica", 16, "bold"), highlightbackground="#00ff00", justify=CENTER)
submitbtn.configure(bg="#ffffff", width=14)
submitbtn.pack(pady=6)

reset = Button(but, text="New Game", fg="#ffffff", command=scramble, font=("Helvetica", 16, "bold"), highlightbackground="#00BFFF", justify=CENTER)
reset.configure(bg='#382888', width=14)
reset.pack(pady=6)

# Clear / Reset board button (restores initial puzzle)
clear_btn = Button(but, text="Reset Board", fg="#282828", command=reset_game, font=("Helvetica", 16, "bold"), highlightbackground="#FFB6C1", justify=CENTER)
clear_btn.configure(bg='#F0F0F0', width=14)
clear_btn.pack(pady=6)

solve = Button(but, text="Solve", fg="#282828", command=pressed_solve, font=("Helvetica", 16, "bold"), highlightbackground="#FF8C00", justify=CENTER)
solve.configure(bg="#D4E2FC", width=14)
solve.pack(pady=6)

hint = Button(
    but,
    text="Help",
    fg="#282828",
    command=pressed_hint,
    font=("Helvetica", 16, "bold"),
    highlightbackground="#FFFF00",
    justify=CENTER
)
hint.configure(bg='#FCD4D4', width=14)
hint.pack(pady=6)


update_time()
scramble()

root.mainloop()

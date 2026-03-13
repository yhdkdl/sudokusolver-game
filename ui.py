import tkinter
from tkinter import *
from tkinter import ttk
import random
import threading
from solver import solve_csp, compute_domains, select_mrv_cell
from generator import generate_puzzle, rearrange
from validators import duplicate_checker, stay, checkrow_horz, checkrow_vert, checkcol


def main():
    root = Tk()
    root.title("Sudoku")
    root.minsize(width=700, height=550)

    title = Label(root, text='SUDOKU', fg="black", font=("Geneva", 30))
    title.pack()

    entry_list = [[], [], []]
    var = []
    done = False
    elapsed_time = 0
    update_id = None

    grid = [[0] * 9 for _ in range(9)]
    initial_grid = None

    def update_time():
        nonlocal elapsed_time, done, update_id
        if not done:
            elapsed_time += 1
            minutes = elapsed_time // 60
            seconds = elapsed_time % 60
            time_string = f"{minutes:02d}:{seconds:02d}"
            time_label.config(text=time_string)
            update_id = root.after(1000, update_time)

    # input validation: only single digits 1-9 allowed via Entry widget validation
    def on_validate(new_value):
        # allow empty to permit deletions
        if new_value == "":
            return True
        # only one character allowed
        if len(new_value) > 1:
            return False
        # must be a digit 1-9
        if new_value.isdigit() and 1 <= int(new_value) <= 9:
            return True
        return False

    vcmd = root.register(on_validate)

    # helpers to disable/enable controls while solver runs
    def disable_controls():
        for w in (submitbtn, reset, clear_btn, solve, hint):
            try:
                w.configure(state=DISABLED)
            except Exception:
                pass

    def enable_controls():
        for w in (submitbtn, reset, clear_btn, solve, hint):
            try:
                w.configure(state=NORMAL)
            except Exception:
                pass

    def submit():
        nonlocal done, update_id
        update_id = None
        done = True

    def one_grid(row, row_index):
        entries = []
        for i in range(9):
            entry = Entry(row, width=2, highlightbackground="#282828", fg="#0000CE", font=("Geneva", 30, "bold"), bg="whitesmoke", justify=CENTER, validate='key', validatecommand=(vcmd, '%P'))
            entry.place(x=(i % 3) * 47 + 5, y=(i // 3) * 47 + 5) 
            entry.bind("<Button-1>", show_possible_numbers)
            entries.append(entry)
            entry_list[i // 3].append(entry)
            entry_list[i // 3][row_index * 3 + i % 3] = entry
            entry.position = (row_index, i)
        return entries

    def display_val():
        # clear and display
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        u = 0
        for a in entry_list:
            a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
            for y in range(9):
                if grid[u][y] != 0:
                    a_splited[0][y].insert(0, grid[u][y])
            u += 1
        u = 3
        for a in entry_list:
            a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
            for y in range(9):
                if grid[u][y] != 0:
                    a_splited[1][y].insert(0, grid[u][y])
            u += 1
        u = 6
        for a in entry_list:
            a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
            for y in range(9):
                if grid[u][y] != 0:
                    a_splited[2][y].insert(0, grid[u][y])
            u += 1

    def clear():
        nonlocal grid
        grid = [[0] * 9 for _ in range(9)]

    def reset_game():
        nonlocal grid, initial_grid, elapsed_time, done, update_id
        if initial_grid is not None:
            grid = [row.copy() for row in initial_grid]
        else:
            clear()
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        display_val()
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
        nonlocal grid, initial_grid, elapsed_time, done, update_id
        elapsed_time = 0
        done = False
        if not update_id:
            update_id = root.after(1000, update_time)
        clear()
        for a in entry_list:
            for b in a:
                b.delete(first=0, last=100)
        generate_puzzle(grid, amount=20)
        initial_grid = [row.copy() for row in grid]
        display_val()

    def pressed_solve():
        nonlocal grid, done, update_id
        # Show a small modal progress dialog with indeterminate progress
        progress_win = Toplevel(root)
        progress_win.title("Solving…")
        progress_win.geometry("320x90")
        progress_win.transient(root)
        progress_win.grab_set()
        Label(progress_win, text="Thinking...", font=("Helvetica", 14)).pack(pady=(10, 4))
        pb = ttk.Progressbar(progress_win, mode='indeterminate', length=260)
        pb.pack(pady=(0, 10))
        pb.start(10)

        # disable controls while working
        disable_controls()

        def run_solver():
            # actual solve (runs in background thread)
            res = solve_csp(grid)

            def on_done():
                nonlocal done
                pb.stop()
                try:
                    progress_win.grab_release()
                except Exception:
                    pass
                progress_win.destroy()
                enable_controls()
                if res:
                    done = True
                    for a in entry_list:
                        for b in a:
                            b.delete(first=0, last=100)
                    display_val()
                else:
                    title.config(fg="#990000", text="No solution")

            root.after(0, on_done)

        # artificial wait (3s) before starting solver to show 'thinking' animation
        root.after(3000, lambda: threading.Thread(target=run_solver, daemon=True).start())

    def pressed_hint():
        nonlocal grid
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
        widget = event.widget
        row, col = widget.position
        x = (row // 3) * 3 + col // 3
        y = (row % 3) * 3 + col % 3
        numbers = [i for i in range(1, 10)]
        for i in range(9):
            if grid[x][i] in numbers:
                numbers.remove(grid[x][i])
            if grid[i][y] in numbers:
                numbers.remove(grid[i][y])
            subgrid_x, subgrid_y = (x // 3) * 3, (y // 3) * 3
            for j in range(3):
                for k in range(3):
                    if grid[subgrid_x + j][subgrid_y + k] in numbers:
                        numbers.remove(grid[subgrid_x + j][subgrid_y + k])
        exist = [i for i in range(1, 10) if i not in numbers]
        posnum.config(text="Exist numbers: " + " ".join(str(num) for num in exist))

    def submit_check():
        # Build a temp grid from the entries while validating input
        temp = [[0] * 9 for _ in range(9)]
        u = 0
        # helper to parse a row-block of entry_list
        def parse_block(offset):
            nonlocal temp, u
            for a in entry_list:
                a_splited = [a[x:x+9] for x in range(0, len(a), 9)]
                for y in range(9):
                    val = a_splited[offset][y].get()
                    if val != '':
                        # validate it's a digit 1-9
                        if not val.isdigit() or not (1 <= int(val) <= 9):
                            title.config(fg="#990000", text="Invalid input")
                            return False
                        temp[u][y] = int(val)
                u += 1
            return True

        # parse three vertical blocks (0,1,2) corresponding to the layout
        u = 0
        if not parse_block(0):
            return
        u = 3
        if not parse_block(1):
            return
        u = 6
        if not parse_block(2):
            return

        # ensure board is complete (no zeros)
        if any(temp[r][c] == 0 for r in range(9) for c in range(9)):
            title.config(fg="#990000", text="Incomplete")
            return

        # now check for duplicates in rows, columns and 3x3 blocks
        if checkrow_horz(temp) or checkrow_vert(temp) or checkcol(temp):
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
        nonlocal done
        done = True
        highlight_color = "#288888"
        normal_color = "white"
        title.config(fg="#288888", text="Correct")
        rows = [canvas for canvas in box.winfo_children() if isinstance(canvas, Canvas)]
        for row in rows:
            row.config(highlightbackground=highlight_color)
            row.after(2100, lambda row=row: row.config(highlightbackground=normal_color))
        title.after(2100, lambda: title.config(fg="#382888", text="Sudoku"))

    posnum = Label(root, text="", font="Geneva 25 bold")
    posnum.pack()
    box = Canvas(root, width = 435, height = 435, bd=6, highlightthickness=5)
    box.pack(side=LEFT) 

    coordinates = [(0, 0), (150, 0), (300, 0), (0, 150), (150, 150), (300, 150), (0, 300), (150, 300), (300, 300)]
    for i in range(9):
        canvas = Canvas(box, width=120, height=120, background="#282828", bd=10, highlightthickness=10)
        one_grid(canvas, i)
        canvas.place(x=coordinates[i][0], y=coordinates[i][1])
        globals()["row" + str(i+1)] = canvas

    time_label = Label(root,text="00:00", font="Geneva 30 bold")
    time_label.pack(pady =20)

    but = Frame(root, bg="#f4f6f8")
    but.pack(padx=20, pady=10, anchor="n")

    # Create the buttons but do not pack extras (they'll be toggled by Extras button)
    submitbtn = Button(but, text="Submit", fg="#282828", command=submit_check, font=("Helvetica", 16, "bold"), highlightbackground="#00ff00", justify=CENTER)
    submitbtn.configure(bg="#ffffff", width=14)

    reset = Button(but, text="New Game", fg="#ffffff", command=scramble, font=("Helvetica", 16, "bold"), highlightbackground="#00BFFF", justify=CENTER)
    reset.configure(bg='#382888', width=14)

    clear_btn = Button(but, text="Reset Board", fg="#282828", command=reset_game, font=("Helvetica", 16, "bold"), highlightbackground="#FFB6C1", justify=CENTER)
    clear_btn.configure(bg='#F0F0F0', width=14)

    solve = Button(but, text="Solve", fg="#282828", command=pressed_solve, font=("Helvetica", 16, "bold"), highlightbackground="#FF8C00", justify=CENTER)
    solve.configure(bg="#D4E2FC", width=14)

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

    # Pack all control buttons (no Extras toggle)
    submitbtn.pack(pady=6)
    reset.pack(pady=6)
    clear_btn.pack(pady=6)
    solve.pack(pady=6)
    hint.pack(pady=6)

    update_time()
    scramble()
    root.mainloop()

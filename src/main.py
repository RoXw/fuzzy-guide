import random
import tkinter as tk

from Solver import Solver


class SolutionDisplay:
    def __init__(self, solution: list):
        self.solution = solution
        self.window = tk.Tk()
        self.frames = []

    def displaySolution(self):
        for m, board in enumerate(self.solution):
            frame = tk.Frame(self.window)
            frame.grid(row=0, column=0, sticky="news")

            greeting = tk.Label(frame, text=f" # moves: {m}")
            greeting.grid(row=0, column=0, columnspan=2)

            self.createWidgets(board, frame)

            if board == self.solution[-1]:
                next_button = tk.Button(frame, text="Exit", command=self.window.quit)
            else:
                next_button = tk.Button(frame, text="Next")
                next_button.bind(
                    "<Button-1>", lambda e, frame=frame: self.goToNextWidget(frame)
                )
            next_button.grid(row=board.n + 1, column=board.n // 2)
            self.frames.append(frame)

        self.showFrame(self.frames[0])
        self.window.mainloop()

    def createWidgets(self, board, window):
        n = board.n
        for i in range(n):
            for j in range(n):
                label = tk.Label(
                    window,
                    text=board.tiles[i][j] if board.tiles[i][j] != 0 else " ",
                    width=8,
                    height=4,
                    borderwidth=2,
                    relief="groove",
                )
                label.grid(row=i + 1, column=j, padx=1, pady=1)

    def showFrame(self, frame):
        for child in frame.master.winfo_children():
            child.grid_remove()
        frame.grid()

    def goToNextWidget(self, current_frame):
        i = self.frames.index(current_frame)
        next_i = (i + 1) % len(self.frames)
        self.showFrame(self.frames[next_i])


def shuffle(values: list):
    for i in range(len(values)):
        x = random.randint(0, i)
        values[i], values[x] = values[x], values[i]


def main():
    n = int(input())
    tiles = [[0] * n for _ in range(n)]
    values = [i % (n * n) for i in range(1, n * n + 1)]
    shuffle(values)

    pos = 0
    for i in range(n):
        for j in range(n):
            tiles[i][j] = values[pos]
            pos += 1

    # tiles = [[0, 5, 2], [4, 8, 7], [1, 3, 6]]
    # tiles = [[9,10,6,11], [0,5,15,14], [1, 13, 3, 4], [8, 2, 12, 7]]
    print(tiles, sep="\n")

    solver = Solver(tiles)
    print(f"Total nodes explored: {solver.exploredNodes}")
    if solver.isSolvable():
        # for sol in solver.solution():
        #     print(sol)
        #     print("-"*5)
        SolutionDisplay(solver.solution()).displaySolution()
    else:
        print("No solution possible")


if __name__ == "__main__":
    main()

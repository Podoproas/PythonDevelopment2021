import time
import random
import tkinter as tk
from tkinter import messagebox


all_way_round = tk.N+tk.E+tk.S+tk.W


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Пятнашки")
        self.grid()
        self.buttons = []
        self.first_row = tk.Frame(self)
        self.new_button = tk.Button(self.first_row, text="New game", command=self.new_game)
        self.exit_button = tk.Button(self.first_row, text="Exit", command=self.quit)
        self.second_row = tk.Frame(self)
        self.column_configure()
        self.place_widgets()

    def column_configure(self):
        for x in range(8):
            tk.Grid.columnconfigure(self.first_row, x, weight=1)
        for y in range(8):
            tk.Grid.rowconfigure(self.first_row, y, weight=1)
        for x in range(4):
            tk.Grid.columnconfigure(self.second_row, x, weight=1, uniform="fred")
        for y in range(4):
            tk.Grid.rowconfigure(self.second_row, y, weight=1, uniform="fred")

    def place_widgets(self):
        self.new_button.grid(row=0, column=1, sticky=all_way_round, padx=10, columnspan=2)
        self.exit_button.grid(row=0, column=5, sticky=all_way_round, padx=10, columnspan=2)
        self.first_row.pack(expand=True, fill=tk.X)

        self.new_game()
        self.second_row.pack(expand=True, fill=tk.BOTH)
        self.pack(expand=True, fill=tk.BOTH)

    def new_game(self):
        for button in self.buttons:
            if button is not None:
                button.destroy()
        self.buttons = []
        nums = [i for i in range(1, 16)] + [None]
        for i in range(4):
            for j in range(4):
                my_num = random.choice(nums)
                nums.pop(nums.index(my_num))
                if my_num is None:
                    self.buttons.append(None)
                else:
                    self.buttons.append(tk.Button(self.second_row, text=str(my_num), command=self.get_func(i, j)))
                    self.buttons[-1].grid(row=i, column=j, sticky=all_way_round)

    def get_func(self, i, j):
        def move():
            none_ind = self.buttons.index(None)
            none_i = none_ind // 4
            none_j = none_ind % 4
            if abs(i - none_i) + abs(j - none_j) == 1:
                self.buttons[none_i * 4 + none_j], self.buttons[i * 4 + j] = \
                    self.buttons[i * 4 + j], self.buttons[none_i * 4 + none_j]
                self.buttons[none_i * 4 + none_j].configure(command=self.get_func(none_i, none_j))
                self.buttons[none_i * 4 + none_j].grid(row=none_i, column=none_j, sticky=tk.N+tk.E+tk.S+tk.W)
                self.win_check()

        return move

    def win_check(self):
        my_seq = [elem.cget('text') if elem is not None else None for elem in self.buttons]
        if list(filter(lambda x: x is not None, my_seq)) == [str(i) for i in range(1, 16)]:
            if messagebox.askyesno(title="You win!", message="Wanna one more time?"):
                self.new_game()


if __name__ == "__main__":
    app = Application()
    app.mainloop()

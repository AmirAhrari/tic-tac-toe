import tkinter
import tkinter.messagebox


tk = tkinter.Tk()
tk.title("Tic Tac Toe - offline")


class GUI:
    def __init__(self, tk):
        self.player = "X"
        self.tk = tk
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.keymap = {" ": "null", "O": 0, "X": 1}
        self.btns = []

    def _check_wins(self):
        b = self.board
        p = self.keymap[self.player]
        for q in b:
            if q[0] == p and q[1] == p and q[2] == p:
                return True

        for i in range(len(b)):
            if b[0][i] == p and b[1][i] == p and b[2][i] == p:
                return True

        if b[0][0] == p and b[1][1] == p and b[2][2] == p:
            return True

        if b[0][2] == p and b[1][1] == p and b[2][0] == p:
            return True

        return False

    def check_wins(self):
        if self._check_wins():
            tkinter.messagebox.showinfo("Game ends", f"{self.player} WON!")
            self.tk.destroy()

    def _check_ends(self):
        for b in self.board:
            for i in b:
                if i == None:
                    return False
        return True

    def check_ends(self):
        if self._check_ends():
            tkinter.messagebox.showinfo(
                "Game ends", "Game has been ended and no one won!"
            )
            self.tk.destroy()

    def btn_click(self, btn):
        btn = self.btns[int(btn)]
        col = btn.grid_info()["column"]
        row = btn.grid_info()["row"]
        self.board[col][row] = self.keymap[self.player]
        btn["text"] = self.player
        btn["state"] = tkinter.DISABLED
        self.check_wins()
        self.check_ends()
        # Change player
        self.player = "X" if self.player == "O" else "O"

    def draw(self):
        """Draw 3x3 buttons"""
        count = 0
        for row in range(3):
            for col in range(3):
                button = tkinter.Button(
                    self.tk,
                    text=" ",
                    font="Times 20 bold",
                    bg="gray",
                    fg="white",
                    height=4,
                    width=8,
                    command=lambda count=count: self.btn_click(count),
                )
                button.grid(row=row, column=col)
                count += 1
                self.btns.append(button)


GUI(tk).draw()
tk.mainloop()

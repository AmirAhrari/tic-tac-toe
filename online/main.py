import sys
import tkinter
import tkinter.messagebox
import threading

from lib.client import Client


tk = tkinter.Tk()
tk.title("Tic Tac Toe - online")


class GUI:
    def __init__(self, tk, sock):
        self.player = "X"
        self.my_turn = False
        self.tk = tk
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self.keymap = {" ": "null", "O": 0, "X": 1}
        self.btns = []
        self.sock = sock
        data = self.sock.recv()
        if data == "start":
            tkinter.messagebox.showinfo(
                "You are first", "You are first player you can start"
            )
            self.my_turn = True
        else:
            tkinter.messagebox.showinfo(
                "You are second", "You are second player wait for first player"
            )
            self.my_turn = False

    def _exit(self):
        self.tk.destroy()
        exit()

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
            self._exit()

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
            self._exit()

    def _btn_click(self, btn):
        btn = self.btns[int(btn)]
        col = btn.grid_info()["column"]
        row = btn.grid_info()["row"]
        self.board[col][row] = self.keymap[self.player]
        btn["text"] = self.player
        btn["state"] = tkinter.DISABLED
        self.check_wins()
        self.check_ends()
        # Change player turn
        self.player = "X" if self.player == "O" else "O"
        self.my_turn = not self.my_turn

    def btn_click(self, btn):
        if not self.my_turn:
            tkinter.messagebox.showwarning("Not your turn", "Is not your turn")
            return
        self.sock.send(str(btn))
        self._btn_click(btn)

    def handle_online_moves(self):
        """Handle second player moves from server"""
        if not self.my_turn:
            d = self.sock.recv()
            self._btn_click(d)
        while not self.check_ends():
            d = self.sock.recv()
            self._btn_click(d)

    def draw(self):
        """Draw 9x9 buttons and start new thread for online moves"""
        threading.Thread(target=self.handle_online_moves).start()
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


if __name__ == "__main__":
    # Connect to server
    c = Client()
    c.connect()

    g = GUI(tk, c)
    g.draw()
    tk.mainloop()

import re
from tkinter import TOP, BOTH, X, LEFT, RIGHT, S, RAISED, CENTER, Toplevel, SUNKEN
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Frame, Label, Entry, Style, Button
from ttkthemes import ThemedTk

from controllers import DataMingler, lotto_scraping


class LuckChecker(Frame):

    def __init__(self):
        super().__init__()
        self.detailsfont = ('helvetica', 15, 'bold')
        self.labelfont = ('helvetica', 17, 'bold')
        self.window_start_x = 300
        self.window_start_y = 300
        self.style = Style()

    def main_window(self):
        self.master.title("LOTTO checker")
        self.master.geometry("+%d+%d" % (self.window_start_x, self.window_start_y))
        self.pack(fill=BOTH, expand=True)

        fetched_lotto = lotto_scraping()[0]
        fetched_lotto_plus = lotto_scraping()[1]

        frame0 = Frame(self, relief=RAISED)
        frame0.pack(fill=X)

        lbl_main = Label(frame0,
                         text=f"\nToday's lucky numbers are: \n\nLotto: {fetched_lotto}\nPlus: {fetched_lotto_plus}",
                         font=self.labelfont, justify=CENTER)
        lbl_main.pack(side=TOP, padx=10, pady=10)

        add_button = Button(frame0, text="Show previous numbers", command=lambda: PopupWindow().popup_numbers())
        add_button.pack(side=TOP, anchor=S, padx=10, pady=10)

        self.results_part()
        DataMingler().add_current_number()

    def results_part(self):
        results = DataMingler().numbers_comparison()

        winner = results[0]
        looser = results[1]

        frame1 = Frame(self)
        frame1.pack(fill=BOTH, pady=10)

        lbl_2 = Label(frame1, text="\nChecking if any number is lucky today...", font=self.labelfont)
        lbl_2.pack(side=TOP, padx=10, pady=10)

        win_lbl = Label(frame1, text="{}".format(winner),
                        font=self.detailsfont, foreground="blue")
        win_lbl.pack(padx=5, pady=5)

        loose_lbl = Label(frame1, text="{}".format(looser), font=self.detailsfont, foreground="#516894", justify=CENTER)
        loose_lbl.pack(padx=5, pady=5)

        frame2 = Frame(self, relief=SUNKEN)
        frame2.pack(fill=BOTH, pady=10)

        add_button = Button(frame2, text="Add more numbers", command=lambda: PopupWindow().popup_now_number())
        add_button.pack(side=LEFT, anchor=S, padx=10, pady=10)

        close_button = Button(frame2, text="Quit", command=lambda: self.master.destroy())
        close_button.pack(side=RIGHT, anchor=S, padx=10, pady=10)


class PopupWindow(LuckChecker):

    def __init__(self):
        super().__init__()
        self.win = Toplevel()

    def popup_now_number(self):
        self.win.wm_title("Add new number")
        self.win.geometry("+%d+%d" % (self.window_start_x, self.window_start_y))

        lbl_add = Label(self.win,
                        text="Add a new number to your database:\n -->use \"-\" between numbers or it won\'t work <--",
                        justify=CENTER)
        lbl_add.grid(row=0, column=0, columnspan=2)

        lbl_name = Label(self.win, text="Number:", width=6)
        lbl_name.grid(row=1, column=0)

        entry_name = Entry(self.win)
        entry_name.config(width=15)
        entry_name.grid(row=1, column=1)

        add_button = Button(self.win, text="Add", command=lambda: self.btn_info(entry_name.get()))
        add_button.grid(row=2, column=0)

        close_button = Button(self.win, text="Quit", command=lambda: self.win.destroy())
        close_button.grid(row=2, column=1)

    def popup_numbers(self):
        self.win.wm_title("Previous lottery numbers")
        self.win.geometry("+%d+%d" % (self.window_start_x, self.window_start_y))

        prev_numbers = DataMingler().show_old_numbers()
        for row in prev_numbers:
            lbl_name = Label(self.win, text=f"{row[0]}")
            lbl_name.pack()

    @staticmethod
    def btn_info(param):
        if not param or not re.match(r"(^\d?\d[-]\d?\d[-]\d?\d[-]\d?\d[-]\d?\d[-]\d?\d$)", param):
            showerror("WARNING",
                      "Please, enter correct numbers.\n\nPattern: \n6 numbers from 1 to 49, separated by a \'-\'.")
        else:
            DataMingler().button_add_to_db(param)
            showinfo(title="GREAT!!",
                     message="New number added correctly. \nTo check new numbers you have to reload the app.")


if __name__ == '__main__':
    root = ThemedTk(theme="radiance")
    LuckChecker().main_window()
    root.mainloop()

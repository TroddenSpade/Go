from src.OnePlayer import OnePlayer
from src.TwoPlayer import TwoPlayer
import tkinter as tk


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Go 圍棋 ")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, OnePlayer, TwoPlayer):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Welcome, Let's Go!")
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="One Player",
                            command=lambda: controller.show_frame("OnePlayer"))
        button2 = tk.Button(self, text="Two Player",
                            command=lambda: controller.show_frame("TwoPlayer"))
        button1.pack()
        button2.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()

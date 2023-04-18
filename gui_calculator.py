from epic import *;
epic.start();

import tkinter;

class Calculator:
    def __init__(self, master):
        self.master = master;
        master.title("Calculator");

        self.entry = tkinter.Entry(master, width=25, font=("Arial", 12));
        self.entry.grid(row=0, column=0, columnspan=4, padx=5, pady=5);

        self.create_buttons();

    def create_buttons(self):
        self.buttons = [
            tkinter.Button(self.master, text="1", width=5, height=2, command=lambda:self.add_to_expression("1")),
            tkinter.Button(self.master, text="2", width=5, height=2, command=lambda:self.add_to_expression("2")),
            tkinter.Button(self.master, text="3", width=5, height=2, command=lambda:self.add_to_expression("3")),
            tkinter.Button(self.master, text="4", width=5, height=2, command=lambda:self.add_to_expression("4")),
            tkinter.Button(self.master, text="5", width=5, height=2, command=lambda:self.add_to_expression("5")),
            tkinter.Button(self.master, text="6", width=5, height=2, command=lambda:self.add_to_expression("6")),
            tkinter.Button(self.master, text="7", width=5, height=2, command=lambda:self.add_to_expression("7")),
            tkinter.Button(self.master, text="8", width=5, height=2, command=lambda:self.add_to_expression("8")),
            tkinter.Button(self.master, text="9", width=5, height=2, command=lambda:self.add_to_expression("9")),
            tkinter.Button(self.master, text="0", width=5, height=2, command=lambda:self.add_to_expression("0")),
            tkinter.Button(self.master, text="+", width=5, height=2, command=lambda:self.add_to_expression("+")),
            tkinter.Button(self.master, text="-", width=5, height=2, command=lambda:self.add_to_expression("-")),
            tkinter.Button(self.master, text="*", width=5, height=2, command=lambda:self.add_to_expression("*")),
            tkinter.Button(self.master, text="/", width=5, height=2, command=lambda:self.add_to_expression("/")),
            tkinter.Button(self.master, text="C", width=5, height=2, command=self.clear_expression),
            tkinter.Button(self.master, text="=", width=5, height=2, command=self.calculate_expression),
        ];

        for i, button in enumerate(self.buttons):
            button.grid(row=(i//4)+1, column=i%4, padx=5, pady=5);

    def add_to_expression(self, value):
        self.entry.insert(tkinter.END, value);

    def clear_expression(self):
        self.entry.delete(0, tkinter.END);

    def calculate_expression(self):
        expression = self.entry.get();
        result = eval(expression);
        self.entry.delete(0, tkinter.END);
        self.entry.insert(tkinter.END, result);

root = tkinter.Tk();
calculator = Calculator(root);
root.mainloop();

"""A simple calculator with a graphical interface, built with Tkinter."""

import ast
import operator
import tkinter as tk
from tkinter import messagebox

# Operators the calculator is allowed to evaluate.
OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def evaluate(expression):
    """Safely evaluate an arithmetic expression such as '2+3*4'."""
    tree = ast.parse(expression, mode="eval")

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](walk(node.operand))
        raise ValueError("Unsupported expression")

    return walk(tree)


class CalculatorApp:
    BUTTONS = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"],
    ]

    def __init__(self, root):
        self.root = root
        root.title("Calculator")
        root.resizable(False, False)

        self.display_var = tk.StringVar(value="0")
        entry = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            bd=8,
            relief="flat",
        )
        entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        for r, row in enumerate(self.BUTTONS, start=1):
            for c, label in enumerate(row):
                tk.Button(
                    root,
                    text=label,
                    font=("Arial", 18),
                    width=4,
                    height=1,
                    command=lambda value=label: self.press(value),
                ).grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

        tk.Button(
            root, text="C", font=("Arial", 18), command=self.clear
        ).grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        tk.Button(
            root, text="Back", font=("Arial", 18), command=self.backspace
        ).grid(row=5, column=2, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Keyboard support
        root.bind("<Return>", lambda event: self.press("="))
        root.bind("<BackSpace>", lambda event: self.backspace())
        root.bind("<Escape>", lambda event: self.clear())
        for key in "0123456789.+-*/":
            root.bind(key, lambda event, k=key: self.press(k))

    def press(self, value):
        current = self.display_var.get()
        if value == "=":
            self.calculate()
        elif current == "0" and value not in ".":
            self.display_var.set(value)
        else:
            self.display_var.set(current + value)

    def calculate(self):
        try:
            result = evaluate(self.display_var.get())
        except ZeroDivisionError:
            messagebox.showerror("Error", "Cannot divide by zero")
            self.clear()
            return
        except (ValueError, SyntaxError):
            messagebox.showerror("Error", "Invalid expression")
            self.clear()
            return
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        self.display_var.set(str(result))

    def clear(self):
        self.display_var.set("0")

    def backspace(self):
        current = self.display_var.get()[:-1]
        self.display_var.set(current if current else "0")


if __name__ == "__main__":
    root = tk.Tk()
    CalculatorApp(root)
    root.mainloop()

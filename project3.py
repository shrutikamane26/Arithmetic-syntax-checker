import re
import tkinter as tk
from tkinter import ttk

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception(f'Invalid character: {self.current_char} at position {self.pos}')

    def advance(self):
        self.pos += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception(f'Invalid syntax at position {self.lexer.pos}')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return str(token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            result = self.expr()
            self.eat(RPAREN)
            return result
        else:
            self.error()

    def term(self):
        result = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)
            result = f'({result} {token.value} {self.factor()})'
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)
            result = f'({result} {token.value} {self.term()})'
        return result

    def parse(self):
        result = self.expr()
        if self.current_token.type != EOF:
            self.error()
        return result

class CodeGenerator:
    def __init__(self, parser):
        self.parser = parser

    def generate_code(self):
        try:
            return eval(self.parser.parse())
        except Exception as e:
            raise Exception(f'Evaluation error: {str(e)}')

class ArithmeticInterpreterApp:
    def __init__(self, root):
        self.root = root
        root.title("Arithmetic Syntax Checker")

        self.input_label = ttk.Label(root, text="Enter an arithmetic expression:")
        self.input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.expression_entry = ttk.Entry(root, width=40)
        self.expression_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.result_label = ttk.Label(root, text="Result:")
        self.result_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.result_var = tk.StringVar()
        self.result_display = ttk.Label(root, textvariable=self.result_var)
        self.result_display.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        self.check_syntax_button = ttk.Button(root, text="Check Syntax", command=self.check_syntax)
        self.check_syntax_button.grid(row=2, column=0, columnspan=2, pady=10)

    def check_syntax(self):
        expression = self.expression_entry.get()
        lexer = Lexer(expression)
        parser = Parser(lexer)
        code_generator = CodeGenerator(parser)

        try:
            result = code_generator.generate_code()
            self.result_var.set(f"Result: {result}\nSyntax is valid.")
        except Exception as e:
            self.result_var.set(f"Syntax/Error: {str(e)}")

def main():
    root = tk.Tk()
    app = ArithmeticInterpreterApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()

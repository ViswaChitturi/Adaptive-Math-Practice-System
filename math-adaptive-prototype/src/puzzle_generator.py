from __future__ import annotations
import random
from typing import Tuple, Literal

Difficulty = Literal["Easy", "Medium", "Hard"]

class PuzzleGenerator:
    def __init__(self, rng: random.Random | None = None) -> None:
        self.rng = rng or random.Random()

    def _easy(self) -> Tuple[str, int]:
        # Single digit add/sub/mul, non-negative results for subtraction
        op = self.rng.choice(["+", "-", "×"])
        a = self.rng.randint(1, 9)
        b = self.rng.randint(1, 9)
        if op == "-":
            a, b = max(a, b), min(a, b)  # avoid negative results
            ans = a - b
        elif op == "+":
            ans = a + b
        else:  # ×
            ans = a * b
        return f"{a} {op} {b} = ?", ans

    def _medium(self) -> Tuple[str, int]:
        # Two-digit add/sub; 1-digit mul/div (integer division only)
        kind = self.rng.choice(["addsub", "mul", "div"])
        if kind == "addsub":
            op = self.rng.choice(["+", "-"])
            a = self.rng.randint(10, 99)
            b = self.rng.randint(10, 99)
            if op == "-":
                a, b = max(a, b), min(a, b)
                ans = a - b
            else:
                ans = a + b
            return f"{a} {op} {b} = ?", ans
        elif kind == "mul":
            a = self.rng.randint(10, 99)
            b = self.rng.randint(2, 9)
            return f"{a} × {b} = ?", a * b
        else:  # div with integer result: (a*b)/b
            b = self.rng.randint(2, 9)
            q = self.rng.randint(2, 12)
            a = b * q
            return f"{a} ÷ {b} = ?", q

    def _hard(self) -> Tuple[str, int]:
        # Two-digit × two-digit; division with integer result; mixed
        kind = self.rng.choice(["mul", "div", "mix"])
        if kind == "mul":
            a = self.rng.randint(12, 99)
            b = self.rng.randint(12, 99)
            return f"{a} × {b} = ?", a * b
        elif kind == "div":
            b = self.rng.randint(12, 25)
            q = self.rng.randint(5, 50)
            a = b * q
            return f"{a} ÷ {b} = ?", q
        else:  # mix: (a + b) × c or (a - b) × c with non-negative
            a = self.rng.randint(10, 99)
            b = self.rng.randint(1, 50)
            if a < b:
                a, b = b, a
            c = self.rng.randint(2, 9)
            op = self.rng.choice(["+", "-"])
            mid = a + b if op == "+" else a - b
            return f"({a} {op} {b}) × {c} = ?", mid * c

    def generate(self, difficulty: Difficulty) -> Tuple[str, int]:
        if difficulty == "Easy":
            return self._easy()
        if difficulty == "Medium":
            return self._medium()
        return self._hard()

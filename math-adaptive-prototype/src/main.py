from __future__ import annotations
import time
import csv
import os
from typing import Tuple
from src.puzzle_generator import PuzzleGenerator
from src.tracker import PerformanceTracker
from src.adaptive_engine import AdaptiveEngine, Difficulty

def prompt_int(msg: str) -> int:
    while True:
        val = input(msg).strip()
        if val.lower() == "q":
            return -1
        if val.isdigit():
            return int(val)
        print("Please enter a number (or 'q' to quit).")

def prompt_level() -> Difficulty:
    while True:
        s = input("Choose start level (Easy/Medium/Hard): ").strip().capitalize()
        if s in ("Easy", "Medium", "Hard"):
            return s  # type: ignore
        print("Please type Easy, Medium, or Hard.")

def run_session() -> None:
    print("=== Math Adventures — Adaptive Practice ===")
    name = input("Your name: ").strip() or "Player"
    start_level = prompt_level()
    num = prompt_int("How many puzzles? (e.g., 10): ")
    if num == -1:
        print("Goodbye!")
        return

    gen = PuzzleGenerator()
    tracker = PerformanceTracker()
    engine = AdaptiveEngine(start_level=start_level)

    print("\nType your answer and press Enter. Type 'q' anytime to stop.\n")

    qnum = 0
    while qnum < num:
        qnum += 1
        level = engine.level
        problem, answer = gen.generate(level)
        print(f"[Q{qnum} | {level}]  {problem}")
        t0 = time.perf_counter()
        user = input("> ").strip()
        if user.lower() == "q":
            qnum -= 1
            break
        t1 = time.perf_counter()
        try:
            user_val = int(user)
        except ValueError:
            user_val = None  # treated as incorrect

        correct = (user_val == answer)
        dt = t1 - t0
        tracker.record(qnum=qnum, problem=problem, level=level,
                       user_answer=user, correct=bool(correct), response_time_s=dt)

        prev_level = engine.update(correct=bool(correct), response_time_s=dt)
        new_level = engine.level
        if new_level != prev_level:
            tracker.add_transition(prev_level, new_level, qnum+1)  # transition affects next Q

        feedback = "✅ Correct!" if correct else f"❌ Oops, answer was {answer}"
        print(f"{feedback}  (Time: {dt:.1f}s)")
        if new_level != level:
            print(f"↪ Adapting difficulty → {new_level}\n")
        else:
            print()

    # Summary
    summ = tracker.summary_dict()
    total = summ["total_questions"]
    acc = summ["accuracy"] * 100 if total else 0.0
    avg = summ["avg_time"]
    print("\n==== Session Summary ====")
    print(f"Player: {name}")
    print(f"Questions answered: {total}")
    print(f"Accuracy: {acc:.1f}%")
    print(f"Average time/question: {avg:.2f}s")
    print("Accuracy by level:")
    for lvl, a in summ["accuracy_by_level"].items():
        print(f"  - {lvl}: {a*100:.1f}%")
    print("Avg time by level:")
    for lvl, t in summ["avg_time_by_level"].items():
        print(f"  - {lvl}: {t:.2f}s")
    if summ["transitions"]:
        print("Difficulty transitions: " + ", ".join(summ["transitions"]))
    print(f"Next recommended level: {engine.level}")

    # Save CSV log (use canonical absolute paths)
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    logs_dir = os.path.join(root, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(logs_dir, f"{name.replace(' ', '_')}_{stamp}.csv")
    with open(filename, "w", newline="", encoding="utf-8") as f:
        import csv as _csv
        writer = _csv.DictWriter(f, fieldnames=["qnum", "problem", "level", "user_answer", "correct", "response_time_s"])
        writer.writeheader()
        for row in tracker.to_csv_rows():
            writer.writerow(row)

    print(f"\nLog saved to: {os.path.abspath(filename)}")
    print("Thanks for playing!")

if __name__ == "__main__":
    run_session()

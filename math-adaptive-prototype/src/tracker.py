from __future__ import annotations
from typing import List, Dict, Any
from collections import defaultdict

class PerformanceTracker:
    def __init__(self) -> None:
        self.records: List[Dict[str, Any]] = []
        self.transitions: List[str] = []  # e.g., "Easy -> Medium (Q4)"

    def record(self, *, qnum: int, problem: str, level: str, user_answer: str,
               correct: bool, response_time_s: float) -> None:
        self.records.append({
            "qnum": qnum,
            "problem": problem,
            "level": level,
            "user_answer": user_answer,
            "correct": correct,
            "response_time_s": response_time_s,
        })

    def add_transition(self, from_level: str, to_level: str, qnum: int) -> None:
        if from_level != to_level:
            self.transitions.append(f"{from_level} -> {to_level} (Q{qnum})")

    def accuracy(self) -> float:
        if not self.records:
            return 0.0
        return sum(1 for r in self.records if r["correct"]) / len(self.records)

    def avg_time(self) -> float:
        if not self.records:
            return 0.0
        return sum(r["response_time_s"] for r in self.records) / len(self.records)

    def avg_time_by_level(self):
        sums = defaultdict(float)
        counts = defaultdict(int)
        for r in self.records:
            sums[r["level"]] += r["response_time_s"]
            counts[r["level"]] += 1
        return {lvl: (sums[lvl]/counts[lvl]) for lvl in counts}

    def accuracy_by_level(self):
        corrects = defaultdict(int)
        counts = defaultdict(int)
        for r in self.records:
            counts[r["level"]] += 1
            if r["correct"]:
                corrects[r["level"]] += 1
        return {lvl: (corrects[lvl]/counts[lvl]) for lvl in counts}

    def to_csv_rows(self):
        return list(self.records)

    def summary_dict(self):
        return {
            "total_questions": len(self.records),
            "accuracy": self.accuracy(),
            "avg_time": self.avg_time(),
            "avg_time_by_level": self.avg_time_by_level(),
            "accuracy_by_level": self.accuracy_by_level(),
            "transitions": list(self.transitions),
        }

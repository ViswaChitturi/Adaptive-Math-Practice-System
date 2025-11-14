from __future__ import annotations
from typing import Literal, Dict

Difficulty = Literal["Easy", "Medium", "Hard"]

TARGET_TIMES: Dict[Difficulty, float] = {
    "Easy": 5.0,
    "Medium": 7.0,
    "Hard": 10.0,
}

class AdaptiveEngine:
    def __init__(self, start_level: Difficulty = "Easy") -> None:
        assert start_level in ("Easy", "Medium", "Hard")
        self.levels = ["Easy", "Medium", "Hard"]
        self.level_index = self.levels.index(start_level)
        self.momentum = 0.0  # bounded in [-3, 3]

    @property
    def level(self) -> Difficulty:
        return self.levels[self.level_index]  # type: ignore

    def _clamp(self, x: float, lo: float, hi: float) -> float:
        return max(lo, min(hi, x))

    def _delta(self, correct: bool, response_time_s: float) -> float:
        target = TARGET_TIMES[self.level]
        delta = 1.0 if correct else -1.0
        if correct and response_time_s < 0.7 * target:
            delta += 0.5  # fast bonus
        if response_time_s > 1.5 * target:
            delta -= 0.5  # slow penalty
        return delta

    def update(self, *, correct: bool, response_time_s: float) -> Difficulty:
        # Compute delta and update momentum with decay.
        d = self._delta(correct, response_time_s)
        self.momentum = 0.5 * self.momentum + d
        self.momentum = self._clamp(self.momentum, -3.0, 3.0)

        # Decide level change
        prev_idx = self.level_index
        if self.momentum >= 2.0 and self.level_index < len(self.levels) - 1:
            self.level_index += 1
            self.momentum = 0.0  # reset on change
        elif self.momentum <= -2.0 and self.level_index > 0:
            self.level_index -= 1
            self.momentum = 0.0

        return self.levels[prev_idx]  # return previous level for logging

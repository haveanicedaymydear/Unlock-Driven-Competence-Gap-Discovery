"""Minimal unlock-driven competence-gap selector.

This file implements the transparent scoring scaffold described in the project
README. It does not include Craftax integration or a trained policy.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable


@dataclass(slots=True)
class CompetenceRecord:
    name: str
    acquired: bool = False
    successful_attempts: int = 0
    failed_attempts: int = 0
    downstream: dict[str, float] = field(default_factory=dict)

    @property
    def attempts(self) -> int:
        return self.successful_attempts + self.failed_attempts

    @property
    def feasibility(self) -> float:
        """Smoothed empirical success probability.

        A Beta(1, 1) prior avoids zero-probability lockout for untried skills.
        """
        return (self.successful_attempts + 1) / (self.attempts + 2)

    @property
    def unlock_potential(self) -> float:
        """Confidence-weighted number of downstream competencies."""
        return sum(max(0.0, min(1.0, confidence)) for confidence in self.downstream.values())

    @property
    def frontier_priority(self) -> float:
        if self.acquired:
            return 0.0
        return self.feasibility * self.unlock_potential


class UnlockDrivenSelector:
    """Maintain a small inferred skill graph and select the next frontier."""

    def __init__(self, competences: Iterable[str] = ()) -> None:
        self.records: dict[str, CompetenceRecord] = {
            name: CompetenceRecord(name=name) for name in competences
        }

    def ensure(self, name: str) -> CompetenceRecord:
        if name not in self.records:
            self.records[name] = CompetenceRecord(name=name)
        return self.records[name]

    def record_attempt(self, name: str, success: bool) -> None:
        record = self.ensure(name)
        if success:
            record.successful_attempts += 1
        else:
            record.failed_attempts += 1

    def mark_acquired(self, name: str) -> None:
        self.ensure(name).acquired = True

    def add_inferred_unlock(self, prerequisite: str, unlocked: str, confidence: float) -> None:
        if prerequisite == unlocked:
            raise ValueError("A competence cannot unlock itself")
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must lie in [0, 1]")
        self.ensure(prerequisite).downstream[unlocked] = confidence
        self.ensure(unlocked)

    def rank_frontier(self) -> list[CompetenceRecord]:
        return sorted(
            (record for record in self.records.values() if not record.acquired),
            key=lambda record: (
                record.frontier_priority,
                record.unlock_potential,
                record.feasibility,
                record.name,
            ),
            reverse=True,
        )

    def select_next(self) -> CompetenceRecord | None:
        ranked = self.rank_frontier()
        return ranked[0] if ranked else None

    def snapshot(self) -> list[dict]:
        return [
            {
                "name": record.name,
                "acquired": record.acquired,
                "attempts": record.attempts,
                "feasibility": round(record.feasibility, 4),
                "unlock_potential": round(record.unlock_potential, 4),
                "frontier_priority": round(record.frontier_priority, 4),
                "downstream": dict(sorted(record.downstream.items())),
            }
            for record in sorted(self.records.values(), key=lambda item: item.name)
        ]


def demo() -> None:
    selector = UnlockDrivenSelector(["craft_pickaxe", "mine_iron", "build_furnace"])
    selector.record_attempt("craft_pickaxe", success=True)
    selector.record_attempt("craft_pickaxe", success=False)
    selector.record_attempt("mine_iron", success=False)
    selector.add_inferred_unlock("craft_pickaxe", "mine_iron", confidence=0.9)
    selector.add_inferred_unlock("mine_iron", "build_furnace", confidence=0.8)

    chosen = selector.select_next()
    print("Selected frontier:", None if chosen is None else chosen.name)
    for row in selector.snapshot():
        print(row)


if __name__ == "__main__":
    demo()

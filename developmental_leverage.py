"""Minimal developmental-leverage selector for the v0.3 research scaffold.

The module implements a transparent, dependency-free approximation of the
proposal's current first-paper mechanism. It does not include Craftax, PPO,
gradient sketches, or trained calibration models. Instead, it exposes the
state and scoring interfaces that those components will populate.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping


@dataclass(slots=True)
class SkillState:
    """Current evidence about one candidate capability."""

    name: str
    competence: float = 0.0
    successful_attempts: int = 0
    failed_attempts: int = 0
    transfer_to: dict[str, float] = field(default_factory=dict)

    @property
    def attempts(self) -> int:
        return self.successful_attempts + self.failed_attempts

    @property
    def feasibility(self) -> float:
        """Beta(1, 1)-smoothed empirical success probability."""
        return (self.successful_attempts + 1) / (self.attempts + 2)


class DevelopmentalLeverageSelector:
    """Rank feasible skills by transfer to unresolved competence.

    DLS(i) = feasibility(i) * sum_j weight(j) * [T(i,j)]+ * (1 - c(j))

    Transfer values may be raw proxy estimates or sparsely calibrated values.
    The environment's ground-truth prerequisite graph is not required.
    """

    def __init__(
        self,
        skills: Iterable[str] = (),
        *,
        minimum_feasibility: float = 0.05,
        maximum_competence: float = 0.95,
    ) -> None:
        if not 0.0 <= minimum_feasibility <= 1.0:
            raise ValueError("minimum_feasibility must lie in [0, 1]")
        if not 0.0 <= maximum_competence <= 1.0:
            raise ValueError("maximum_competence must lie in [0, 1]")
        self.minimum_feasibility = minimum_feasibility
        self.maximum_competence = maximum_competence
        self.skills: dict[str, SkillState] = {
            name: SkillState(name=name) for name in skills
        }
        self.weights: dict[str, float] = {}

    def ensure(self, name: str) -> SkillState:
        if name not in self.skills:
            self.skills[name] = SkillState(name=name)
        return self.skills[name]

    def set_competence(self, name: str, competence: float) -> None:
        if not 0.0 <= competence <= 1.0:
            raise ValueError("competence must lie in [0, 1]")
        self.ensure(name).competence = competence

    def set_weight(self, name: str, weight: float) -> None:
        if weight < 0.0:
            raise ValueError("weight must be non-negative")
        self.ensure(name)
        self.weights[name] = weight

    def record_attempt(self, name: str, success: bool) -> None:
        skill = self.ensure(name)
        if success:
            skill.successful_attempts += 1
        else:
            skill.failed_attempts += 1

    def set_transfer(self, source: str, target: str, estimate: float) -> None:
        """Store a proxy or calibrated cross-skill transfer estimate.

        Values are bounded to [-1, 1]. Negative values represent interference
        and are retained for inspection, although the minimal DLS uses only
        positive transfer.
        """
        if source == target:
            raise ValueError("source and target skills must differ")
        if not -1.0 <= estimate <= 1.0:
            raise ValueError("transfer estimate must lie in [-1, 1]")
        self.ensure(source).transfer_to[target] = estimate
        self.ensure(target)

    def calibrate_transfers(self, alpha: float, beta: float = 0.0) -> None:
        """Apply a lightweight linear calibration to all stored proxies."""
        for skill in self.skills.values():
            for target, raw in tuple(skill.transfer_to.items()):
                skill.transfer_to[target] = max(-1.0, min(1.0, alpha * raw + beta))

    def developmental_leverage(self, name: str) -> float:
        source = self.ensure(name)
        if source.competence >= self.maximum_competence:
            return 0.0
        if source.feasibility < self.minimum_feasibility:
            return 0.0

        unresolved_transfer = 0.0
        for target_name, transfer in source.transfer_to.items():
            target = self.ensure(target_name)
            remaining = max(0.0, 1.0 - target.competence)
            weight = self.weights.get(target_name, 1.0)
            unresolved_transfer += weight * max(0.0, transfer) * remaining

        return source.feasibility * unresolved_transfer

    def rank_frontier(self) -> list[tuple[SkillState, float]]:
        ranked = [
            (skill, self.developmental_leverage(skill.name))
            for skill in self.skills.values()
            if skill.competence < self.maximum_competence
        ]
        return sorted(
            ranked,
            key=lambda item: (
                item[1],
                item[0].feasibility,
                -item[0].competence,
                item[0].name,
            ),
            reverse=True,
        )

    def select_next(self) -> SkillState | None:
        ranked = self.rank_frontier()
        return ranked[0][0] if ranked else None

    def snapshot(self) -> list[Mapping[str, object]]:
        return [
            {
                "name": skill.name,
                "competence": round(skill.competence, 4),
                "feasibility": round(skill.feasibility, 4),
                "developmental_leverage": round(
                    self.developmental_leverage(skill.name), 4
                ),
                "transfer_to": dict(sorted(skill.transfer_to.items())),
            }
            for skill in sorted(self.skills.values(), key=lambda item: item.name)
        ]


def demo() -> None:
    selector = DevelopmentalLeverageSelector(
        ["craft_pickaxe", "mine_iron", "build_furnace"]
    )
    selector.record_attempt("craft_pickaxe", success=True)
    selector.record_attempt("craft_pickaxe", success=False)
    selector.record_attempt("mine_iron", success=False)
    selector.set_competence("mine_iron", 0.10)
    selector.set_competence("build_furnace", 0.05)
    selector.set_transfer("craft_pickaxe", "mine_iron", 0.80)
    selector.set_transfer("craft_pickaxe", "build_furnace", 0.45)
    selector.set_transfer("mine_iron", "build_furnace", 0.60)

    selected = selector.select_next()
    print("Selected capability:", None if selected is None else selected.name)
    for row in selector.snapshot():
        print(row)


# Backward-compatible name for early repository users.
UnlockDrivenSelector = DevelopmentalLeverageSelector


if __name__ == "__main__":
    demo()

# Research Plan

## Motivation

An open-ended agent must decide not only how to solve a task, but what capability to learn next. Existing curricula often prioritize immediate difficulty, novelty, prediction error, or regret. Those criteria can improve local learning progress without necessarily expanding the agent's reachable future task set.

This project studies an alternative objective: **unlock-driven competence-gap discovery**.

## Research question

> Can an agent infer latent prerequisite structure from its own trajectories and select the next competence by expected expansion of future reachability?

## Proposed system

The intended Craftax prototype contains five components:

1. **Trajectory recorder** - stores observations, actions, rewards, achievements, and temporal order.
2. **Competence estimator** - estimates whether a candidate skill is currently feasible.
3. **Unlock-graph learner** - infers directed relations between acquired skills and later reachable achievements.
4. **Frontier selector** - ranks missing skills by unlock potential multiplied by feasibility.
5. **Policy learner** - trains or adapts behaviour toward the selected frontier objective.

The ground-truth achievement tree is hidden during learning. It may be used only after training for graph-fidelity evaluation.

## Minimal implemented scaffold

The current public code implements:

- competence records;
- smoothed feasibility estimation from attempts;
- confidence-weighted downstream reach;
- frontier ranking;
- explicit acquired/unacquired state;
- tests for ranking and graph constraints.

It does not yet implement trajectory-based causal graph induction or policy learning.

## Main hypotheses

- H1: Unlock-driven selection increases achievement coverage under a fixed interaction budget.
- H2: Learned prerequisite structure becomes more faithful as the agent accumulates diverse trajectories.
- H3: Different early experiences produce distinguishable developmental stages and later skill choices.
- H4: Explicit uncertainty over inferred dependencies reduces lock-in after early graph errors.

## Baselines

Planned baselines include:

- random frontier selection;
- novelty-driven selection;
- learning-progress selection;
- regret or failure-driven selection;
- oracle achievement-tree selection, used only as an upper-bound reference.

## Scope boundary

The first full study is single-agent. Team-level competence acquisition and role differentiation are later extensions. The repository does not claim completed multi-agent learning results.

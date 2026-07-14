# Unlock-Driven Competence Gap Discovery

**A Minimal Architecture for Developmental Agency**

This project asks a different curriculum-learning question:

> Which competence should an agent acquire next if the objective is to expand the set of future tasks it can reach?

Most automatic curricula prioritize immediate difficulty, novelty, prediction error, or regret. This project instead defines an **unlock-driven competence gap**: a missing skill whose acquisition is expected to make the largest new region of the agent's future task space reachable, while remaining feasible enough to learn now.

## Core hypothesis

An agent can estimate a latent skill-unlock graph from its own trajectories, without receiving the environment's ground-truth achievement tree, and use that graph to select frontier goals by:

```text
frontier priority = estimated unlock potential x estimated feasibility
```

The project is being developed for Craftax-style long-horizon environments, where achievements exhibit prerequisite structure and early experience can change later developmental trajectories.

## Current public status

This repository is an honest research scaffold, not a completed benchmark result. It currently contains:

- a minimal, runnable unlock-driven frontier selector;
- an explicit representation of inferred skill dependencies;
- unit tests for scoring and selection behaviour;
- a research plan and evaluation protocol;
- clear boundaries between implemented components and planned Craftax experiments.

The current code does **not** yet claim:

- a trained Craftax policy;
- a validated learned achievement graph;
- multi-agent reinforcement-learning results;
- AAAI or AAMAS submission status.

## Quick start

Requires Python 3.10+ and no third-party runtime dependencies.

```bash
python unlock_driven.py
python -m unittest discover -s tests -v
```

## Minimal mechanism

For every candidate competence, the selector tracks:

- successful and failed attempts, used to estimate feasibility;
- inferred downstream skills that may become reachable;
- confidence in the inferred dependencies;
- whether the competence has already been acquired.

The public scaffold ranks unacquired frontier skills by a transparent product of feasibility and weighted downstream reach. The initial heuristic is deliberately simple so that later Craftax experiments can test whether richer graph inference is actually necessary.

## Planned Craftax evaluation

The full research prototype will:

1. collect the agent's own trajectories;
2. infer a directed skill-unlock graph without access to the ground-truth achievement tree;
3. select frontier goals using unlock potential and feasibility;
4. train or adapt a policy toward the selected frontier;
5. update the inferred graph as new competencies are acquired.

Planned metrics include:

- achievement coverage;
- sample efficiency;
- learned-graph fidelity against the hidden evaluation graph;
- emergent developmental stages;
- trajectory divergence under different early experiences;
- robustness when early inferred dependencies are wrong.

## Multi-agent extension

A later extension will study team-level competence acquisition: which skill should one agent acquire next to expand what a team can jointly achieve? This connection to lifelong multi-agent learning is a planned research direction, not a completed result.

## Repository structure

```text
.
├── unlock_driven.py
├── tests/test_unlock_driven.py
├── docs/research-plan.md
├── docs/evaluation-plan.md
└── .github/workflows/tests.yml
```

## Status

Sole-author research prototype and manuscript in preparation, July 2026.

## Author

Livan Zhou - [zhoulivan@gmail.com](mailto:zhoulivan@gmail.com)

## License

MIT License. See [LICENSE](LICENSE).

# Learning What to Learn Next

**Sparse Intervention-Calibrated Developmental Leverage for Autonomous Curriculum Learning**

This project studies a minimal but central component of **Developmental Agency**:

> Given what an agent has become so far, which currently learnable capability should it develop next?

Most automatic curricula prioritize difficulty, novelty, failure, regret, immediate learning progress, or a fixed prerequisite graph. This project instead asks which training choice is most likely to improve the largest amount of competence the current agent still lacks.

## Current scientific object

For candidate skill `i`, the v0.3 proposal defines a transparent **Developmental Leverage Score (DLS)**:

```text
DLS(i) = feasibility(i)
         × Σ_j positive_transfer(i → j)
         × unresolved_competence(j)
```

A capability has high developmental leverage when:

- it is currently feasible to train;
- training it is estimated to help other capabilities;
- those downstream capabilities remain unresolved;
- its value is specific to this agent and developmental stage.

This differs from simply counting descendants in an achievement tree. The project explicitly separates:

1. **Environment affordance structure** — what the world makes physically or procedurally reachable.
2. **Agent-specific competence transfer** — how training one capability changes this agent's other capabilities.

## v0.3 method

The first-paper implementation is designed for a single consumer GPU.

### 1. Goal-conditioned competence state

The agent is evaluated separately on predefined achievement goals to form a competence vector.

### 2. Low-cost transfer proxy

The preferred first implementation uses compact gradient-affinity estimates derived from ordinary training data. Aligned goal gradients are treated as a candidate signal of positive transfer; conflicting gradients indicate possible interference.

### 3. Sparse real interventions

The proxy is not assumed to be correct by itself. At a small number of predetermined checkpoints, only 2–4 frontier skills are probed sequentially from the same saved checkpoint and compared with a matched control branch.

### 4. Lightweight calibration

Sparse intervention results calibrate the proxy with a low-parameter estimator such as ridge regression, Bayesian linear regression, isotonic calibration, or linear UCB.

### 5. Developmental arbitration

The calibrated transfer estimate is combined with current feasibility and unresolved competence to choose the next training goal.

All probe interactions and GPU costs are counted in the final comparison.

## Why the design changed

The earlier v0.1 scaffold ranked skills by estimated downstream reach multiplied by feasibility. That implementation remains useful as a transparent graph-centrality baseline, but it is no longer the intended main contribution.

The v0.3 research claim is narrower and stronger:

> Use sparsely calibrated, agent- and stage-specific cross-skill transfer estimates to decide which currently learnable capability should receive the next training budget.

## Current public status

This repository is an honest research scaffold, not a completed Craftax result. It currently contains:

- a dependency-free DLS selector;
- explicit competence, feasibility, and cross-skill transfer state;
- a lightweight linear calibration interface;
- automated tests for developmental-leverage behaviour;
- the v0.3 research and evaluation plans.

The repository does **not** yet claim:

- a trained Craftax policy;
- validated gradient-transfer predictions;
- improved curriculum performance;
- AAAI submission or acceptance;
- a complete self-developing agent.

## Quick start

Requires Python 3.10+ and no third-party runtime dependencies.

```bash
python developmental_leverage.py
python -m unittest discover -s tests -v
```

## Planned first-paper experiments

1. **Transfer prediction** — compare the cheap proxy with measured sparse intervention effects.
2. **Calibration value** — test whether a few real probes improve held-out transfer ranking.
3. **Curriculum performance** — compare DLS with random, fixed, feasibility-only, novelty, learning-progress, graph-centrality, and static-transfer curricula under matched total budgets.
4. **Agent and stage specificity** — test whether transfer estimates change across agents and checkpoints.

The primary practical benchmark is **Craftax-Classic-Symbolic**. Full Craftax is an optional extension after the core mechanism is stable.

## Long-term upgrade: neural Counterfactual Unlock Value

The stronger long-horizon formulation is retained as Phase II.

Once enough intervention data exist across agents, checkpoints, skills, and environments, an uncertainty-aware neural predictor can estimate:

```text
current developmental state + candidate skill + short intervention signature
→ long-horizon competence expansion
```

This neural CUV predictor is deferred for data and compute reasons, not rejected conceptually.

## Repository structure

```text
.
├── developmental_leverage.py
├── tests/test_developmental_leverage.py
├── docs/research-plan.md
├── docs/evaluation-plan.md
├── docs/proposal-v0.3.md
└── .github/workflows/tests.yml
```

## Status

Sole-author research proposal and implementation in progress, July 2026.

## Author

Livan Zhou — [zhoulivan@gmail.com](mailto:zhoulivan@gmail.com)

## License

MIT License. See [LICENSE](LICENSE).

# Research Plan v0.3

## Working title

**Learning What to Learn Next: Sparse Intervention-Calibrated Developmental Leverage for Autonomous Curricula**

## Motivation

An open-ended agent must decide not only how to solve a task, but what capability to develop next. Existing automatic curricula usually prioritize difficulty, novelty, failure, regret, immediate learning progress, external prerequisite structure, or foundation-model priors.

Those criteria do not directly estimate which training choice is most likely to improve the largest amount of competence the current agent still lacks.

This project isolates one falsifiable component of **Developmental Agency**:

> Can an agent estimate which currently learnable capability has the greatest downstream developmental leverage for itself at its present stage?

## Research question

> Can a low-cost cross-skill transfer signal, calibrated by a small number of real training interventions, identify which currently learnable skill will provide the greatest benefit to unresolved competence under a fixed total budget?

## Scope

The first paper studies developmental arbitration over a predefined achievement vocabulary. It does not claim unrestricted goal invention, autobiographical identity, consciousness, autonomous code modification, or a complete digital life.

## Formal state

Let:

- `S` be the set of achievement goals;
- `c_t[j]` be current competence on goal `j`;
- `f_t[i]` be current feasibility of training goal `i`;
- `T_t[i,j]` be estimated transfer from training `i` to competence `j`.

The candidate frontier contains unresolved goals that are currently learnable.

## Developmental Leverage Score

```text
DLS_t(i) = f_t(i) × Σ_j w_j × [T_t(i,j)]+ × (1 - c_t(j))
```

A skill receives high priority when:

1. it is feasible now;
2. its training is estimated to help other skills;
3. those skills remain unresolved;
4. its value is specific to this agent and checkpoint.

## Separation of structures

### Environment affordance structure

Describes what the world makes physically or procedurally reachable. A Craftax achievement tree belongs here.

### Agent-specific competence-transfer structure

Describes how training one capability changes the current agent's performance on other capabilities. It may differ across agents and change during development.

The first-paper claim concerns the second structure. Recovering an environment technology tree is not enough.

## Low-cost transfer proxy

The preferred first implementation uses goal-conditioned gradient affinity:

```text
P_t(i,j) = cosine(gradient_sketch_i, gradient_sketch_j)
```

Only selected shared layers are sketched. Aligned gradients are treated as a candidate signal of positive transfer; conflicting gradients indicate possible interference.

If this proxy is unstable, one alternative will be tested at a time, such as historical competence co-improvement or representation similarity.

## Sparse intervention calibration

The cheap proxy is not treated as ground truth.

At a small number of predetermined checkpoints:

1. choose only 2–4 frontier skills;
2. reuse the same saved checkpoint sequentially;
3. micro-train one branch per candidate plus a matched control;
4. evaluate relevant goals with common random seeds;
5. estimate empirical cross-skill transfer;
6. fit a low-parameter calibration model.

Candidate calibrators include ridge regression, Bayesian linear regression, isotonic calibration, or linear UCB.

Online exhaustive branching is explicitly excluded from the first-paper method.

## Main hypotheses

- **H1 — Transfer prediction:** calibrated proxy estimates predict measured cross-skill transfer better than difficulty, novelty, failure, immediate learning progress, graph centrality, and raw gradient affinity.
- **H2 — Budgeted performance:** DLS-guided training improves competence coverage or developmental regret under a fixed total interaction budget that includes probes.
- **H3 — Calibration efficiency:** a small number of sparse interventions materially improves transfer ranking.
- **H4 — Agent specificity:** dynamic agent-conditioned transfer estimates outperform a static population-average matrix.
- **H5 — Stage dependence:** the leverage of the same skill changes across developmental checkpoints.

## Required baselines

- vanilla PPO;
- random frontier;
- fixed curriculum;
- feasibility-only curriculum;
- novelty-based curriculum;
- learning-progress curriculum;
- graph centrality multiplied by feasibility;
- raw uncalibrated transfer proxy;
- static transfer matrix;
- calibrated dynamic DLS.

A sparse intervention oracle may be reported as an upper bound.

## Environments

### Stage A — dependency-control environment

A lightweight environment with controlled shared subskills and inexpensive exhaustive transfer measurement.

### Stage B — Craftax-Classic-Symbolic

Primary first-paper benchmark.

### Optional Stage C — full Craftax-Symbolic

Attempted only after the core mechanism and baseline matrix are stable.

## Engineering order

1. reproducible reduced-memory PPO baseline;
2. achievement logging and checkpoint restoration;
3. goal-conditioned competence evaluation;
4. gradient-transfer proxy;
5. sparse intervention engine;
6. lightweight calibration;
7. DLS arbitration;
8. budget-matched curriculum experiments.

## Current implementation boundary

The public dependency-free selector implements the DLS state and scoring interface. It does not yet implement Craftax, PPO, gradient sketches, or calibrated empirical results.

## Long-term Phase II: neural Counterfactual Unlock Value

The stronger long-horizon formulation is retained for future work. After collecting enough intervention data across agents, checkpoints, skills, and environments, an uncertainty-aware neural predictor may estimate:

```text
developmental state + candidate skill + short intervention signature
→ long-horizon competence expansion
```

This predictor is deferred because the first study cannot yet produce a sufficiently large and diverse supervised intervention dataset. It remains a planned upgrade rather than a rejected idea.

## Scope boundary

The first full study is single-agent and compute-aware. Open goal-space expansion, persistent self-models, selective autobiographical memory, identity continuity, and multi-agent developmental role allocation are later research stages.

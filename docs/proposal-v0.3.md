# Learning What to Learn Next
## Sparse Intervention-Calibrated Developmental Leverage for Autonomous Curriculum Learning

*Research Proposal v0.3 — implementation-focused public version*

## One-sentence pitch

> Do not ask where an agent currently fails most. Ask which currently learnable skill is most likely to expand the rest of its competence — and estimate that value using a cheap transfer signal calibrated by sparse real interventions.

## Long-term vision

The broader Developmental Agency programme seeks agents that maintain persistent self-models, identify competence bottlenecks, generate endogenous goals, arbitrate among developmental directions, selectively consolidate experience, expand capabilities, and preserve continuity while changing.

This first paper isolates one falsifiable component:

> How should an agent allocate its next training budget when different currently learnable skills have different downstream effects on unresolved competence?

## Gap

Difficulty, novelty, regret, learning progress, prerequisite graphs, and foundation-model priors provide useful curriculum signals, but they do not directly estimate which training choice is most likely to improve the largest amount of competence the current agent still lacks.

The intended gap is:

> Low-cost estimation of agent- and stage-specific cross-skill developmental leverage.

## Formal setup

Let:

- `S = {s_1, ..., s_n}` be predefined achievement goals;
- `π_θ(a | o, g)` be a goal-conditioned policy;
- `c_t[j]` be competence on goal `j`;
- `f_t[i]` be feasibility of training goal `i` now;
- `T_t[i,j]` be estimated transfer from training `i` to competence `j`.

The candidate frontier contains unresolved but currently learnable goals.

## Two structures

### Environment affordance structure

What the world makes physically or procedurally reachable. A known Craftax achievement tree belongs here and may be used only as an evaluation reference.

### Agent-specific competence-transfer structure

How training one capability changes the current agent's other capabilities. This structure may differ between agents and change across checkpoints.

The paper studies the second structure.

## Developmental Leverage Score

```text
DLS_t(i) = feasibility_t(i)
           × Σ_j weight_j
           × positive_transfer_t(i → j)
           × (1 - competence_t(j))
```

A capability has high leverage when it is currently trainable, transfers to several unresolved capabilities, and does not merely improve skills that are already mastered.

The selected goal is the feasible skill with maximal DLS.

## Low-cost transfer proxy

The preferred first implementation uses compact goal-conditioned gradient sketches:

```text
P_t(i,j) = cosine(gradient_sketch_i, gradient_sketch_j)
```

Aligned gradients are treated as a candidate signal of positive transfer; conflicting gradients suggest interference. Only selected shared network layers are sketched.

If gradient affinity is unstable, one alternative proxy will be tested at a time, such as historical competence co-improvement or representation similarity.

## Sparse intervention calibration

The proxy is not assumed to be correct by itself.

At a small number of predetermined checkpoints:

1. choose 2–4 informative frontier skills;
2. restore the same saved checkpoint sequentially;
3. micro-train one branch per candidate plus a matched control;
4. evaluate relevant goals with common seeds;
5. measure empirical cross-skill transfer;
6. fit a low-parameter calibration model.

Candidate calibrators include ridge regression, Bayesian linear regression, isotonic calibration, and linear UCB.

The normal online loop remains cheap. Exhaustive branching at every developmental epoch is not part of the first-paper method.

## Main hypotheses

- **H1:** calibrated proxy estimates predict measured transfer better than difficulty, novelty, failure, immediate learning progress, graph centrality, and raw gradient affinity.
- **H2:** DLS-guided training improves competence coverage or developmental regret under a fixed total budget that includes probes and evaluation.
- **H3:** a small number of sparse interventions materially improves transfer prediction.
- **H4:** dynamic agent-conditioned transfer outperforms a static population-average matrix.
- **H5:** the leverage of the same skill changes across developmental checkpoints.

## Environments

### Stage A — dependency-control environment

A lightweight domain with known shared subskills and inexpensive exhaustive transfer measurement.

### Stage B — Craftax-Classic-Symbolic

Primary practical benchmark for the first paper.

### Optional Stage C — full Craftax-Symbolic

Attempted only after the mechanism and baseline matrix are stable.

## Required baselines

- vanilla PPO;
- random frontier;
- fixed curriculum;
- feasibility-only;
- novelty-driven;
- learning progress;
- graph centrality × feasibility;
- raw proxy DLS;
- static transfer DLS;
- calibrated dynamic DLS.

A sparse intervention oracle may be reported as an upper bound.

## Four core experiments

1. **Transfer validity:** does the cheap proxy predict measured cross-skill transfer?
2. **Calibration value:** do sparse real interventions improve transfer ranking?
3. **Curriculum performance:** does DLS improve competence under a matched total budget?
4. **Agent and stage specificity:** do transfer structures differ across agents and checkpoints?

## Metrics

- hard and soft competence coverage;
- area under the competence-coverage curve;
- total interactions including probes;
- GPU hours and wall-clock cost;
- Spearman and Kendall transfer-ranking correlation;
- top-k selection accuracy;
- developmental regret;
- cost–accuracy frontier.

## Failure criteria

The central claim fails if the proxy does not predict measured transfer, calibration adds no information, gains disappear after probe costs are counted, or a static transfer matrix matches the dynamic method.

Negative results remain useful if they establish a careful transfer benchmark or reveal limits of cheap developmental signals.

## Current implementation boundary

The public code currently implements only a transparent dependency-free DLS selector and test suite. It does not yet claim Craftax integration, validated gradient proxies, or improved curriculum results.

## Long-term Phase II — neural Counterfactual Unlock Value

After accumulating enough intervention data across agents, checkpoints, skills, and environments, train an uncertainty-aware neural predictor:

```text
developmental state + candidate skill + short intervention signature
→ long-horizon competence expansion
```

This model may use recurrent developmental histories, uncertainty prediction, hierarchical priors, offline intervention replay, cross-agent meta-learning, and active probe selection.

The neural predictor is deferred for data and compute reasons, not rejected conceptually.

## Longer-term phases

- open goal-space expansion;
- autonomous capability decomposition and tool creation;
- persistent developmental self-model;
- selective autobiographical memory;
- continuity-constrained self-modification;
- multi-agent developmental role allocation.

## Final intended claim

If the experiments succeed:

> An agent can use a low-cost, dynamically estimated cross-skill transfer signal — calibrated by a small number of real learning interventions — to select currently learnable skills that expand unresolved competence more effectively than difficulty-, novelty-, progress-, or static-graph-based curricula under a fixed total budget.

This is not yet a digital life. It is a feasible first mechanism through which an artificial agent begins to choose its own direction of capability development.

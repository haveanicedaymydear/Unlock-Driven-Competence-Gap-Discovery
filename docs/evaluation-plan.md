# Evaluation Plan v0.3

## Objective

Evaluate whether a low-cost, agent- and stage-specific cross-skill transfer estimate can improve curriculum decisions after all probe interactions and compute costs are counted.

## Environments

### Dependency-control environment

Used to verify that the transfer proxy can recover known positive and negative transfer and to distinguish transfer from simple temporal co-occurrence.

### Craftax-Classic-Symbolic

Primary practical benchmark for the first paper.

### Full Craftax-Symbolic

Optional extension after the mechanism is stable.

## Experimental conditions

1. Vanilla PPO.
2. Random frontier selection.
3. Fixed human curriculum.
4. Feasibility-only curriculum.
5. Novelty-driven curriculum.
6. Learning-progress curriculum.
7. Graph centrality × feasibility.
8. Raw transfer-proxy DLS.
9. Static population-transfer DLS.
10. Calibrated dynamic DLS.
11. Sparse intervention oracle as an optional upper bound.

## Competence protocol

For every achievement goal:

- condition the policy on that goal;
- evaluate with a fixed episode budget;
- reuse common random seeds across compared branches;
- report success probability and uncertainty;
- optionally report time-to-achievement and partial progress.

The same evaluator is used for frontier construction, sparse-probe measurement, and final reporting.

## Sparse calibration protocol

At predetermined checkpoints, such as 10%, 30%, 55%, and 80% of training:

1. choose 2–4 informative frontier skills;
2. compute the low-cost transfer proxy before intervention;
3. sequentially restore the same checkpoint for each candidate;
4. micro-train each candidate for the same probe budget;
5. run a matched control branch;
6. evaluate relevant goals with common seeds;
7. calculate empirical transfer relative to control;
8. update the lightweight calibrator.

The exact checkpoint schedule, candidate count, probe budget, and evaluation budget are fixed before the main comparison.

## Core experiments

### Experiment 1 — transfer-prediction validity

Compare proxy predictions with measured sparse intervention effects.

Metrics:

- Spearman rank correlation;
- Kendall rank correlation;
- top-1 and top-k ranking accuracy;
- mean absolute error;
- positive/negative transfer sign accuracy.

### Experiment 2 — value of sparse calibration

Compare:

- raw proxy;
- static calibration;
- dynamic calibration;
- simple difficulty, feasibility, and learning-progress signals.

### Experiment 3 — curriculum performance

Compare all required curricula under matched total interaction budgets.

All of the following are counted:

- main training interactions;
- calibration-probe interactions;
- competence-evaluation interactions;
- GPU hours and wall-clock time.

### Experiment 4 — agent and stage specificity

Compare:

- different seeds at the same checkpoint;
- the same agent across checkpoints;
- dynamic estimates with a static population-average transfer matrix.

## Primary metrics

### Competence coverage

Report hard achievement count, soft coverage, and area under the competence-coverage curve.

### Total-budget efficiency

Report interactions required to reach coverage thresholds, with all probe and evaluation interactions included.

### Compute-normalized performance

Report competence coverage per GPU hour and final wall-clock cost.

### Developmental regret

At calibration checkpoints, compare the selected skill with the best measured candidate intervention:

```text
regret_t = measured_value(best candidate) - measured_value(selected candidate)
```

### Cost–accuracy frontier

Vary:

- number of calibration checkpoints;
- number of probed candidates;
- probe length.

Plot prediction quality and final competence against total cost.

## Required ablations

- no feasibility term;
- no unresolved-competence weighting;
- raw proxy without calibration;
- static transfer instead of dynamic transfer;
- immediate self-skill progress instead of cross-skill transfer;
- shuffled calibration labels;
- fewer calibration checkpoints;
- fewer probed candidates;
- exclude negative transfer.

Only the most informative ablations will be scaled to all seeds.

## Failure criteria

The central claim fails if:

1. the proxy does not predict measured transfer above simple baselines;
2. sparse calibration does not improve held-out transfer ranking;
3. curriculum gains disappear when probe costs are counted;
4. a static transfer matrix performs as well as the dynamic estimate;
5. gradient affinity merely tracks difficulty or training stage;
6. transfer estimates are too noisy for stable ranking;
7. the method improves only easy achievements without extending the frontier.

Negative results remain publishable evidence if they establish a careful benchmark or reveal limits of low-cost transfer prediction.

## Statistical reporting

- use multiple independent seeds for final methods;
- report confidence intervals rather than a single best run;
- preserve failed runs and unstable transfer estimates;
- disclose all probe and evaluation budgets;
- add numerical claims to the README and CV only after corresponding logs and artifacts are public.

## Future boundary

Controlled developmental divergence, revisability after environmental shift, full Craftax replication, neural long-horizon CUV prediction, open goal invention, and multi-agent developmental allocation are later extensions rather than first-paper requirements.

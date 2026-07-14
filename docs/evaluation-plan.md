# Evaluation Plan

## Environment

The intended environment is Craftax or a comparable long-horizon achievement environment with latent prerequisite structure. The agent will not receive the ground-truth achievement tree during learning.

## Experimental conditions

1. Random frontier selection.
2. Novelty-driven curriculum.
3. Learning-progress curriculum.
4. Failure- or regret-driven curriculum.
5. Unlock-driven competence-gap discovery.
6. Oracle prerequisite tree, used only as an upper-bound reference.

## Evaluation protocol

- Use the same environment seeds and interaction budget across curriculum conditions.
- Separate graph inference, frontier selection, and policy-learning components in ablations.
- Prevent the ground-truth achievement tree from entering training or frontier scoring.
- Report results across multiple seeds rather than a single successful trajectory.
- Preserve failed runs and early graph errors for qualitative analysis.

## Primary metrics

### Achievement coverage

The number and proportion of distinct achievements reached under a fixed interaction budget.

### Sample efficiency

Environment interactions required to reach predefined achievement milestones.

### Learned-graph fidelity

After training only, compare inferred prerequisite edges with the hidden evaluation graph using precision, recall, F1, and reachability agreement.

### Developmental-stage structure

Test whether groups of competencies emerge in stable temporal stages rather than as an arbitrary acquisition sequence.

### Trajectory divergence

Measure how different early observations or successes change later competence selection and final achievement coverage.

### Recovery from graph error

Inject or identify incorrect early dependencies and measure how quickly later evidence changes frontier ranking.

## Ablations

- unlock potential only;
- feasibility only;
- product of unlock potential and feasibility;
- no uncertainty or confidence weighting on inferred edges;
- frozen graph versus continually revised graph;
- one-step downstream count versus transitive reachability.

## Statistical reporting

The planned report will include means and uncertainty intervals across seeds, per-achievement success rates, learning curves, graph-quality trajectories, and manual error categories. Numerical claims will not be added to the CV or README before corresponding logs and result artifacts are public.

## Multi-agent boundary

A future team-level study may replace individual future reachability with joint team reachability and examine role-specialised competence acquisition. That extension is not part of the current single-agent evaluation claim.

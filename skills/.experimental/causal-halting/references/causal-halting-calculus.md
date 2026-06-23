---
layout: page
title: Causal Halting Calculus
---

# Causal Halting: Diagonalization as Forbidden Prediction Feedback

## Abstract

The classical Halting Problem states that no Turing-computable total procedure can decide, for every program and input, whether the program halts. The standard diagonal proof constructs a program that queries a hypothetical halting predictor about its own execution and then inverts the predictor's answer.

This note isolates the information-flow assumption used by that construction. Classical diagonalization requires unrestricted prediction feedback: the output of a halting observation may causally influence the very execution being observed. We define a minimal calculus, CHC-0, in which such feedback is rejected by the type system. In CHC-0, the diagonal computation is not merely undecidable; it is causally ill-typed.

This is not a solution to the classical Halting Problem. Ordinary semantic undecidability remains, as shown by standard H-free object-language programs. The contribution is a separation: causal paradox and semantic unprovability are distinct failure modes. The former is a decidable structural property of a causal dependency graph. The latter is relative to the strength of the proof system used to reason about program behavior.

Implementation status, v4.0: the CHC-0 core described here is implemented by the checker. The repository also includes operational, conservative extensions for CHC-1 through CHC-5: recursive effect summaries, higher-order effect annotations, process/session non-interference, temporal trace analysis, and probabilistic prediction feedback. Those extensions are practical verifiers over structured artifacts, not claims to decide arbitrary termination.

## 1. Introduction

The classical diagonal argument assumes that programs, program descriptions, observations, and the use of observational results all inhabit one unrestricted computational universe. This allows a program to ask whether its own execution halts and then choose behavior that contradicts the answer.

CHC-0 separates these roles.

```text
Code        inert program description
Exec        live execution event
H           halting observation operator
HaltResult  causal token produced by observation
```

The central restriction is:

```text
HaltResult is not ordinary data.
```

It cannot be passed into opaque code, stored as an ordinary value, or passed across CHC function boundaries. It may be discarded, or it may be eliminated by a dedicated halting-branch rule. That elimination records a causal edge from the observation result to the current execution.

The guiding claim is:

```text
Diagonalization is prediction feedback. Prediction feedback can be typed.
```

## 2. Informal Picture

The forbidden pattern is:

```text
Exec(P, X) -> HaltResult(P, X) -> Exec(P, X)
```

The first edge means that a halting result observes an execution. The second means that the result controls that same execution. CHC-0 rejects this cycle.

This does not make all halting questions decidable. It only identifies a special structural failure mode: prediction feedback into the predicted execution.

## 3. CHC-0 Restrictions

CHC-0 is deliberately small. The restrictions are part of the model, not implementation details.

```text
No eval.
No runtime code generation.
No higher-order code.
No recursion in CHC-defined code.
CHC function definitions form an acyclic call graph.
L0 programs are opaque, H-free, and may be Turing-complete.
HaltResult is not a subtype of Val.
HaltResult cannot be a function parameter.
HaltResult has one introduction form: OBS.
HaltResult has one elimination form: H-BRANCH.
```

The object language `L0` supplies ordinary Turing-complete programs. CHC-0 wraps `L0` with a causal halting observation operator `H`. L0 programs may be recursive and arbitrarily complex; their internals are opaque to the causal type checker and contribute no causal graph edges.

## 4. Types and Causal Nodes

Types:

```text
Val              ordinary values
Code <: Val      program descriptions
Bool <: Val      ordinary booleans
HaltResult(p,a)  causal token, not a subtype of Val
Comp             computations
```

Causal graph nodes:

```text
E(p,a)   execution of program p on argument a
R(p,a)   halting result produced by observing E(p,a)
```

Typing judgment:

```text
Gamma ; self=e |- M : tau => G
```

Read: under context `Gamma` and current execution root `e`, term `M` has type `tau` and generates causal graph `G`. The graph `G` is a finite directed graph over `E` and `R` nodes with first-order symbolic labels.

## 5. Inference Rules

Base computations:

```text
HALT
------------------------------------------------
Gamma ; self=e |- halt : Comp => empty

LOOP
------------------------------------------------
Gamma ; self=e |- loop : Comp => empty
```

Observation, the only introduction form for `HaltResult`:

```text
OBS
Gamma |- p : Code
Gamma |- a : Val
------------------------------------------------
Gamma ; self=e |- H(p,a) : HaltResult(p,a)
  => { E(p,a) -> R(p,a) }
```

Halting-result branch, the only elimination form for `HaltResult`:

```text
H-BRANCH
Gamma |- r : HaltResult(p,a)
Gamma ; self=e |- M : Comp => G1
Gamma ; self=e |- N : Comp => G2
------------------------------------------------
Gamma ; self=e |- if r then M else N : Comp
  => G1 union G2 union { R(p,a) -> e }
```

The edge `R(p,a) -> e` records that the current execution's control flow depends on the halting result.

Ordinary data branch:

```text
DATA-BRANCH
Gamma |- v : Bool
Gamma ; self=e |- M : Comp => G1
Gamma ; self=e |- N : Comp => G2
------------------------------------------------
Gamma ; self=e |- if v then M else N : Comp
  => G1 union G2
```

No causal edge is generated by an ordinary boolean branch.

Let binding:

```text
LET
Gamma ; self=e |- A : sigma => G0
Gamma, r:sigma ; self=e |- M : Comp => G1
------------------------------------------------
Gamma ; self=e |- let r = A in M : Comp
  => G0 union G1
```

If `sigma = HaltResult(p,a)`, binding alone creates no feedback edge. The edge `R(p,a) -> e` appears only when the result is eliminated by `H-BRANCH`.

Opaque object-language call:

```text
CALL-L0
Def(f) in L0
Gamma |- a : Val
------------------------------------------------
Gamma ; self=e |- f(a) : Comp => empty
```

Side conditions: `L0` is H-free, has no callbacks into CHC, and accepts no `HaltResult`. The premise `a : Val` excludes `HaltResult` because `HaltResult` is not a subtype of `Val`.

CHC call by non-recursive inlining:

```text
CALL-INLINE
Def(f) = lambda y. Mf
f in CHC
Gamma |- a : Val
Gamma ; self=e |- Mf[y := a] : Comp => G
------------------------------------------------
Gamma ; self=e |- f(a) : Comp => G
```

Closed CHC execution validity:

```text
RUN-CHC
Def(f) = lambda y. Mf
Gamma ; self=E(f,a) |- Mf[y := a] : Comp => G
acyclic_unif(G)
------------------------------------------------
Gamma |- run f(a) valid => G
```

Closed L0 execution validity:

```text
RUN-L0
Def(f) in L0
Gamma |- a : Val
------------------------------------------------
Gamma |- run f(a) valid => empty
```

`RUN-L0` is needed because L0 supplies the ordinary Turing-complete programs used in the undecidability reduction. L0 programs are causally valid because they contain no CHC halting observations.

## 6. Causal Validity

Define `acyclic_unif(G)` as follows.

`acyclic_unif(G)` holds iff there is no nonempty directed path:

```text
E(s,t) ->+ E(u,v)
```

in `G` such that the label pairs `(s,t)` and `(u,v)` are unifiable under first-order unification.

Equivalently:

```text
causal_paradox(G)
  iff exists E-nodes n1,n2 such that:
       reachable+(n1,n2)
       and label(n1), label(n2) are first-order unifiable.
```

Thus:

```text
acyclic_unif(G) iff not causal_paradox(G)
```

The use of unification matters. `Code` ranges over infinitely many closed programs, so CHC-0 does not enumerate substitutions. Instead, it asks whether some substitution could turn a symbolic feedback path into a cycle. For first-order symbolic labels, that existential question is decidable by unification.

## 7. Decidability of Causal Validity

**Lemma.** For CHC-0 programs satisfying the restrictions in Section 3, causal validity is decidable.

**Proof.**

1. CHC-defined functions form an acyclic call graph. Therefore `CALL-INLINE` terminates by induction on the call graph.
2. L0 calls are opaque by `CALL-L0` and contribute the empty graph.
3. `HaltResult` is not a subtype of `Val` and cannot be a function parameter. Therefore a halting result cannot enter L0 or cross CHC call boundaries, so causal edges cannot be hidden inside opaque calls or separate functions.
4. Consequently, every closed CHC-0 execution produces a finite symbolic graph `G`.
5. Because `G` is finite, the set of E-node pairs in `G` is finite. Compute the finite reachability relation over `G`.
6. For each reachable pair of E-nodes, first-order unification of their labels is decidable.
7. Therefore `acyclic_unif(G)` is decidable.

QED.

## 8. Diagonalization Is Ill-Typed

**Theorem 1.** The diagonal computation `D(D)` is not a valid CHC-0 computation.

Define:

```text
D(y) =
  let r = H(y,y) in
  if r then loop else halt
```

Typing the body of `D(y)` with current execution root `self = E(D,y)` generates:

```text
OBS on H(y,y):       E(y,y) -> R(y,y)
H-BRANCH on r:       R(y,y) -> E(D,y)
```

So:

```text
G_D(y) = { E(y,y) -> R(y,y), R(y,y) -> E(D,y) }
```

For generic `y`, this graph has no literal syntactic cycle. However, it contains a unifiable feedback path:

```text
E(y,y) ->+ E(D,y)
```

The endpoint labels unify under:

```text
y |-> D
```

Thus `D` may be syntactically definable, but it is not valid as a total function over all `Code` inputs.

Now consider the closed execution:

```text
run D(D)
```

`RUN-CHC` sets:

```text
self = E(D,D)
```

and substitutes `y := D`, yielding:

```text
G = { E(D,D) -> R(D,D), R(D,D) -> E(D,D) }
```

There is a nonempty path from `E(D,D)` to itself. The endpoint labels unify trivially. Therefore:

```text
acyclic_unif(G) fails
```

So `run D(D)` is rejected by `RUN-CHC`. Classical diagonalization fails because it requires `H(D,D)` to be a valid observation inside `D(D)`, and that observation completes a prediction-feedback cycle.

QED.

## 9. Semantic Undecidability Survives

**Theorem 2.** No CHC-0 analyzer can decide `halts/diverges` for all causally valid programs.

Let `e` be any L0 program. Define an H-free L0 program:

```text
Q_e() =
  simulate e(e)
  if e(e) halts, halt
  else diverge
```

`Q_e` uses no CHC halting observation `H`. Therefore it generates no `R` nodes and contributes no causal edges:

```text
G = empty
```

By `RUN-L0`, `Q_e` is a valid causally acyclic program.

Suppose an analyzer `A` decided `halts/diverges` for every causally valid CHC-0 execution. Applying `A` to `Q_e` would decide whether `Q_e` halts. But:

```text
Q_e halts iff e(e) halts
```

Therefore `A` would decide the classical Halting Problem. Contradiction.

QED.

## 10. Boundary Stability

**Theorem 3.** `CausalParadox` and `Unproved` are distinct failure modes with different stability properties.

For a fixed CHC-0 type system, define:

```text
CausalParadox(P) iff not acyclic_unif(G_P)
```

where `G_P` is the causal graph generated by typing `P`.

For a sound proof system `S`, define:

```text
Unproved_S(P)
  iff acyclic_unif(G_P)
      and S proves neither halts(P) nor diverges(P)
```

Then:

```text
CausalParadox(P)
```

depends only on the CHC-0 type rules and the generated symbolic graph. It is independent of the proof system used for semantic termination reasoning.

If `S2` is a sound extension of `S1`, then:

```text
Unproved_S2 subseteq Unproved_S1
```

because any termination fact proved by `S1` is also available to `S2`, while `S2` may prove more. Stronger proof systems can shrink the unproved set. They do not change the causal paradox set.

QED.

## 11. Summary

| Property | CausalParadox | Unproved |
|---|---|---|
| Source | Prediction-feedback cycle in `G` | Semantic complexity of L0 behavior |
| Detection | Decidable by finite reachability plus unification | Undecidable in general |
| Proof-system relative | No | Yes |
| Example | `D(D)` | `Q_e` |
| CHC-0 response | Type error at `RUN-CHC` | `unproved` or analyzer failure |

The contribution in one sentence:

```text
CHC-0 shows that the classical diagonal construction relies on unrestricted prediction feedback; once that feedback is made explicit and typed, the diagonal becomes causally ill-formed while ordinary undecidability remains.
```

## 12. What This Does Not Claim

CHC-0 does not decide the classical Halting Problem.

CHC-0 does not eliminate undecidability.

CHC-0 does not claim quantum computation, analog computation, or hypercomputation.

CHC-0 does not show that all self-reference is invalid.

The claim is narrower:

```text
The classical diagonal proof uses a prediction-feedback loop.
CHC-0 makes that loop visible as a causal graph cycle.
The type system rejects that cycle.
Semantic undecidability remains in causally valid programs.
```

## 13. Related Work

**Infinite Time Turing Machines** (Hamkins and Lewis, 2000): allow ordinal time and decide the classical halting problem, but generate a new halting problem at the transfinite level. CHC-0 takes the opposite route: it restricts feedback rather than expanding computation.

**Non-interference** (Goguen and Meseguer, 1982): studies information-flow policies that prevent one class of outputs from influencing another class of inputs. CHC-0 applies an analogous policy to prediction and execution.

**Propositions as Sessions / Linear Logic** (Wadler, 2014): uses type structure to control communication and resource flow. In CHC-0, `HaltResult` is non-passable and has restricted elimination. A fully linear extension would additionally make `HaltResult` non-copyable.

**Categorical process theory and no-cloning** (Abramsky, 2009): model causal structure and resource constraints in process-theoretic terms. CHC-0's E/R graph is a minimal causal dependency structure in this spirit.

**Quantum measurement protocols** (Ozawa, 1998): separate a measured process, a measurement event, and a classical outcome. CHC-0 uses a computational analogue: observation results may control later computation, but not the execution being observed.

## 14. Implementation Status v4.0

The implemented package contains six operational layers.

```text
CHC-0  finite first-order causal graph checking
CHC-1  recursion through conservative causal effect summaries
CHC-2  higher-order calls through explicit effect annotations
CHC-3  process/session non-interference over ProcessIR
CHC-4  temporal trace analysis over happens-before/event identity
CHC-5  probabilistic PredictionResult feedback
```

The common output boundary is:

```json
{
  "validity_scope": "no_modeled_prediction_feedback_only"
}
```

Thus `valid_acyclic` means only that no modeled prediction-feedback cycle was detected. It does not mean the program terminates, the agent is safe, the trace is complete, or the system is correct.

The implementation also emits identity-resolution metadata:

```json
{
  "resolved": [],
  "ambiguous": [],
  "missing": [],
  "conflicts": [],
  "assumptions": []
}
```

For production-style artifacts, ambiguous execution/result/channel/prediction identity is classified as `insufficient_info`, not `valid_acyclic`.

### CHC-1: Recursive Effect Summaries

CHC-1 adds recursive CHC definitions with causal effect summaries as fixed points:

```text
G_f = body_graph(f, G_f)
```

Operationally, the checker computes summaries by finite iteration over symbolic causal edges. If the summary stabilizes, the resulting graph is analyzed with `acyclic_unif`. If it does not stabilize within the configured bound, the checker returns `insufficient_info`.

This is conservative. Some causally safe recursive programs may be rejected, but non-convergence is not accepted as `valid_acyclic`.

### CHC-2: Higher-Order Effects

CHC-2 adds controlled higher-order code with explicit causal effect annotations:

```text
f : A -> B ! Eff
```

Callback effects are composed into the caller's graph before `acyclic_unif` runs. Missing or incomplete effect annotations return `insufficient_info`. `HaltResult` still cannot be hidden inside callbacks or passed as an ordinary value.

### CHC-3: Process and Session Non-Interference

CHC-3 analyzes structured `ProcessIR` artifacts. It separates:

```text
process identity
session identity
execution identity
result identity
control channel identity
```

The core rule is:

```text
an observation result for E must not flow into a control channel for E before E ends
```

The analyzer detects direct and modeled multi-hop routes through channels/controllers. Missing or ambiguous identity returns `insufficient_info`.

### CHC-4: Temporal Trace Semantics

CHC-4 analyzes JSONL traces with temporal metadata:

```text
exec_start
observe
consume
control_exec
exec_end
```

It builds a happens-before relation from explicit `happens_before`, span parent links, logical clocks, and safe timestamp order. Same-execution consumption before `exec_end` is rejected. Post-run audit and future-run control are accepted when the trace exposes enough identity and temporal order.

### CHC-5: Probabilistic PredictionResult

CHC-5 generalizes `HaltResult` to broader prediction results:

```text
halt_prediction
failure_risk
confidence_score
budget_prediction
quality_prediction
bounded_progress_metric
```

The confidence value is not used for classification. The structural rule remains:

```text
prediction_about(E) -> PredictionResult -> control(E)
```

Bounded local progress metrics are accepted only when scoped as local progress metrics rather than predictions about the outcome of the current execution.

### Lean Track

The repository includes a Lean 4 proof track for the core structural invariants:

```text
CHC-0  finite graph/reachability core and diagonal rejection
CHC-1  conservative effect-summary status
CHC-2  effect annotation and callback composition
CHC-3  process/session non-interference core
CHC-4  temporal pre-end feedback rule
CHC-5  prediction-confidence irrelevance
```

This Lean track does not mechanize arbitrary halting, the `Q_e` semantic reduction, or every parser/adapter detail. It mechanizes the structural boundaries enforced by the tool.

## 15. Remaining Research Work

The main open problem remains:

```text
Characterize the boundary between causal paradox and semantic unprovability
for increasingly expressive causal calculi.
```

The practical tool already detects and repairs modeled prediction-feedback in structured artifacts. The deeper theory work is to connect those operational checks to stronger mechanized soundness theorems, especially for recursive and higher-order calculi.

The maximum claim stays narrow:

```text
CHC detects modeled prediction-feedback structure.
CHC does not decide arbitrary halting.
CHC does not solve the classical Halting Problem.
```

## Appendix: Rule Reference

```text
HALT
  Gamma ; self=e |- halt : Comp => empty

LOOP
  Gamma ; self=e |- loop : Comp => empty

OBS
  Gamma |- p : Code
  Gamma |- a : Val
  ------------------------------------------------
  Gamma ; self=e |- H(p,a) : HaltResult(p,a)
    => { E(p,a) -> R(p,a) }

H-BRANCH
  Gamma |- r : HaltResult(p,a)
  Gamma ; self=e |- M : Comp => G1
  Gamma ; self=e |- N : Comp => G2
  ------------------------------------------------
  Gamma ; self=e |- if r then M else N : Comp
    => G1 union G2 union { R(p,a) -> e }

DATA-BRANCH
  Gamma |- v : Bool
  Gamma ; self=e |- M : Comp => G1
  Gamma ; self=e |- N : Comp => G2
  ------------------------------------------------
  Gamma ; self=e |- if v then M else N : Comp
    => G1 union G2

LET
  Gamma ; self=e |- A : sigma => G0
  Gamma, r:sigma ; self=e |- M : Comp => G1
  ------------------------------------------------
  Gamma ; self=e |- let r = A in M : Comp
    => G0 union G1

CALL-L0
  Def(f) in L0
  Gamma |- a : Val
  ------------------------------------------------
  Gamma ; self=e |- f(a) : Comp => empty

CALL-INLINE
  Def(f) = lambda y. Mf
  f in CHC
  Gamma |- a : Val
  Gamma ; self=e |- Mf[y := a] : Comp => G
  ------------------------------------------------
  Gamma ; self=e |- f(a) : Comp => G

RUN-CHC
  Def(f) = lambda y. Mf
  Gamma ; self=E(f,a) |- Mf[y := a] : Comp => G
  acyclic_unif(G)
  ------------------------------------------------
  Gamma |- run f(a) valid => G

RUN-L0
  Def(f) in L0
  Gamma |- a : Val
  ------------------------------------------------
  Gamma |- run f(a) valid => empty
```

`acyclic_unif(G)`: no nonempty path `E(s,t) ->+ E(u,v)` in `G` where `(s,t)` and `(u,v)` are first-order unifiable.

#!/usr/bin/env python3
"""Operational CHC-0/CHC-1/CHC-2 causal checker.

The checker has two surfaces:

* Graph DSL: explicit E/R edges and first-order unification.
* Mini-CHC v2: a small structured syntax for CHC expressions.

It does not decide arbitrary halting. It only generates causal effects and
checks whether an observation/prediction result can feed back into the observed
execution.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


MAX_EFFECT_ITERATIONS = 32

CAPABILITY_BOUNDARY = {
    "does_not_prove_arbitrary_termination": True,
    "does_not_solve_classical_halting": True,
}
VALIDITY_SCOPE = "no_modeled_prediction_feedback_only"


def default_identity_resolution() -> dict[str, list[object]]:
    return {
        "resolved": [],
        "ambiguous": [],
        "missing": [],
        "conflicts": [],
        "assumptions": ["Mini-CHC and graph DSL identities are symbolic labels supplied by the artifact."],
    }


def default_theorem_coverage(chc_level: str) -> dict[str, object]:
    return {
        "chc_level": chc_level,
        "mechanized_core": "CHC-0" if chc_level == "CHC-0" else "partial",
        "claims": [
            "finite modeled graph feedback detection",
            "diagonal rejection for modeled CHC-0 feedback",
        ],
    }


@dataclass(frozen=True)
class Term:
    name: str
    args: tuple["Term", ...] = ()

    @property
    def is_var(self) -> bool:
        return not self.args and bool(re.match(r"^[a-z][A-Za-z0-9_]*$", self.name))

    def substitute(self, mapping: dict[str, "Term"]) -> "Term":
        if self.is_var and self.name in mapping:
            return mapping[self.name]
        if not self.args:
            return self
        return Term(self.name, tuple(arg.substitute(mapping) for arg in self.args))

    def to_string(self) -> str:
        if not self.args:
            return self.name
        return f"{self.name}({','.join(arg.to_string() for arg in self.args)})"


@dataclass(frozen=True)
class Node:
    kind: str
    left: Term
    right: Term

    def substitute(self, mapping: dict[str, Term]) -> "Node":
        return Node(self.kind, self.left.substitute(mapping), self.right.substitute(mapping))

    def to_string(self) -> str:
        return f"{self.kind}({self.left.to_string()},{self.right.to_string()})"


@dataclass(frozen=True)
class Edge:
    source: Node
    target: Node

    def substitute(self, mapping: dict[str, Term]) -> "Edge":
        return Edge(self.source.substitute(mapping), self.target.substitute(mapping))

    def to_string(self) -> str:
        return f"{self.source.to_string()} -> {self.target.to_string()}"


@dataclass(frozen=True)
class Param:
    name: str
    effect: str | None = None

    @property
    def is_function(self) -> bool:
        return self.effect is not None


@dataclass(frozen=True)
class FunctionDef:
    name: str
    params: tuple[Param, ...]
    body: str


@dataclass(frozen=True)
class FunctionValue:
    name: str
    effect: str | None = None


@dataclass(frozen=True)
class TypeValue:
    kind: str
    halt_terms: tuple[Term, Term] | None = None
    function: FunctionValue | None = None
    term: Term | None = None


@dataclass
class EffectResult:
    edges: list[Edge] = field(default_factory=list)
    value: TypeValue = field(default_factory=lambda: TypeValue("Comp"))
    semantic_status: str = "unproved"
    higher_order_effects: list[dict[str, str]] = field(default_factory=list)
    incomplete_higher_order: bool = False

    def extend(self, other: "EffectResult") -> None:
        self.edges = dedupe_edges(self.edges + other.edges)
        if other.semantic_status == "not_analyzed":
            self.semantic_status = "not_analyzed"
        self.higher_order_effects.extend(other.higher_order_effects)
        self.incomplete_higher_order = self.incomplete_higher_order or other.incomplete_higher_order


class ParseError(ValueError):
    pass


class InsufficientInfo(ValueError):
    pass


class TermParser:
    def __init__(self, text: str):
        self.text = text
        self.index = 0

    def parse_term(self) -> Term:
        self._skip_ws()
        name = self._parse_identifier()
        self._skip_ws()
        if self._peek() != "(":
            return Term(name)

        self.index += 1
        args: list[Term] = []
        self._skip_ws()
        if self._peek() == ")":
            self.index += 1
            return Term(name, ())

        while True:
            args.append(self.parse_term())
            self._skip_ws()
            char = self._peek()
            if char == ",":
                self.index += 1
                continue
            if char == ")":
                self.index += 1
                break
            raise ParseError(f"Expected ',' or ')' at offset {self.index} in {self.text!r}.")
        return Term(name, tuple(args))

    def require_end(self) -> None:
        self._skip_ws()
        if self.index != len(self.text):
            raise ParseError(f"Unexpected text at offset {self.index}: {self.text[self.index:]!r}.")

    def _parse_identifier(self) -> str:
        match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", self.text[self.index :])
        if not match:
            raise ParseError(f"Expected identifier at offset {self.index} in {self.text!r}.")
        self.index += len(match.group(0))
        return match.group(0)

    def _peek(self) -> str:
        if self.index >= len(self.text):
            return ""
        return self.text[self.index]

    def _skip_ws(self) -> None:
        while self.index < len(self.text) and self.text[self.index].isspace():
            self.index += 1


def parse_term(text: str) -> Term:
    parser = TermParser(text)
    term = parser.parse_term()
    parser.require_end()
    return term


def split_top_level_pair(text: str) -> tuple[str, str]:
    parts = split_top_level(text, ",", maxsplit=1)
    if len(parts) != 2:
        raise ParseError(f"Expected a top-level comma in {text!r}.")
    return parts[0], parts[1]


def split_top_level(text: str, delimiter: str, maxsplit: int = -1) -> list[str]:
    depth = 0
    parts: list[str] = []
    start = 0
    splits = 0
    index = 0
    while index < len(text):
        char = text[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif depth == 0 and text.startswith(delimiter, index):
            parts.append(text[start:index].strip())
            index += len(delimiter)
            start = index
            splits += 1
            if maxsplit >= 0 and splits >= maxsplit:
                break
            continue
        index += 1
    parts.append(text[start:].strip())
    return parts


def find_keyword_top_level(text: str, keyword: str) -> int:
    depth = 0
    needle = f" {keyword} "
    padded = f" {text} "
    for index, char in enumerate(padded):
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif depth == 0 and padded.startswith(needle, index):
            return max(index - 1, 0)
    return -1


def parse_node(text: str) -> Node:
    text = text.strip()
    match = re.match(r"^(E|R)\((.*)\)$", text)
    if not match:
        raise ParseError(f"Expected E(term,term) or R(term,term), got {text!r}.")
    left_text, right_text = split_top_level_pair(match.group(2))
    return Node(match.group(1), parse_term(left_text), parse_term(right_text))


def strip_comments(text: str) -> list[str]:
    lines = []
    for raw_line in text.splitlines():
        line = raw_line.lstrip("\ufeff").split("#", 1)[0].strip()
        if line:
            lines.append(line)
    return lines


def parse_graph_dsl(text: str) -> list[Edge]:
    edges: list[Edge] = []
    lines = strip_comments(text)
    for line in lines:
        parts = [part.strip() for part in line.split("->")]
        if len(parts) < 2:
            raise ParseError(f"Expected an edge with '->', got {line!r}.")
        nodes = [parse_node(part) for part in parts]
        edges.extend(Edge(source, target) for source, target in zip(nodes, nodes[1:]))
    return edges


def parse_arg_term(text: str) -> Term:
    text = text.strip()
    if not text:
        return Term("Unit")
    return parse_term(text)


def args_term(args: list[Term]) -> Term:
    if not args:
        return Term("Unit")
    if len(args) == 1:
        return args[0]
    return Term("Args", tuple(args))


def parse_call(expr: str) -> tuple[str, list[str]] | None:
    expr = expr.strip()
    match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", expr)
    if not match:
        return None
    raw_args = match.group(2).strip()
    return match.group(1), ([] if raw_args == "" else split_top_level(raw_args, ","))


def parse_param(text: str) -> Param:
    text = text.strip()
    if "!" in text:
        name, effect = [part.strip() for part in text.split("!", 1)]
        if not name or not effect:
            raise ParseError(f"Invalid higher-order parameter annotation {text!r}.")
        return Param(name, effect)
    if ":" in text:
        name, effect = [part.strip() for part in text.split(":", 1)]
        if effect.startswith("A->B!"):
            effect = effect.split("!", 1)[1].strip()
        if not name or not effect:
            raise ParseError(f"Invalid higher-order parameter annotation {text!r}.")
        return Param(name, effect)
    return Param(text)


def parse_program(text: str) -> tuple[dict[str, FunctionDef], set[str], tuple[str, list[Term]]]:
    definitions: dict[str, FunctionDef] = {}
    l0_names: set[str] = set()
    run_target: tuple[str, list[Term]] | None = None

    for line in strip_comments(text):
        if line.startswith("l0 "):
            name = line[3:].strip()
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", name):
                raise ParseError(f"Invalid L0 name {name!r}.")
            l0_names.add(name)
            continue

        run_match = re.match(r"^run\s+([A-Za-z_][A-Za-z0-9_]*)\((.*)\)$", line)
        if run_match:
            raw_args = run_match.group(2).strip()
            run_target = (
                run_match.group(1),
                [] if raw_args == "" else [parse_arg_term(part) for part in split_top_level(raw_args, ",")],
            )
            continue

        def_match = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)\(([^)]*)\)\s*=\s*(.+)$", line)
        if def_match:
            name = def_match.group(1)
            raw_params = def_match.group(2).strip()
            params = tuple(parse_param(part) for part in split_top_level(raw_params, ",") if part.strip())
            definitions[name] = FunctionDef(name, params, def_match.group(3).strip())
            continue

        raise ParseError(f"Unsupported mini-CHC line: {line!r}.")

    if run_target is None:
        raise ParseError("Mini-CHC input must include a run statement.")
    if run_target[0] not in definitions and run_target[0] not in l0_names:
        raise ParseError(f"run references undefined function {run_target[0]!r}.")
    return definitions, l0_names, run_target


def canonical_edges(edges: Iterable[Edge]) -> tuple[str, ...]:
    return tuple(sorted(edge.to_string() for edge in edges))


def dedupe_edges(edges: Iterable[Edge]) -> list[Edge]:
    seen: set[str] = set()
    result: list[Edge] = []
    for edge in edges:
        key = edge.to_string()
        if key not in seen:
            seen.add(key)
            result.append(edge)
    return result


class MiniCHCAnalyzer:
    def __init__(self, definitions: dict[str, FunctionDef], l0_names: set[str]):
        self.definitions = definitions
        self.l0_names = l0_names
        self.effect_summaries: dict[str, list[Edge]] = {name: [] for name in definitions}
        self.effect_summary_details: dict[str, dict[str, object]] = {
            name: {
                "summary_id": f"Eff({name})",
                "function": name,
                "edges": [],
                "status": "not_needed",
                "iteration_count": 0,
                "max_iterations": MAX_EFFECT_ITERATIONS,
                "widening_applied": False,
                "conservative_reason": None,
            }
            for name in definitions
        }
        self.fixed_point_status = "not_needed"
        self.higher_order_effects: list[dict[str, str]] = []
        self.effect_composition_status = "complete"
        self.missing_effect_annotations: list[dict[str, str]] = []
        self.chc_level = "CHC-0"
        self.recursive_seen = False

    def compute_summaries(self) -> None:
        if not self.definitions:
            return
        status = "not_needed"
        previous = {name: () for name in self.definitions}
        for iteration in range(MAX_EFFECT_ITERATIONS):
            changed = False
            for definition in self.definitions.values():
                symbolic_args = [Term(param.name) for param in definition.params]
                self_node = Node("E", Term(definition.name), args_term(symbolic_args))
                env = self.initial_env(definition, symbolic_args)
                result = self.eval_expr(definition.body, env, self_node, stack=[definition.name], summary_mode=True)
                next_key = canonical_edges(result.edges)
                if next_key != previous[definition.name]:
                    changed = True
                    previous[definition.name] = next_key
                summary_edges = dedupe_edges(result.edges)
                self.effect_summaries[definition.name] = summary_edges
                self.effect_summary_details[definition.name].update(
                    {
                        "edges": [edge.to_string() for edge in summary_edges],
                        "iteration_count": iteration + 1,
                    }
                )
            if not changed:
                self.fixed_point_status = "converged_exact" if self.recursive_seen else "not_needed"
                for definition_name in self.definitions:
                    self.effect_summary_details[definition_name]["status"] = self.fixed_point_status
                return
            status = "recursive"
        self.fixed_point_status = "not_converged"
        for definition_name in self.definitions:
            self.effect_summary_details[definition_name].update(
                {
                    "status": "not_converged",
                    "conservative_reason": (
                        f"Effect summary for {definition_name} did not stabilize within "
                        f"{MAX_EFFECT_ITERATIONS} iterations."
                    ),
                }
            )

    def initial_env(self, definition: FunctionDef, args: list[Term | FunctionValue]) -> dict[str, TypeValue]:
        if len(args) != len(definition.params):
            raise ParseError(f"{definition.name} expects {len(definition.params)} argument(s), got {len(args)}.")
        env: dict[str, TypeValue] = {}
        for param, arg in zip(definition.params, args):
            if param.is_function:
                if isinstance(arg, FunctionValue):
                    env[param.name] = TypeValue("Function", function=FunctionValue(arg.name, param.effect))
                elif isinstance(arg, Term):
                    env[param.name] = TypeValue("Function", function=FunctionValue(arg.to_string(), param.effect))
                else:
                    raise ParseError(f"Invalid function argument for {param.name}.")
                self.chc_level = max_level(self.chc_level, "CHC-2")
            else:
                if isinstance(arg, FunctionValue):
                    raise InsufficientInfo(f"Higher-order argument {arg.name!r} requires an explicit effect annotation.")
                env[param.name] = TypeValue("Val", term=arg if isinstance(arg, Term) else Term(param.name))
        return env

    def run(self, name: str, args: list[Term]) -> EffectResult:
        if name in self.l0_names:
            return EffectResult(value=TypeValue("Comp"), semantic_status="unproved")
        definition = self.definitions[name]
        converted_args: list[Term | FunctionValue] = []
        for param, arg in zip(definition.params, args):
            if param.is_function and not arg.args and arg.name in self.definitions:
                converted_args.append(FunctionValue(arg.name, param.effect))
            else:
                converted_args.append(arg)
        self_node = Node("E", Term(name), args_term(args))
        env = self.initial_env(definition, converted_args)
        result = self.eval_expr(definition.body, env, self_node, stack=[name], summary_mode=False)
        return result

    def substitute_summary(self, callee: FunctionDef, actual_terms: list[Term]) -> list[Edge]:
        mapping = {param.name: term for param, term in zip(callee.params, actual_terms)}
        return [edge.substitute(mapping) for edge in self.effect_summaries.get(callee.name, [])]

    def eval_expr(
        self,
        expr: str,
        env: dict[str, TypeValue],
        self_node: Node,
        stack: list[str],
        summary_mode: bool,
    ) -> EffectResult:
        expr = strip_outer_parens(expr.strip())
        if expr in {"halt", "loop"}:
            return EffectResult(value=TypeValue("Comp"))

        if expr.startswith("let "):
            return self.eval_let(expr, env, self_node, stack, summary_mode)
        if expr.startswith("if "):
            return self.eval_if(expr, env, self_node, stack, summary_mode)

        call = parse_call(expr)
        if call is not None:
            name, raw_args = call
            if name == "H":
                if len(raw_args) != 2:
                    raise ParseError("H expects two arguments.")
                left = self.term_from_value(raw_args[0], env)
                right = self.term_from_value(raw_args[1], env)
                observed = Node("E", left, right)
                result = Node("R", left, right)
                return EffectResult(
                    edges=[Edge(observed, result)],
                    value=TypeValue("HaltResult", halt_terms=(left, right)),
                    semantic_status="not_analyzed",
                )
            return self.eval_call(name, raw_args, env, self_node, stack, summary_mode)

        if expr in env:
            return EffectResult(value=env[expr])
        return EffectResult(value=TypeValue("Val"))

    def eval_let(
        self,
        expr: str,
        env: dict[str, TypeValue],
        self_node: Node,
        stack: list[str],
        summary_mode: bool,
    ) -> EffectResult:
        match = re.match(r"^let\s+([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$", expr)
        if not match:
            raise ParseError(f"Invalid let expression {expr!r}.")
        name = match.group(1)
        rest = match.group(2)
        in_index = find_keyword_top_level(rest, "in")
        if in_index < 0:
            raise ParseError(f"let expression must contain top-level 'in': {expr!r}.")
        bound_expr = rest[:in_index].strip()
        body_expr = rest[in_index + len(" in ") :].strip()
        bound = self.eval_expr(bound_expr, dict(env), self_node, stack, summary_mode)
        next_env = dict(env)
        next_env[name] = bound.value
        body = self.eval_expr(body_expr, next_env, self_node, stack, summary_mode)
        bound.extend(body)
        bound.value = body.value
        return bound

    def eval_if(
        self,
        expr: str,
        env: dict[str, TypeValue],
        self_node: Node,
        stack: list[str],
        summary_mode: bool,
    ) -> EffectResult:
        body = expr[3:].strip()
        then_index = find_keyword_top_level(body, "then")
        if then_index < 0:
            raise ParseError(f"if expression must contain top-level 'then': {expr!r}.")
        condition_expr = body[:then_index].strip()
        rest = body[then_index + len(" then ") :].strip()
        else_index = find_keyword_top_level(rest, "else")
        if else_index < 0:
            raise ParseError(f"if expression must contain top-level 'else': {expr!r}.")
        then_expr = rest[:else_index].strip()
        else_expr = rest[else_index + len(" else ") :].strip()

        condition = self.eval_expr(condition_expr, dict(env), self_node, stack, summary_mode)
        then_result = self.eval_expr(then_expr, dict(env), self_node, stack, summary_mode)
        else_result = self.eval_expr(else_expr, dict(env), self_node, stack, summary_mode)
        condition.extend(then_result)
        condition.extend(else_result)
        if condition.value.kind == "HaltResult" and condition.value.halt_terms is not None:
            left, right = condition.value.halt_terms
            condition.edges.append(Edge(Node("R", left, right), self_node))
        condition.value = TypeValue("Comp")
        return condition

    def eval_call(
        self,
        name: str,
        raw_args: list[str],
        env: dict[str, TypeValue],
        self_node: Node,
        stack: list[str],
        summary_mode: bool,
    ) -> EffectResult:
        arg_values = [self.eval_expr(arg, dict(env), self_node, stack, summary_mode) for arg in raw_args]
        result = EffectResult(value=TypeValue("Comp"))
        for value in arg_values:
            result.extend(value)
            if value.value.kind == "HaltResult":
                raise ParseError("HaltResult cannot be passed as a function argument.")

        actual_terms = [self.term_from_value(arg, env) for arg in raw_args]
        if name in self.l0_names:
            return result

        if name in env and env[name].kind == "Function":
            function = env[name].function
            if function is None or function.effect is None:
                result.incomplete_higher_order = True
                self.missing_effect_annotations.append(
                    {"parameter": name, "required": "A -> B ! Eff", "reason": "Missing callback effect."}
                )
                raise InsufficientInfo(f"Higher-order function {name!r} is missing an explicit effect annotation.")
            self.chc_level = max_level(self.chc_level, "CHC-2")
            if not summary_mode or function.name in self.definitions:
                self.higher_order_effects.append(
                    {"parameter": name, "callee": function.name, "effect": function.effect, "status": "composed"}
                )
            if function.name not in self.definitions:
                if summary_mode:
                    return result
                result.incomplete_higher_order = True
                raise InsufficientInfo(f"Higher-order callee {function.name!r} is not defined.")
            callee = self.definitions[function.name]
            if function.name in stack or summary_mode:
                result.edges.extend(self.substitute_summary(callee, actual_terms))
            else:
                callee_env = self.initial_env(callee, actual_terms)
                callee_result = self.eval_expr(callee.body, callee_env, self_node, stack + [function.name], summary_mode)
                result.extend(callee_result)
            return result

        if name in env:
            raise InsufficientInfo(f"Higher-order call through {name!r} requires an explicit effect annotation.")

        if name not in self.definitions:
            if name and name[0].isupper():
                return result
            raise ParseError(f"Call references undefined function {name!r}.")

        callee = self.definitions[name]
        if name in stack:
            self.recursive_seen = True
            self.chc_level = max_level(self.chc_level, "CHC-1")
        if name in stack or summary_mode:
            result.edges.extend(self.substitute_summary(callee, actual_terms))
            return result
        callee_env = self.initial_env(callee, actual_terms)
        callee_result = self.eval_expr(callee.body, callee_env, self_node, stack + [name], summary_mode)
        result.extend(callee_result)
        return result

    def term_from_value(self, expr: str, env: dict[str, TypeValue]) -> Term:
        expr = strip_outer_parens(expr.strip())
        if expr in env and env[expr].kind == "Function" and env[expr].function is not None:
            return Term(env[expr].function.name)
        if expr in env and env[expr].term is not None:
            return env[expr].term
        if expr in env:
            return Term(expr)
        call = parse_call(expr)
        if call is None:
            return parse_arg_term(expr)
        name, raw_args = call
        return Term(name, tuple(self.term_from_value(arg, env) for arg in raw_args))


def strip_outer_parens(expr: str) -> str:
    while expr.startswith("(") and expr.endswith(")"):
        depth = 0
        balanced = True
        for index, char in enumerate(expr):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0 and index != len(expr) - 1:
                    balanced = False
                    break
        if not balanced:
            break
        expr = expr[1:-1].strip()
    return expr


def max_level(left: str, right: str) -> str:
    order = {"CHC-0": 0, "CHC-1": 1, "CHC-2": 2}
    return left if order[left] >= order[right] else right


def analysis_profile(
    chc_level: str,
    fixed_point_status: str = "not_needed",
    effect_composition_status: str = "complete",
) -> str:
    if effect_composition_status == "incomplete" or chc_level == "CHC-2":
        return "annotation_required_chc2"
    if chc_level == "CHC-1" or fixed_point_status in {
        "converged",
        "converged_exact",
        "converged_conservative",
        "not_converged",
    }:
        return "conservative_chc1"
    return "complete_for_chc0"


Substitution = dict[str, Term]


def walk(term: Term, subst: Substitution) -> Term:
    while term.is_var and term.name in subst:
        term = subst[term.name]
    return term


def occurs(var_name: str, term: Term, subst: Substitution) -> bool:
    term = walk(term, subst)
    if term.is_var:
        return term.name == var_name
    return any(occurs(var_name, arg, subst) for arg in term.args)


def bind(var: Term, term: Term, subst: Substitution) -> Substitution | None:
    if var == term:
        return subst
    if occurs(var.name, term, subst):
        return None
    next_subst = dict(subst)
    next_subst[var.name] = term
    return next_subst


def unify_term(left: Term, right: Term, subst: Substitution) -> Substitution | None:
    left = walk(left, subst)
    right = walk(right, subst)
    if left == right:
        return subst
    if left.is_var:
        return bind(left, right, subst)
    if right.is_var:
        return bind(right, left, subst)
    if left.name != right.name or len(left.args) != len(right.args):
        return None
    for left_arg, right_arg in zip(left.args, right.args):
        subst = unify_term(left_arg, right_arg, subst)
        if subst is None:
            return None
    return subst


def unify_node_labels(left: Node, right: Node) -> Substitution | None:
    subst: Substitution = {}
    subst = unify_term(left.left, right.left, subst)
    if subst is None:
        return None
    return unify_term(left.right, right.right, subst)


def subst_to_json(subst: Substitution | None) -> dict[str, str] | None:
    if subst is None:
        return None
    return {name: walk(term, subst).to_string() for name, term in sorted(subst.items())}


def graph_nodes(edges: Iterable[Edge]) -> list[Node]:
    seen: set[Node] = set()
    nodes: list[Node] = []
    for edge in edges:
        for node in (edge.source, edge.target):
            if node not in seen:
                seen.add(node)
                nodes.append(node)
    return nodes


def find_path(edges: list[Edge], source: Node, target: Node) -> list[Node] | None:
    adjacency: dict[Node, list[Node]] = {}
    for edge in edges:
        adjacency.setdefault(edge.source, []).append(edge.target)

    stack: list[tuple[Node, list[Node]]] = [(source, [source])]
    while stack:
        node, path = stack.pop()
        for neighbor in adjacency.get(node, []):
            next_path = path + [neighbor]
            if neighbor == target:
                return next_path
            if neighbor not in path:
                stack.append((neighbor, next_path))
    return None


def base_result(
    classification: str,
    edges: list[Edge],
    semantic_status: str,
    explanation: str,
    *,
    chc_level: str = "CHC-0",
    effect_summaries: dict[str, list[Edge]] | None = None,
    fixed_point_status: str = "not_needed",
    higher_order_effects: list[dict[str, str]] | None = None,
    effect_composition_status: str = "complete",
    reachable_pairs: list[dict] | None = None,
    unifier: dict[str, str] | None = None,
    effect_summary_details: dict[str, dict[str, object]] | None = None,
    missing_effect_annotations: list[dict[str, str]] | None = None,
) -> dict:
    return {
        "classification": classification,
        "graph": [edge.to_string() for edge in edges],
        "reachable_e_pairs": reachable_pairs or [],
        "unifier": unifier,
        "semantic_status": semantic_status,
        "chc_level": chc_level,
        "effect_summaries": {
            name: [edge.to_string() for edge in summary]
            for name, summary in (effect_summaries or {}).items()
        },
        "fixed_point_status": fixed_point_status,
        "higher_order_effects": higher_order_effects or [],
        "missing_effect_annotations": missing_effect_annotations or [],
        "effect_composition_status": effect_composition_status,
        "effect_summary_details": effect_summary_details or {},
        "analysis_profile": analysis_profile(chc_level, fixed_point_status, effect_composition_status),
        "capability_boundary": dict(CAPABILITY_BOUNDARY),
        "validity_scope": VALIDITY_SCOPE,
        "identity_resolution": default_identity_resolution(),
        "formal_status": "mechanized",
        "theorem_coverage": default_theorem_coverage(chc_level),
        "explanation": explanation,
    }


def analyze_edges(
    edges: list[Edge],
    semantic_status: str = "not_analyzed",
    *,
    chc_level: str = "CHC-0",
    effect_summaries: dict[str, list[Edge]] | None = None,
    fixed_point_status: str = "not_needed",
    higher_order_effects: list[dict[str, str]] | None = None,
    effect_composition_status: str = "complete",
    effect_summary_details: dict[str, dict[str, object]] | None = None,
    missing_effect_annotations: list[dict[str, str]] | None = None,
) -> dict:
    nodes = graph_nodes(edges)
    e_nodes = [node for node in nodes if node.kind == "E"]
    reachable_pairs = []
    first_paradox = None

    for source in e_nodes:
        for target in e_nodes:
            path = find_path(edges, source, target)
            if path is None:
                continue
            unifier = unify_node_labels(source, target)
            pair = {
                "source": source.to_string(),
                "target": target.to_string(),
                "path": [node.to_string() for node in path],
                "unifier": subst_to_json(unifier),
            }
            reachable_pairs.append(pair)
            if unifier is not None and first_paradox is None:
                first_paradox = pair

    if first_paradox:
        return base_result(
            "causal_paradox",
            edges,
            semantic_status,
            "Found a nonempty E-to-E path whose endpoint labels unify, so the graph contains prediction feedback.",
            chc_level=chc_level,
            effect_summaries=effect_summaries,
            fixed_point_status=fixed_point_status,
            higher_order_effects=higher_order_effects,
            effect_composition_status=effect_composition_status,
            reachable_pairs=reachable_pairs,
            unifier=first_paradox["unifier"],
            effect_summary_details=effect_summary_details,
            missing_effect_annotations=missing_effect_annotations,
        )

    return base_result(
        "valid_acyclic",
        edges,
        semantic_status,
        "No unifiable E-to-E feedback path was found.",
        chc_level=chc_level,
        effect_summaries=effect_summaries,
        fixed_point_status=fixed_point_status,
        higher_order_effects=higher_order_effects,
        effect_composition_status=effect_composition_status,
        reachable_pairs=reachable_pairs,
        effect_summary_details=effect_summary_details,
        missing_effect_annotations=missing_effect_annotations,
    )


def is_graph_like(text: str) -> bool:
    lines = strip_comments(text)
    return bool(lines) and all("->" in line for line in lines)


def analyze_mini_chc(text: str) -> dict:
    definitions, l0_names, run_target = parse_program(text)
    analyzer = MiniCHCAnalyzer(definitions, l0_names)
    analyzer.compute_summaries()
    if analyzer.fixed_point_status == "not_converged":
        first_reason = next(
            (
                str(summary.get("conservative_reason"))
                for summary in analyzer.effect_summary_details.values()
                if summary.get("conservative_reason")
            ),
            "CHC-1 effect summaries did not converge within the configured iteration limit.",
        )
        return base_result(
            "insufficient_info",
            [],
            "not_analyzed",
            first_reason,
            chc_level="CHC-1",
            effect_summaries=analyzer.effect_summaries,
            fixed_point_status=analyzer.fixed_point_status,
            effect_composition_status="incomplete",
            effect_summary_details=analyzer.effect_summary_details,
        )
    name, args = run_target
    result = analyzer.run(name, args)
    if result.incomplete_higher_order:
        analyzer.effect_composition_status = "incomplete"
    return analyze_edges(
        result.edges,
        semantic_status=result.semantic_status,
        chc_level=analyzer.chc_level,
        effect_summaries=analyzer.effect_summaries,
        fixed_point_status=analyzer.fixed_point_status,
        higher_order_effects=analyzer.higher_order_effects + result.higher_order_effects,
        effect_composition_status=analyzer.effect_composition_status,
        effect_summary_details=analyzer.effect_summary_details,
        missing_effect_annotations=analyzer.missing_effect_annotations,
    )


def analyze_text(text: str, mode: str = "auto") -> dict:
    try:
        if mode == "graph" or (mode == "auto" and is_graph_like(text)):
            return analyze_edges(parse_graph_dsl(text), semantic_status="not_analyzed")
        if mode == "mini-chc" or mode == "auto":
            return analyze_mini_chc(text)
        raise ParseError(f"Unsupported mode {mode!r}.")
    except InsufficientInfo as exc:
        return base_result(
            "insufficient_info",
            [],
            "not_analyzed",
            str(exc),
            chc_level="CHC-2",
            fixed_point_status="not_needed",
            effect_composition_status="incomplete",
        )
    except ParseError as exc:
        return base_result("parse_error", [], "not_analyzed", str(exc))


def format_human(result: dict) -> str:
    lines = [
        f"classification: {result['classification']}",
        f"semantic_status: {result['semantic_status']}",
        f"chc_level: {result.get('chc_level', 'CHC-0')}",
        f"fixed_point_status: {result.get('fixed_point_status', 'not_needed')}",
        f"effect_composition_status: {result.get('effect_composition_status', 'complete')}",
        f"explanation: {result['explanation']}",
    ]
    if result["graph"]:
        lines.append("graph:")
        lines.extend(f"  {edge}" for edge in result["graph"])
    if result["unifier"]:
        lines.append("unifier:")
        lines.extend(f"  {key} = {value}" for key, value in result["unifier"].items())
    if result["reachable_e_pairs"]:
        lines.append("reachable_e_pairs:")
        for pair in result["reachable_e_pairs"]:
            unifier = pair["unifier"] if pair["unifier"] is not None else "none"
            lines.append(f"  {pair['source']} ->+ {pair['target']} | unifier={unifier}")
    if result.get("higher_order_effects"):
        lines.append("higher_order_effects:")
        for item in result["higher_order_effects"]:
            lines.append(f"  {item}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Check CHC-0/CHC-1/CHC-2 causal feedback.")
    parser.add_argument("input", help="Input file containing graph DSL or mini-CHC syntax.")
    parser.add_argument(
        "--mode",
        choices=("auto", "graph", "mini-chc"),
        default="auto",
        help="Input parser mode. Default: auto.",
    )
    parser.add_argument(
        "--format",
        choices=("human", "json"),
        default="human",
        help="Output format. Default: human.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    text = Path(args.input).read_text(encoding="utf-8")
    result = analyze_text(text, mode=args.mode)
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(format_human(result))
    return 2 if result["classification"] == "parse_error" else 0


if __name__ == "__main__":
    sys.exit(main())

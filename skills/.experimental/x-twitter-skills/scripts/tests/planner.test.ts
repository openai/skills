import test from "node:test";
import assert from "node:assert/strict";
import { buildResearchPlan } from "../lib/planner";

test("buildResearchPlan includes core lanes and handle-specific query", () => {
  const plan = buildResearchPlan("What is @sama and @gdb saying about OpenAI agents?", {
    maxQueries: 8,
  });

  const labels = plan.queries.map((q) => q.label);
  assert.ok(labels.some((label) => label.startsWith("Core")));
  assert.ok(labels.includes("Linked Evidence"));
  assert.ok(plan.queries.some((q) => q.id === "handle-sama"));
  assert.ok(plan.queries.some((q) => q.id === "handle-gdb"));
});

test("buildResearchPlan clamps query count", () => {
  const small = buildResearchPlan("ai coding tools", { maxQueries: 1 });
  assert.equal(small.queries.length >= 2, true);

  const large = buildResearchPlan("ai coding tools", { maxQueries: 99 });
  assert.equal(large.queries.length <= 10, true);
});

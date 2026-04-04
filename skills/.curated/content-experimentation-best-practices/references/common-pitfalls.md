# Common Experimentation Pitfalls

Avoid these mistakes that invalidate results or lead to wrong conclusions.

## Statistical Mistakes

### 1. Stopping Early (Peeking)

**The problem:** Checking results daily and stopping when you see significance.

**Why it's wrong:** Statistical significance fluctuates. At any point during a test, you might see "significance" that disappears with more data. This is called the "peeking problem" or "repeated significance testing."

**The fix:**
- Pre-calculate required sample size
- Commit to running until you reach it
- If you must peek, use sequential testing methods that account for multiple looks

### 2. Underpowered Tests

**The problem:** Running tests without enough traffic to detect realistic effect sizes.

**Why it's wrong:** You'll conclude "no difference" when there actually is one—you just couldn't detect it.

**The fix:**
- Calculate required sample size before starting
- Be realistic about minimum detectable effect (can you act on a 0.5% improvement?)
- If traffic is low, test bigger changes

### 3. Multiple Comparisons

**The problem:** Testing many variants or metrics and celebrating any that reach significance.

**Why it's wrong:** With 20 metrics, you expect 1 false positive at 95% confidence—by chance alone.

**The fix:**
- Define ONE primary metric before starting
- Use Bonferroni correction or similar for multiple comparisons
- Treat secondary metrics as directional, not conclusive

### 4. Ignoring Segments

**The problem:** Only looking at aggregate results.

**Why it's wrong:** Simpson's Paradox—overall winner might be loser for your key segments.

**The fix:**
- Always segment by device, traffic source, user type
- Check if results are consistent across segments
- If segments differ dramatically, investigate why

## Design Mistakes

### 5. Testing Too Many Things

**The problem:** Changing headline, image, CTA, and layout simultaneously.

**Why it's wrong:** You won't know which change caused the result. And each variable multiplies required sample size.

**The fix:**
- Test one variable at a time (A/B testing)
- If testing multiple, use proper multivariate testing with adequate sample size
- Prioritize highest-impact changes first

### 6. Vague Hypothesis

**The problem:** "Let's see if this new design is better."

**Why it's wrong:** Without a hypothesis, you can't learn WHY something worked (or didn't).

**The fix:**
- State: "We believe [change] will [impact metric] because [reasoning]"
- Even if you're wrong, you learn something

### 7. No Control

**The problem:** Changing the control during the test, or not having one.

**Why it's wrong:** You need a stable baseline to compare against.

**The fix:**
- Never modify the control mid-test
- If you must change it, start a new test
- Document exactly what the control is

## Execution Mistakes

### 8. External Contamination

**The problem:** Running a test during a sale, holiday, or major event.

**Why it's wrong:** External factors affect both variants differently, contaminating results.

**The fix:**
- Avoid tests during unusual periods
- If unavoidable, note it and extend the test past the event
- Compare to the same period historically

### 9. Selection Bias

**The problem:** Testing on a non-representative sample (e.g., only logged-in users).

**Why it's wrong:** Results won't generalize to your full audience.

**The fix:**
- Test on representative traffic
- Be explicit about who's included/excluded
- Note limitations when reporting results

### 10. Implementation Bugs

**The problem:** Variants don't render correctly, tracking fires incorrectly, assignment is biased.

**Why it's wrong:** You're not testing what you think you're testing.

**The fix:**
- QA both variants thoroughly before launch
- Verify tracking events fire correctly
- Check assignment distribution matches weights

## Interpretation Mistakes

### 11. Celebrating Trivial Wins

**The problem:** Implementing a change because it was "statistically significant" even though the effect was tiny.

**Why it's wrong:** Statistical significance ≠ practical significance. A 0.01% improvement isn't worth the complexity.

**The fix:**
- Define minimum meaningful effect before starting
- Consider implementation cost vs. benefit
- Don't over-optimize

### 12. Ignoring Confidence Intervals

**The problem:** Only reporting point estimates ("5% improvement!").

**Why it's wrong:** The true effect could be anywhere in the confidence interval.

**The fix:**
- Report confidence intervals: "5% improvement (95% CI: 2%-8%)"
- Base decisions on the lower bound for conservative estimates
- Wider intervals = more uncertainty

### 13. Not Documenting Learnings

**The problem:** Running tests but not recording what you learned.

**Why it's wrong:** You'll repeat mistakes, forget context, lose institutional knowledge.

**The fix:**
- Document every test: hypothesis, results, learnings
- Include what surprised you
- Build a searchable knowledge base

## Organizational Mistakes

### 14. HiPPO (Highest Paid Person's Opinion)

**The problem:** Running experiments but ignoring results when leadership disagrees.

**Why it's wrong:** Defeats the purpose of data-driven decision making.

**The fix:**
- Get buy-in before testing that results will be honored
- Present data clearly to stakeholders
- Frame as "learning" not "winning/losing"

### 15. Testing Everything

**The problem:** Running experiments on trivial changes that don't matter.

**Why it's wrong:** Wastes resources, creates testing fatigue, delays important experiments.

**The fix:**
- Prioritize tests by potential impact
- Not everything needs a test—use judgment for low-risk changes
- Focus experimentation resources on high-value decisions

### 16. Sample Ratio Mismatch (SRM)

**The problem:** The actual traffic split doesn't match the intended split (e.g., you expect 50/50 but observe 52/48).

**Why it's wrong:** SRM is a strong signal of an implementation bug — broken randomization, bot contamination, or redirect issues. Results from experiments with SRM cannot be trusted.

**The fix:**
- Check the actual split ratio against expected before analyzing results
- Use a chi-squared test to detect statistically significant mismatches
- If SRM is detected, investigate the root cause before drawing any conclusions
- Common causes: bot traffic, browser redirects dropping users, bucketing bugs

### 17. Novelty and Primacy Effects

**The problem:** Users react differently to new designs initially, and the effect fades over time.

**Why it's wrong:** Short experiments may show inflated effects that don't persist. Returning users may click more simply because something looks new.

**The fix:**
- Run experiments for at least 2 full business cycles
- Segment results by new vs. returning users
- If possible, check whether the effect holds in the second week vs. the first

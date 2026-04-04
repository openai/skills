# Statistical Foundations

Understanding basic statistics prevents misinterpreting experiment results.

## Key Concepts

### Statistical Significance

A measure of whether observed differences are likely real or due to chance.

- **p-value < 0.05:** "Statistically significant" at 95% confidence
- Means: If there were no real difference, there's less than a 5% chance of seeing results this extreme
- Does NOT mean: The change is important or meaningful
- **Common misconception:** The p-value is NOT "the probability the result is due to chance." It's the probability of observing data this extreme *assuming* the null hypothesis is true.

### Confidence Interval

A range of plausible values for the true effect.

Example: "Conversion rate increased by 5% (95% CI: 2% to 8%)"
- Best estimate: 5% improvement
- Could be as low as 2% or as high as 8%
- Narrower intervals = more certainty

### Statistical Power

The ability to detect a real effect when it exists.

- Standard: 80% power
- Higher power = larger sample size needed
- Low power = might miss real improvements

### Minimum Detectable Effect (MDE)

The smallest improvement worth detecting.

- Smaller MDE = larger sample size needed
- Be realistic: Can you act on a 0.5% improvement?

## Sample Size Calculation

Before running a test, calculate required sample size:

```
Required per variant = 16 × σ² / MDE²

Where:
- σ² = variance (for conversion rate: p × (1-p))
- MDE = minimum detectable effect (absolute)
```

For a 5% baseline conversion rate, detecting a 1% absolute lift (5% → 6%):
- σ² = 0.05 × 0.95 = 0.0475
- MDE² = 0.01² = 0.0001
- n = 16 × 0.0475 / 0.0001 = **7,600 per variant**
- Total: ~15,200 visitors minimum

## Common Statistical Mistakes

### Multiple Comparisons Problem

Testing 10 variants increases false positive rate.

**Solution:** Adjust significance threshold (Bonferroni correction) or use sequential testing methods.

### Peeking Problem

Checking results daily and stopping when significant.

**Why it's wrong:** Significance fluctuates. Early "winners" often regress.

**Solution:** Pre-commit to sample size and duration. Use sequential testing if you must peek.

### Simpson's Paradox

Overall results hide segmented truths.

Example:
- Overall: Variant B wins
- Mobile users: Variant A wins
- Desktop users: Variant A wins
- How? Different traffic mix per variant

**Solution:** Always segment by major factors (device, traffic source).

### Survivorship Bias

Only analyzing users who completed the funnel.

**Solution:** Include all visitors, not just converters.

## Interpreting Results

### Significant + Meaningful
Clear win. Implement the change.

### Significant + Trivial
Statistically different but tiny effect. Consider if worth the complexity.

### Not Significant + Large Effect
Might be real but underpowered. Extend the test or accept uncertainty.

### Not Significant + Small Effect
No detectable difference. Either no real effect or test was underpowered.

## Alternative Approaches

### Bayesian A/B Testing

An alternative to traditional (frequentist) hypothesis testing. Bayesian methods provide:
- **Direct probability statements:** "There's a 95% probability Variant B is better" (more intuitive than p-values)
- **No peeking problem:** Continuous monitoring is built in — you can check results at any time
- **Credible intervals:** Directly interpretable as "the true value falls in this range with X% probability"

Bayesian methods are offered by platforms like VWO and are useful when you need to make decisions with limited traffic or want more intuitive reporting for stakeholders.

### Multi-Armed Bandits

Dynamically allocate more traffic to winning variants while still learning:
- **Thompson Sampling:** Balances exploration (learning) with exploitation (serving the best variant)
- **Best for:** Ongoing optimization where you want to minimize regret during the test
- **Trade-off:** Faster convergence to the winner, but less statistical rigor than fixed-allocation A/B tests

Consider bandits for content recommendations, personalization, or situations where the cost of showing a losing variant is high.

### Sequential Testing

For teams that need to monitor experiments continuously:
- **Group sequential designs** (O'Brien-Fleming, Lan-DeMets) allow pre-planned interim analyses
- **Always-valid p-values** let you check results at any time without inflating false positive rates
- Use when you must balance the peeking problem with business pressure to act on results quickly

## When to Trust Results

Checklist before declaring a winner:
- [ ] Reached pre-calculated sample size
- [ ] Ran for full business cycle (1-2 weeks minimum)
- [ ] p-value < 0.05 (or your chosen threshold)
- [ ] Effect size is meaningful for business
- [ ] Results consistent across major segments
- [ ] No external factors contaminated results

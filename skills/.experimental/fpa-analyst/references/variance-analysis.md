# Variance Analysis Reference

## Budget vs. Actual Template

Standard P&L variance layout (columns per period):

| Line Item | Actual | Budget | $ Variance | % Variance | Commentary |
|-----------|--------|--------|------------|------------|------------|

### Variance decomposition

When data supports it, decompose total variance into:

1. **Volume variance**: (Actual units - Budget units) x Budget price
2. **Price variance**: (Actual price - Budget price) x Actual units
3. **Mix variance**: shift in product/channel/segment mix vs. plan
4. **Timing variance**: revenue/expense recognized in a different period than planned
5. **FX variance**: impact of exchange rate movement (international businesses only)

### Materiality thresholds

Default flagging rules (override with user-specified thresholds):
- Flag line items with |% variance| > 5%
- Flag line items with |$ variance| > $50K (adjust for company size)
- Always flag sign flips (budget positive, actual negative or vice versa)

### Waterfall / bridge chart

For executive presentations, build a waterfall from budget to actual:
```
Budget -> Volume -> Price -> Mix -> Timing -> Other -> Actual
```

Use `matplotlib` or `openpyxl.chart.BarChart` with stacked bars to approximate a waterfall.

## Flux Analysis (Month-End)

Compare each GL account across three dimensions:
1. Current month vs. prior month
2. Current month vs. same month prior year
3. Current month vs. forecast/budget

Flag accounts where any comparison exceeds the threshold. Draft one-line variance explanations for the top 10 movers.

### Flux template columns

| Account | Account Name | Current Month | Prior Month | MoM $ Change | MoM % Change | PY Same Month | YoY $ Change | YoY % Change | Explanation |
|---------|-------------|---------------|-------------|--------------|--------------|---------------|--------------|--------------|-------------|

## Rolling Forecast Update

When updating a rolling forecast:
1. Replace completed months with actuals.
2. Reforecast remaining months using updated drivers and trends.
3. Show original forecast vs. updated forecast to quantify the change.
4. Highlight assumption changes that drove the reforecast.

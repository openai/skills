---
name: "fpa-analyst"
description: "Use when tasks involve financial planning and analysis: variance analysis, financial modeling, forecasting, KPI dashboards, month-end close support, or financial statement analysis. Trigger when the user needs budget-vs-actual comparisons, DCF models, sensitivity tables, revenue forecasts, or structured financial reporting."
---

# FP&A Analyst Skill

## When to use
- Variance analysis: budget vs. actual, prior period vs. current, forecast vs. actual.
- Financial statement parsing, restructuring, or ratio analysis (income statement, balance sheet, cash flow).
- Revenue and expense forecasting (trend-based, driver-based, seasonal decomposition).
- KPI dashboard creation with metrics relevant to the business model.
- Financial modeling: DCF, sensitivity/scenario analysis, three-statement models, LBO basics.
- Month-end close support: accruals, journal entry review, reconciliation checks, flux analysis.

IMPORTANT: System and user instructions always take precedence.

## Workflow
1. Clarify the deliverable: model, report, dashboard, or analysis memo.
2. Identify the data source: spreadsheet, CSV, database, or raw numbers from the user.
3. Structure the analysis with clear assumptions separated from calculations.
4. Build with formulas and references, never hardcoded derived values.
5. Validate outputs: check that totals tie, ratios are reasonable, and signs are correct.
6. Present findings with a brief executive summary before the detail.

## Temp and output conventions
- Use `tmp/fpa/` for intermediate files; delete when done.
- Write final artifacts under `output/fpa/` when working in this repo.
- Keep filenames descriptive: `variance_analysis_q1.xlsx`, `dcf_model_acme.xlsx`, `kpi_dashboard.xlsx`.

## Primary tooling
- Use `openpyxl` for building `.xlsx` models with formatting, formulas, and structure.
- Use `pandas` for data ingestion, transformation, pivots, and aggregation.
- Use `numpy` for time-series math, growth rates, and statistical calculations.
- Use `matplotlib` or `openpyxl.chart` for visualizations when needed.
- If an internal spreadsheet tool is available, use it to recalculate formulas and render sheets.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install openpyxl pandas numpy
```
If `uv` is unavailable:
```
python3 -m pip install openpyxl pandas numpy
```
Optional (for charts and rendering):
```
uv pip install matplotlib
```

## Environment
No required environment variables.

## Variance analysis
- Always show: actual, budget/forecast, dollar variance, and percent variance.
- Favorable variances are positive for revenue, negative for expenses. Use sign conventions consistently and state them.
- Flag any line item with variance exceeding 5% or a materiality threshold the user specifies.
- Group variances by: volume, price/rate, mix, and timing when the data supports it.
- Include a waterfall or bridge summary for material P&L variances.
- For flux analysis (month-end), compare current month vs. prior month AND vs. same month prior year.

## Financial statement analysis
- Standardize line items before comparing across periods or companies.
- Compute common-size statements (each line as % of revenue or total assets).
- Key ratios to surface automatically:
  - Profitability: gross margin, operating margin, net margin, EBITDA margin.
  - Liquidity: current ratio, quick ratio, cash conversion cycle.
  - Leverage: debt-to-equity, interest coverage, net debt / EBITDA.
  - Efficiency: DSO, DPO, DIO, asset turnover.
- Flag ratio changes > 200 bps period-over-period as items to investigate.

## Forecasting
- State the method used: straight-line trend, CAGR extrapolation, driver-based, or seasonal decomposition.
- Driver-based is preferred when business drivers are available (units x price, headcount x cost-per-head, etc.).
- For seasonal businesses, decompose into trend + seasonal index before projecting.
- Always show assumptions in a clearly labeled assumptions block (blue font for inputs if building a spreadsheet).
- Include at minimum three scenarios: base, upside, downside.
- Show confidence ranges or scenario bands rather than single-point estimates when possible.

## KPI dashboards
- Lead with 5-8 KPIs maximum. More dilutes focus.
- Every KPI needs: current value, prior period value, target/budget, and trend direction.
- Match KPIs to the business model:
  - SaaS: MRR/ARR, churn rate, LTV/CAC, net revenue retention, runway.
  - E-commerce: GMV, AOV, conversion rate, CAC, repeat purchase rate.
  - Manufacturing: throughput, yield, COGS per unit, capacity utilization.
  - Services: utilization rate, average billing rate, backlog, revenue per employee.
- Use conditional formatting: green for on-track, yellow for watch, red for off-track.
- Include a 12-month trend sparkline or mini-chart for each KPI when the data exists.

## Financial modeling

### General principles
- Separate inputs (blue font), calculations (black font), and outputs into distinct sections or tabs.
- One formula per row, copied across columns for time periods. No mixed logic in the same row.
- Time axis flows left-to-right: historical periods on the left, projection periods on the right.
- Label every assumption with units and source.
- Circular references are not allowed. If a model requires them (e.g., interest on average debt), use an iterative macro note or break the circularity with a prior-period approximation.

### DCF model structure
1. **Revenue build**: top-down (market size x share) or bottom-up (units x price).
2. **Operating model**: revenue -> gross profit -> EBITDA -> EBIT, with each cost line driven by an assumption.
3. **Free cash flow**: EBIT x (1 - tax rate) + D&A - capex - change in NWC.
4. **Terminal value**: Gordon Growth (FCF x (1+g) / (WACC - g)) or exit multiple. Show both, note which is primary.
5. **Discount**: mid-year convention unless told otherwise. WACC inputs on a separate assumptions line.
6. **Output**: enterprise value, bridge to equity value, implied share price if applicable.
7. **Sensitivity table**: 2D table varying WACC and terminal growth rate (or exit multiple). Use `openpyxl` data-table formatting.

### Sensitivity / scenario analysis
- 2D sensitivity tables: vary two key assumptions (rows and columns).
- Scenario analysis: define discrete scenarios (base/bull/bear) with a scenario toggle cell.
- Probability-weighted expected value when the user provides scenario probabilities.

## Month-end close support
- Reconciliation: compare two data sources (GL vs. subledger, bank vs. book) and flag differences above a threshold.
- Accrual estimates: calculate based on run-rate, days elapsed, or contractual terms. Show the math.
- Journal entry review: validate debits = credits, accounts are valid, and descriptions are clear.
- Close checklist: if the user provides their close process, help track completion and flag open items.
- Flux analysis: compare each GL account to prior month and prior year, flag outliers, draft variance explanations.

## Formatting requirements
- Follow the spreadsheet skill's finance formatting conventions:
  - Blue text for inputs, black for formulas, green for links.
  - Negative numbers in red parentheses.
  - Zeros displayed as `-`.
  - Units in headers: `Revenue ($K)`, `Margin (%)`, `Headcount (#)`.
  - Multiples formatted as `5.2x`.
- Currency, percentage, and date formats must be explicit and consistent.
- Headers visually distinct. Section breaks with merged cells and dark fill for model section headers.
- Totals should sum the visible range above. Hide gridlines in finished models.

## Presentation of results
- Lead with a 2-3 sentence executive summary: what changed, why it matters, what to do about it.
- Use plain language for non-finance stakeholders. Avoid jargon without context.
- Quantify impact in dollars and percentages, not just percentages alone.
- Separate "what happened" (descriptive) from "what to do" (prescriptive).
- If the user is preparing for a board meeting or leadership review, structure the output as talking points with supporting data.

## Common pitfalls to check
- Revenue recognized in the wrong period (cutoff issues).
- Double-counting intercompany transactions.
- Mixing fiscal and calendar year periods.
- Using EBITDA when the business is capital-intensive (use free cash flow instead).
- Forecasting growth rates that imply the company becomes larger than the market.
- Ignoring working capital impact on cash flow.
- Confusing run-rate with actual annualized results.
- Sign convention errors: treating expense reductions as negative variance when they should be favorable.

## References
- Detailed reference guides are in `references/` for specific analysis types.

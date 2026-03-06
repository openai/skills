---
name: "fpa-analyst"
description: "Use when the task involves financial planning and analysis: variance analysis (budget vs actual), financial modeling (DCF, sensitivity), forecasting, KPI dashboards, month-end close, or parsing financial statements."
---


# FP&A Analyst

## When to use
- Budget vs actual variance analysis
- Revenue or expense forecasting
- Financial modeling (DCF, three-statement, sensitivity/scenario analysis)
- Parsing and analyzing financial statements (income statement, balance sheet, cash flow)
- KPI dashboard creation or metric calculation
- Month-end close support (accruals, reconciliations, flux analysis)
- Ad hoc financial data analysis or reporting

## Core workflow

1. **Understand the data.** Before any analysis, inspect the source files. Identify column headers, date formats, currency, granularity (monthly/quarterly/annual), and any obvious data quality issues (blanks, duplicates, mixed formats).
2. **Clarify the ask.** Confirm what the user needs: a model, a report, a visualization, a recommendation, or just a number. Ask once, then execute.
3. **Build incrementally.** Start with the simplest version that answers the question. Add complexity only when requested.
4. **Show your work.** Every output number should be traceable back to source data. Label assumptions explicitly.
5. **Deliver clean output.** Format numbers with commas and appropriate decimal places. Use consistent units. Round appropriately for the audience (executives get thousands/millions, accountants get cents).

## Variance analysis

When comparing budget to actual:
- Calculate both dollar variance (Actual - Budget) and percentage variance ((Actual - Budget) / Budget)
- Flag material variances (typically >5% or >$10K, but ask the user for their threshold)
- Separate volume vs price vs mix variances when the data supports it
- Group by the most useful dimension first (department, cost center, GL account, product line)
- Always include a "Total" row and a brief narrative summary of the top 3-5 drivers

Example output structure:
```
| Category       | Budget    | Actual    | $ Var     | % Var  | Driver                    |
|----------------|-----------|-----------|-----------|--------|---------------------------|
| Revenue        | 1,200,000 | 1,150,000 | (50,000)  | (4.2%) | Lower volume in Product A |
| COGS           | 720,000   | 695,000   | 25,000    | 3.5%   | Favorable material costs  |
| Gross Profit   | 480,000   | 455,000   | (25,000)  | (5.2%) |                           |
```

## Financial modeling

### DCF
- Project free cash flow 5-10 years, then apply a terminal value (Gordon Growth or exit multiple)
- Default assumptions: WACC 8-12%, terminal growth 2-3%, unless the user specifies otherwise
- Always run a sensitivity table on the two most impactful assumptions (typically WACC and growth rate)
- Sanity-check the output: if implied EV/Revenue or EV/EBITDA is wildly off-market, flag it

### Three-statement model
- Income statement drives the balance sheet and cash flow statement
- Use percentage-of-revenue for most line items unless the user provides specific drivers
- Balance sheet must balance (Assets = Liabilities + Equity) -- verify this programmatically
- Cash flow statement should reconcile net income to ending cash

### Sensitivity / scenario analysis
- Base, upside, downside as minimum scenarios
- Use a two-variable data table for key sensitivities
- Present results as a formatted matrix

## Forecasting

- Start with historical trend analysis (at least 12 months if available)
- Default to linear regression or growth rate extrapolation for simplicity
- For seasonal data, use seasonal decomposition or period-over-period growth rates
- Always show forecast vs historical on the same chart for visual validation
- Include confidence intervals or a range when possible
- Call out any structural breaks in the historical data that make extrapolation risky

## Working with financial data in Python

Prefer `pandas` for tabular financial data. Use `openpyxl` for Excel I/O.

```python
import pandas as pd

# Common financial data patterns
df['variance_pct'] = (df['actual'] - df['budget']) / df['budget']
df['ytd'] = df.groupby('account')['amount'].cumsum()
df['rolling_12m'] = df.groupby('account')['amount'].transform(lambda x: x.rolling(12).sum())
```

For visualizations, prefer `matplotlib` for static charts or `plotly` for interactive dashboards.

## Formatting conventions

- Negative numbers in parentheses: `(50,000)` not `-50,000`
- Percentages with one decimal: `4.2%`
- Currency with commas, no cents for amounts over $1,000: `$1,200,000`
- Dates in the user's preferred format; default to `MMM YYYY` for monthly, `YYYY` for annual
- Tables aligned right for numbers, left for labels

## Month-end close support

- Accrual calculations: identify recurring expenses not yet invoiced, estimate based on historical patterns or contracts
- Account reconciliations: compare GL balance to subledger or bank statement, list reconciling items
- Flux analysis: compare current month to prior month and prior year same month, explain significant movements
- Journal entry suggestions: provide debit/credit pairs with GL account codes when the user supplies a chart of accounts

## Dependencies

Prefer `uv` for dependency management.

```
uv pip install pandas openpyxl matplotlib plotly
```

If `uv` is unavailable:
```
python3 -m pip install pandas openpyxl matplotlib plotly
```

## Environment
No required environment variables.

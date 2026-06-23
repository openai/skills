# DCF Modeling Reference

## Model Tab Structure

Organize the workbook with these tabs:

1. **Assumptions** - all inputs in one place, blue font
2. **Income Statement** - historical + projected
3. **Balance Sheet** - historical + projected
4. **Cash Flow** - historical + projected
5. **DCF** - unlevered FCF, discount factors, terminal value, valuation bridge
6. **Sensitivity** - WACC vs. growth rate table, WACC vs. exit multiple table
7. **Output / Summary** - key metrics, implied valuation range

## Unlevered Free Cash Flow

```
Revenue
- COGS
= Gross Profit
- SGA
- R&D
- Other OpEx
= EBIT (Operating Income)
x (1 - Tax Rate)
= NOPAT
+ Depreciation & Amortization
- Capital Expenditures
- Change in Net Working Capital
= Unlevered Free Cash Flow
```

### Net Working Capital

```
NWC = Current Assets (ex cash) - Current Liabilities (ex debt)
Change in NWC = NWC(t) - NWC(t-1)
```

Negative change in NWC = cash source (good). Positive change = cash use.

Use DSO, DIO, DPO to project AR, inventory, AP as % of revenue or COGS.

## Terminal Value

### Gordon Growth Model
```
TV = FCF(n+1) / (WACC - g)
FCF(n+1) = FCF(n) x (1 + g)
```
- `g` should not exceed long-term GDP growth (2-3% nominal) for mature companies.
- Sanity check: TV as % of total enterprise value. If >80%, the near-term projections may be too conservative or the projection period too short.

### Exit Multiple Method
```
TV = EBITDA(n) x Exit Multiple
```
- Use comparable company trading multiples or precedent transaction multiples.
- State the source of the multiple.

### Show both methods and note which is primary.

## Discount Rate (WACC)

```
WACC = (E/V) x Ke + (D/V) x Kd x (1 - t)
```

Where:
- `Ke` = Cost of equity (CAPM: Rf + Beta x ERP + size premium if applicable)
- `Kd` = Pre-tax cost of debt (yield on existing debt or comparable credit spread)
- `E/V` = Equity weight (market cap / enterprise value)
- `D/V` = Debt weight
- `t` = Marginal tax rate

### Mid-year convention
Discount each year's FCF as if received at the midpoint:
```
Discount factor = 1 / (1 + WACC)^(period - 0.5)
```

## Sensitivity Table

Build a 2D data table in the spreadsheet:

**Table 1: WACC vs. Terminal Growth Rate**
- Rows: WACC from -1% to +1% around base case in 0.25% steps
- Columns: Terminal growth rate from 1.5% to 3.5% in 0.5% steps
- Cell values: Implied share price (or enterprise value)

**Table 2: WACC vs. Exit Multiple**
- Same WACC range
- Columns: Exit multiple from -2x to +2x around base case in 0.5x steps

Highlight the base case cell. Use conditional formatting for the range.

## Valuation Bridge

```
Enterprise Value (from DCF)
- Net Debt
- Minority Interest
- Preferred Equity
+ Equity Method Investments
= Equity Value
/ Diluted Shares Outstanding
= Implied Share Price
```

Use treasury stock method for diluted share count if options/warrants exist.

## Common Errors to Check
- Terminal growth rate > WACC (produces negative or infinite value).
- Forgetting to discount the terminal value back to present.
- Using levered FCF with WACC (should be unlevered).
- Not adjusting for mid-year convention consistently.
- Double-counting items in both FCF and the equity bridge.
- Using book value of debt instead of market value for WACC weights.

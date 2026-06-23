# Month-End Close Reference

## Close Checklist Template

Standard close tasks (adapt to the user's process):

### Day 1-2: Subledger Close
- [ ] Close AP subledger, post final invoices
- [ ] Close AR subledger, post final billings
- [ ] Process payroll accrual (if payroll crosses month boundary)
- [ ] Close inventory/COGS subledger
- [ ] Post intercompany transactions and confirm with counterparties

### Day 3-4: Accruals and Adjustments
- [ ] Book revenue accruals / deferrals
- [ ] Book expense accruals (utilities, rent, professional services)
- [ ] Book prepaid amortization entries
- [ ] Book depreciation and amortization
- [ ] Book bad debt / allowance adjustments
- [ ] Post FX revaluation entries (if applicable)

### Day 5-6: Reconciliation
- [ ] Reconcile bank accounts (book vs. bank)
- [ ] Reconcile intercompany balances
- [ ] Reconcile fixed assets (GL vs. subledger)
- [ ] Reconcile payroll (GL vs. payroll provider)
- [ ] Reconcile deferred revenue schedule
- [ ] Tie out BS accounts to supporting schedules

### Day 7-8: Review and Reporting
- [ ] Run trial balance, verify debits = credits
- [ ] Perform flux analysis on all P&L and BS accounts
- [ ] Draft variance commentary for material items
- [ ] Prepare management reporting package
- [ ] Controller/CFO review and sign-off

## Accrual Estimation Methods

### Run-rate accrual
```
Accrual = (Prior month actual / days in prior month) x days elapsed in current month
```
Use when: recurring expenses without invoices yet (utilities, telecom).

### Contractual accrual
```
Accrual = Annual contract value / 12
```
Use when: fixed contracts (rent, software licenses, retainers).

### Percentage of completion
```
Accrual = Total project cost x % complete - amounts previously recognized
```
Use when: long-term projects or service delivery milestones.

## Reconciliation Format

| Account | GL Balance | Subledger / Support | Difference | Status | Notes |
|---------|-----------|---------------------|------------|--------|-------|

- Differences under $100 (or user-defined threshold): auto-clear
- Differences over threshold: require explanation and resolution
- All reconciliations should be dated and attributed to the preparer

## Journal Entry Validation

When reviewing or generating journal entries, check:
1. **Debits = Credits** (hard stop if they do not)
2. **Valid accounts** - account numbers exist in the chart of accounts
3. **Correct period** - entry is dated within the close period
4. **Description** - clear, includes reference to source document or reason
5. **Reversing entries** - mark accruals that should auto-reverse in the next period
6. **Supporting documentation** - reference to invoice, contract, or calculation

### Standard JE format

| Date | Account | Description | Debit | Credit |
|------|---------|-------------|-------|--------|

## Flux Analysis Thresholds

Default thresholds for flagging (adjust per company):
- P&L accounts: >10% and >$10K change MoM
- Balance sheet accounts: >15% and >$25K change MoM
- Revenue accounts: any negative variance to budget >5%
- New accounts with balances that did not exist in prior month

## Management Reporting Package

Typical contents for a monthly reporting deck:
1. Executive summary (1 page: revenue, EBITDA, cash, key callouts)
2. P&L summary with budget and prior year comparisons
3. Revenue detail by segment/product/geography
4. OpEx detail by department with headcount
5. Balance sheet summary
6. Cash flow summary and 13-week cash forecast (if applicable)
7. KPI scorecard
8. Open items and risks

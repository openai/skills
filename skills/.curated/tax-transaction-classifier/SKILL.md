---
name: "tax-transaction-classifier"
description: "Use when a user asks to classify bank statement transactions for tax preparation, categorize expenses for VAT/GST or income tax, or produce a working paper from a CSV or pasted table of financial transactions. Covers any jurisdiction; defaults to US Schedule C when unspecified."
---

# Tax Transaction Classifier

Classify bank or card transactions into tax categories and produce a structured working paper ready for accountant review.

## Overview

Turn a messy bank export into four structured outputs: a line-by-line working paper, a reviewer brief, an action list, and a review checklist. Every line gets a tax treatment, a confidence label, and plain-language notes.

> **Disclaimer:** This is not tax or legal advice. Rates, thresholds, and form lines change by country and year. Verify amounts and rules against official guidance for the user's jurisdiction and period. A qualified professional must review outputs before filing.

## Inputs

- A CSV file, pasted table, or OCR text of bank/card transactions
- Jurisdiction (optional; defaults to US)
- Entity type (optional; sole trader, company, etc.)
- VAT/GST registration status (optional)

## Workflow

1. **Confirm scope.**
   Ask (if not given): jurisdiction, tax year or period, entity type, and VAT/GST registration status. If declined, default to **Needs Input** for any line that depends on that fact.

2. **Normalize the ledger.**
   Build an internal table: date, description, payee, amount in/out, currency, running balance if provided. Flag duplicates, obvious transfers between own accounts, and FX if multi-currency.

3. **Classify in three passes.**
   - **Pass A — Mechanical:** fees, interest, taxes, payroll, loan principal/repayments using clear labels.
   - **Pass B — Supplier heuristics:** match common merchants (utilities, software subscriptions, fuel) to likely categories; if ambiguous, mark **Assumed** or **Needs Input**.
   - **Pass C — VAT logic (if registered):** identify sales vs purchases, exempt supplies, reverse charge indicators, and missing invoices.

4. **Label every line with exactly one outcome.**
   - **Classified** — enough facts to apply a rule.
   - **Assumed** — a fact is missing; a conservative default was applied. State the assumption and estimated cash impact.
   - **Needs Input** — cannot proceed without one targeted question.

5. **Apply conservative defaults.**
   When uncertain, choose the treatment that tends to increase tax or reduce deductions. Reviewers can unwind an over-conservative line; they cannot always fix an aggressive one.

6. **Produce four outputs.**
   - **Working paper:** table with Date | Description | Amount | Category | Tax treatment | Outcome | Notes.
   - **Reviewer brief:** grouped assumptions, sorted by approximate money impact.
   - **Action list:** documents to fetch, registrations to confirm, corrections to bank labels.
   - **Review checklist:** yes/no items for the accountant.

7. **Privacy.**
   Redact account numbers in examples. Do not store or transmit unnecessary PII.

## Example

**User:** "Classify these lines for my 2025 taxes (USD). I'm a freelance developer filing Schedule C."

| Date | Description | Amount |
|------|-------------|-------:|
| 2025-03-02 | ZELLE FROM ACME CORP | 4,500.00 |
| 2025-03-05 | COMCAST BUSINESS INTERNET | -89.99 |
| 2025-03-12 | VERIZON WIRELESS | -65.00 |
| 2025-03-15 | AMZN MKTP US*AWS | -142.00 |
| 2025-03-22 | STARBUCKS STORE 1847 | -7.25 |

**Output** (abbreviated working paper):

| Date | Description | Amount | Category | Schedule C line | Outcome | Notes |
|------|-------------|-------:|----------|-----------------|---------|-------|
| 2025-03-02 | ZELLE FROM ACME CORP | 4,500.00 | Client receipt | Line 1 — Gross receipts | **Needs Input** | Confirm business income; check if Acme issues 1099-NEC. |
| 2025-03-05 | COMCAST BUSINESS INTERNET | -89.99 | Utilities | Line 25 — Utilities | **Assumed** | Assumed 100% business; if home office, apportion. |
| 2025-03-12 | VERIZON WIRELESS | -65.00 | Telecom | Line 25 — Utilities | **Assumed** | Assumed business phone; if personal line, apportion. |
| 2025-03-15 | AMZN MKTP US*AWS | -142.00 | Cloud/software | Line 18 — Office expense | **Classified** | AWS hosting — deductible; keep invoice. |
| 2025-03-22 | STARBUCKS STORE 1847 | -7.25 | Meals | 50% deductible or personal | **Needs Input** | Client meeting? If yes, 50% deductible; if personal, exclude. |

Full run must include reviewer brief, action list, and review checklist.

## Tips

- Run monthly so missing invoices are easier to find.
- Keep original bank files immutable; work in a copy.
- Attach receipts for any line where a deduction is claimed.

**Inspired by:** [OpenAccountants](https://github.com/openaccountants/openaccountants) — 371 open-source tax classification skills across 134 countries.

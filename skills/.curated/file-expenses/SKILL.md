---
name: file-expenses
description: Prepare and file employee expense reports through a web expense portal using receipts and user-provided details. Use when the user asks to file, submit, enter, reconcile, or organize business expenses, reimbursements, receipts, mileage, or an expense report. Draft and validate reports autonomously, but require the user's review before any final submission, certification, or attestation.
---

# File Expenses

## Workflow

1. Identify the expense portal and source materials.
   - Prefer an existing authenticated browser session when the user requests browser use.
   - Locate receipts and expense details only in locations the user identifies or authorizes.
   - Ask one concise question when the portal, receipt location, or reporting period cannot be discovered.

2. Build an expense manifest before entering data.
   Capture for every expense:
   - transaction date
   - merchant
   - amount and currency
   - category
   - business purpose
   - project, client, cost center, or attendees when applicable
   - receipt path or URL
   - tax or VAT amount when shown

3. Validate the manifest.
   - Match amounts and dates to receipts.
   - Detect duplicates, missing receipts, unreadable receipts, and inconsistent currencies.
   - Apply the organization's expense policy when available.
   - Never invent a merchant, amount, category, business purpose, attendee, or receipt.
   - Clearly mark uncertain or missing values and ask the user only for those values.

4. Prepare the expense report.
   - Create or open the appropriate report for the reporting period.
   - Enter validated fields and attach the corresponding receipt to each expense.
   - Preserve receipt files and do not alter their contents.
   - Save as a draft whenever the portal supports drafts.

5. Review before submission.
   - Summarize the number of expenses, total by currency, missing information, policy warnings, and any assumptions.
   - Show the user the final report state before submitting.
   - Stop before clicking any button that submits, certifies, attests, or declares the report accurate.
   - Submit only after the user explicitly confirms the reviewed final report.

6. Confirm the outcome.
   - Record the report name or ID, submitted total, submission date, and resulting status.
   - Report any portal errors or expenses left unfiled.

## Safety

- Treat expense filing as a financial record and employee attestation.
- Do not classify personal spending as business spending without explicit user confirmation.
- Do not bypass approval controls, receipt requirements, policy checks, or portal warnings.
- Do not submit an expense with unresolved required fields.
- Do not expose sensitive payment, identity, or receipt data outside the authorized portal.


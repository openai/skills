# Checklist Template

Copy only the sections that apply to the app under test. Add app-specific journeys, roles, integrations, and release risks.

## Setup and access

- [ ] Install and start the app successfully
- [ ] Confirm required environment variables, services, and fixtures
- [ ] Confirm available test accounts, roles, and permissions
- [ ] Confirm logs or errors are visible somewhere useful

## Smoke pass

- [ ] App loads without fatal errors
- [ ] Main route or landing screen renders correctly
- [ ] Basic navigation works
- [ ] Critical dependencies respond

## Core user journeys

- [ ] Primary persona can complete the main task end to end
- [ ] Data written in one step appears correctly in later steps
- [ ] Refresh or reopen does not corrupt the flow
- [ ] Success states are clear and trustworthy

## Inputs and validation

- [ ] Required fields enforce constraints
- [ ] Boundary values behave correctly
- [ ] Invalid formats show useful errors
- [ ] Duplicate submissions and rapid repeat actions are handled safely

## Permissions and roles

- [ ] Signed-out behavior is correct
- [ ] Low-privilege users cannot access restricted actions
- [ ] Role changes take effect correctly
- [ ] Unauthorized API calls fail safely

## State and resilience

- [ ] Retry, cancel, back, and refresh behave safely
- [ ] Slow or failed network calls surface actionable feedback
- [ ] Partial failures do not leave corrupted state
- [ ] Concurrent edits or repeated requests are handled correctly

## Integrations and assets

- [ ] External services return expected outcomes or fail safely
- [ ] Uploads, downloads, payments, emails, or webhooks behave correctly
- [ ] Background jobs reflect status in the app
- [ ] Audit trails or logs capture important actions when relevant

## Broader quality

- [ ] Layout works on target device sizes and browsers
- [ ] Keyboard and screen-reader basics are usable
- [ ] Dates, currency, locale, and timezone behavior are correct
- [ ] Performance is acceptable on critical flows

## Closeout

- [ ] Findings are documented with repro steps and impact
- [ ] Failed and blocked items are called out explicitly
- [ ] Remaining risk areas are listed

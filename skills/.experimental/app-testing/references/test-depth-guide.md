# Deep Testing Guide

Use this after the checklist exists and the smoke pass is complete.

## Expand around every important flow

For each important journey, probe:

- Entry
- Success
- Failure
- Retry
- Cancel
- Refresh or reopen
- Timeout or slow dependency
- Duplicate submit
- Permission change
- Stale session or expired token

## Web app heuristics

- Check deep links, browser back and forward, reload, and tab restore.
- Check form preservation, loading states, and optimistic UI.
- Check upload and download flows, clipboard behavior, and keyboard navigation.
- Check responsive layouts, overflow, focus handling, and error visibility.
- Check cache, local storage, and session transitions across tabs when relevant.

## Mobile and desktop heuristics

- Check relaunch, background and foreground transitions, and interrupted flows.
- Check poor network behavior, offline states, and recovery.
- Check OS permissions such as files, camera, notifications, or location when relevant.
- Check device-specific layout, scaling, and input behavior.

## API-backed and data-heavy heuristics

- Check idempotency, retries, pagination, sorting, and filtering.
- Check stale reads, race conditions, and partial writes.
- Check webhook retries, duplicate events, and eventual consistency.
- Check validation on both client and server boundaries.

## Data integrity checks

- Verify user-visible state against persisted state when possible.
- Check create, edit, delete, rollback, and cross-role visibility paths.
- Look for duplicate records, orphaned records, mismatched counts, or stuck jobs.

## Severity calibration

- Critical: data loss, auth bypass, payment or security failure, or app unusable.
- High: main flow blocked, incorrect persistent state, or major integration failure.
- Medium: degraded flow with workaround, incorrect validation, or notable UX break.
- Low: copy, layout, or polish issue with minor impact.

## Reporting minimum

Include:

- Environment or build under test
- Preconditions
- Steps to reproduce
- Expected result
- Actual result
- Evidence
- Scope or suspected blast radius

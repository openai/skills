---
name: internal-comms
description: Draft or polish internal communications such as 3P updates, leadership notes, incident follow-ups, company newsletters, FAQs, launch announcements, and status reports. Use when the task is to turn raw notes, tickets, meeting takeaways, or source documents into a concise internal message matched to a specific audience and format.
---

# Internal Comms

## Overview

Use this skill to turn scattered facts into clear internal communication that is easy for teammates, leaders, or the whole company to scan. Pick the format first, mine only the relevant facts, then write with the audience's context and decision needs in mind.

## Workflow

1. Identify the audience, goal, and time window. Infer these from the request when possible; only ask if the structure would change materially.
2. Choose the communication format and load the matching reference:
   - `references/3p-updates.md` for weekly or sprint-style Progress / Plans / Problems updates
   - `references/company-newsletter.md` for broad multi-team or company-wide roundups
   - `references/faq-answers.md` for recurring questions and concise answer sets
   - `references/general-comms.md` for leadership notes, incident updates, launch announcements, project updates, and other one-off internal messages
3. Gather facts from the artifacts already in reach first: user notes, docs, tickets, specs, meeting notes, drafts, changelogs, or chat exports.
4. If connected tools exist and the user wants a fuller roundup, use them selectively to confirm dates, pull authoritative language, or find missing context.
5. Draft with signal over flourish. Lead with outcomes, decisions, impact, risks, and next actions.
6. Review for accuracy, audience fit, and confidentiality before delivering.

## Writing Rules

- Do not invent facts, timelines, metrics, or alignment. If something is uncertain, say so plainly.
- Prefer concrete nouns and verbs over abstract status language. "Shipped the billing retry fix" is better than "made progress on billing."
- Match the audience's depth. Executives usually need outcomes, risk, and asks; broader audiences need context and decisions; operators need status and action items.
- Keep action items explicit. If people need to do something, say what, by when, and who owns it when known.
- Use links or file references to authoritative sources when they exist.
- Remove sensitive details that the target audience does not need.

## Source Prioritization

Use sources in this order unless the user says otherwise:

- User-provided bullets, notes, and drafts
- Workspace artifacts such as docs, tickets, changelogs, and meeting notes
- Connected systems or shared tools, if available and appropriate
- Prior internal language that sets style or precedent

If the available material is thin, produce the best draft you can, clearly mark assumptions, and list the smallest missing facts needed to finalize it.

## Deliverables

- Deliver the message in the exact format the user requested when one is specified.
- If no format is specified, choose the closest matching reference and state the format briefly.
- When useful, provide both a polished version and a shorter variant for chat, email, or announcement channels.

# Sample Readiness Report

```text
Agent Readiness Score: 74%
Verdict: Pass

Pillar breakdown:
- Metadata: 80%
- Errors: 60%
- Introspection: 70%
- Naming: 85%
- Predictability: 75%
- Documentation: 72%
- Performance: 68%
- Discoverability: 82%

Top fixes:
1. Add structured error schemas for all 4xx and 5xx responses.
2. Add missing parameter descriptions for search and pagination inputs.
3. Document rate limits and return 429 responses consistently.
4. Apply explicit auth requirements to 3 protected endpoints.
5. Add examples for the highest-traffic write endpoints.
```

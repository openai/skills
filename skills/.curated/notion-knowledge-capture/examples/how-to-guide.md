# Example: How-To Guide from Discussion

**User Request**: "Save our discussion about deploying to production as a how-to guide"

## Workflow

### 1. Extract Content from Chat
From conversation, identified:
- Deployment prerequisites
- Step-by-step procedure
- Common issues and solutions
- Best practices and tips

### 2. Structure as How-To
Organized into:
- Overview & prerequisites
- Numbered deployment steps
- Verification steps
- Troubleshooting section
- Related resources

### 3. Find Location
```
Notion:notion-search
query: "deployment documentation"
```
Found: Engineering Wiki → Deployment section

### 4. Create Guide
```
Notion:notion-create-pages
parent: { page_id: "deployment-section-id" }
```

## Output

```markdown
# How to Deploy to Production

## Overview
Production deployment using GitHub Actions with zero-downtime rolling updates.
**Time Required**: 15-20 minutes | **Complexity**: Intermediate

## Prerequisites
- [ ] PR approved and merged to main
- [ ] All CI tests passing
- [ ] Database migrations reviewed
- [ ] Feature flags configured

## Deployment Steps

1. **Verify main branch is ready**
   ```bash
   git checkout main && git pull
   ```

2. **Tag release**
   ```bash
   git tag -a v1.2.3 -m "Release v1.2.3"
   git push origin v1.2.3
   ```

3. **Trigger deployment**
   - GitHub Actions auto-starts from tag push
   - Monitor: https://github.com/org/repo/actions

4. **Database migrations** (if needed)
   - Auto-run in GitHub Actions
   - Check logs for completion

5. **Verify deployment**
   - Wait for health checks (2-3 min)
   - Test key endpoints
   - Check error rates in Datadog

## Verification Checklist
- [ ] All pods healthy in k8s dashboard
- [ ] Error rate < 0.1% in last 10 min
- [ ] Response time p95 < 500ms
- [ ] Test login flow
- [ ] Check Slack #alerts channel

## Troubleshooting

**Health checks failing**
→ Check pod logs: `kubectl logs -f deployment/api -n production`

**Migration errors**
→ Rollback: Revert tag, migrations auto-rollback

**High error rate**
→ Emergency rollback: Previous tag auto-deploys via GitHub Actions

## Best Practices
- Deploy during low-traffic hours (2-4am PST)
- Have 2 engineers available
- Monitor for 30 min post-deploy
- Update #engineering Slack with deploy notice

## Related Docs
- <mention-page url="...">Rollback Procedure</mention-page>
- <mention-page url="...">Database Migration Guide</mention-page>
```

### 5. Make Discoverable
```
Notion:notion-update-page
page_id: "engineering-wiki-homepage"
command: "insert_content_after"
```
Added link in Engineering Wiki → How-To Guides section

## Key Success Factors
- Captured tribal knowledge from discussion
- Structured as actionable steps
- Included troubleshooting from experience
- Made discoverable by linking from wiki index
- Added metadata (time, complexity)

# Example: Conversation to FAQ

## User Request

> "Save this conversation about deployment troubleshooting to the FAQ"

**Context**: User just had a conversation explaining how to troubleshoot common deployment errors.

## Conversation Summary

The conversation covered:
1. **Question**: "Why does deployment fail with 'port already in use' error?"
2. **Answer**: Process from previous deployment still running, need to kill it
3. **Question**: "How do I find and kill the process?"
4. **Commands shared**: `lsof -ti:3000 | xargs kill -9` or use `pm2 restart app`
5. **Question**: "What about 'cannot connect to database' errors?"
6. **Answer**: Check database credentials, verify database is running, check network connectivity
7. **Best practice**: Always check logs first (`pm2 logs` or `docker logs`)

## Workflow Execution

### Step 1: Identify Content Type

This is Q&A content → **FAQ Entry** format is appropriate

### Step 2: Structure FAQ Entries

Extract distinct Q&A pairs from conversation:

**FAQ 1**: Port already in use error
**FAQ 2**: Cannot connect to database error
**FAQ 3**: General troubleshooting approach

### Step 3: Determine Destination

```
Notion:notion-search
query: "FAQ deployment"
query_type: "internal"
```

Found: "Deployment FAQ" database in Engineering Docs

```
Notion:notion-fetch
id: "deployment-faq-database-id"
```

**Schema**:
- Question (title)
- Category (select): Deployment, Configuration, Troubleshooting, etc.
- Tags (multi_select)
- Last Reviewed (date)

### Step 4: Create FAQ Entries

**FAQ Entry 1: Port Already in Use**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "Question": "Why does deployment fail with 'port already in use' error?",
    "Category": "Troubleshooting",
    "Tags": "deployment, errors, ports",
    "date:Last Reviewed:start": "2025-10-14",
    "date:Last Reviewed:is_datetime": 0
  },
  content: "## Short Answer\n\nThe deployment port (usually 3000) is still occupied by a process from a previous deployment. You need to kill the existing process before deploying again.\n\n## Detailed Explanation\n\nWhen you deploy the application, it tries to bind to a specific port (e.g., port 3000). If a previous deployment didn't shut down cleanly, that process may still be running and holding the port. This prevents the new deployment from starting.\n\n**Common causes**:\n- Previous deployment crashed without cleanup\n- Manual `node` process started and forgotten\n- PM2 or other process manager didn't restart properly\n- Multiple deployments attempted simultaneously\n\n## Solution\n\n### Option 1: Kill the process using the port\n\n```bash\n# Find and kill process on port 3000\nlsof -ti:3000 | xargs kill -9\n```\n\nReplace `3000` with your application's port number.\n\n### Option 2: If using PM2\n\n```bash\n# Restart the application\npm2 restart app\n\n# Or delete and restart\npm2 delete app\npm2 start app.js --name app\n```\n\n### Option 3: Check all node processes\n\n```bash\n# List all node processes\nps aux | grep node\n\n# Kill specific process by PID\nkill -9 <PID>\n```\n\n## Prevention\n\n1. **Use process managers**: PM2, systemd, or Docker handle cleanup automatically\n2. **Graceful shutdown**: Implement proper shutdown handlers in your app\n3. **Health checks**: Monitor if previous deployment shut down before starting new one\n\n```javascript\n// Graceful shutdown example\nprocess.on('SIGTERM', () => {\n  server.close(() => {\n    console.log('Server closed');\n    process.exit(0);\n  });\n});\n```\n\n## Verification\n\nAfter killing the process, verify the port is free:\n\n```bash\nlsof -ti:3000\n# Should return nothing if port is free\n```\n\n## Related Questions\n- <mention-page url=\"...\">How do I check what's using a port?</mention-page>\n- <mention-page url=\"...\">How do I configure the application port?</mention-page>\n- <mention-page url=\"...\">PM2 deployment best practices</mention-page>\n\n## Last Updated\nOctober 14, 2025"
}]
```

**FAQ Entry 2: Database Connection Errors**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "Question": "Why do I get 'cannot connect to database' errors during deployment?",
    "Category": "Troubleshooting",
    "Tags": "deployment, database, errors",
    "date:Last Reviewed:start": "2025-10-14",
    "date:Last Reviewed:is_datetime": 0
  },
  content: "## Short Answer\n\nDatabase connection errors usually mean either the database isn't running, credentials are incorrect, or there's a network connectivity issue. Check database status, verify credentials, and test connectivity.\n\n## Detailed Explanation\n\nThe application can't establish a connection to the database during startup. This prevents the application from initializing properly.\n\n**Common causes**:\n- Database service isn't running\n- Incorrect connection credentials\n- Network connectivity issues (firewall, security groups)\n- Database host/port misconfigured\n- Database is at connection limit\n- SSL/TLS configuration mismatch\n\n## Troubleshooting Steps\n\n### Step 1: Check database status\n\n```bash\n# For local PostgreSQL\npg_isready -h localhost -p 5432\n\n# For Docker\ndocker ps | grep postgres\n\n# For MongoDB\nmongosh --eval \"db.adminCommand('ping')\"\n```\n\n### Step 2: Verify credentials\n\nCheck your `.env` or configuration file:\n\n```bash\n# Common environment variables\nDB_HOST=localhost\nDB_PORT=5432\nDB_NAME=myapp_production\nDB_USER=myapp_user\nDB_PASSWORD=***********\n```\n\nTest connection manually:\n\n```bash\n# PostgreSQL\npsql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME\n\n# MongoDB\nmongosh \"mongodb://$DB_USER:$DB_PASSWORD@$DB_HOST:$DB_PORT/$DB_NAME\"\n```\n\n### Step 3: Check network connectivity\n\n```bash\n# Test if port is reachable\ntelnet $DB_HOST $DB_PORT\n\n# Or using nc\nnc -zv $DB_HOST $DB_PORT\n\n# Check firewall rules (if applicable)\nsudo iptables -L\n```\n\n### Step 4: Check application logs\n\n```bash\n# PM2 logs\npm2 logs app\n\n# Docker logs\ndocker logs container-name\n\n# Application logs\ntail -f /var/log/app/error.log\n```\n\nLook for specific error messages:\n- `ECONNREFUSED`: Database not running or wrong host/port\n- `Authentication failed`: Wrong credentials\n- `Timeout`: Network/firewall issue\n- `Too many connections`: Database connection limit reached\n\n## Solutions by Error Type\n\n### Database Not Running\n\n```bash\n# Start PostgreSQL\nsudo systemctl start postgresql\n\n# Start via Docker\ndocker start postgres-container\n```\n\n### Wrong Credentials\n\n1. Reset database password\n2. Update `.env` file\n3. Restart application\n\n### Connection Limit Reached\n\n```sql\n-- Check current connections (PostgreSQL)\nSELECT count(*) FROM pg_stat_activity;\n\n-- Increase max connections\nALTER SYSTEM SET max_connections = 200;\n```\n\n### SSL/TLS Issues\n\nAdd to connection string:\n```\nssl=true&sslmode=require\n```\n\nOr disable SSL for dev:\n```\nsslmode=disable\n```\n\n## Prevention\n\n1. **Connection pooling**: Limits concurrent connections\n```javascript\npool: {\n  min: 2,\n  max: 10\n}\n```\n\n2. **Health checks**: Verify database before starting app\n```javascript\nconst healthCheck = async () => {\n  try {\n    await db.raw('SELECT 1');\n    console.log('Database connected');\n  } catch (err) {\n    console.error('Database connection failed:', err);\n    process.exit(1);\n  }\n};\n```\n\n3. **Retry logic**: Auto-reconnect on temporary failures\n```javascript\nretry: {\n  max: 3,\n  backoff: 1000\n}\n```\n\n4. **Environment validation**: Check all required env vars exist\n```javascript\nconst required = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'];\nfor (const key of required) {\n  if (!process.env[key]) {\n    throw new Error(`Missing required env var: ${key}`);\n  }\n}\n```\n\n## Related Questions\n- <mention-page url=\"...\">How do I configure database connection pooling?</mention-page>\n- <mention-page url=\"...\">Database backup and restore procedures</mention-page>\n- <mention-page url=\"...\">Database performance optimization</mention-page>\n\n## Last Updated\nOctober 14, 2025"
}]
```

**FAQ Entry 3: General Troubleshooting**

```
Notion:notion-create-pages

parent: { data_source_id: "collection://faq-db-uuid" }

pages: [{
  properties: {
    "Question": "What's the first thing I should check when deployment fails?",
    "Category": "Troubleshooting",
    "Tags": "deployment, debugging, best-practices",
    "date:Last Reviewed:start": "2025-10-14",
    "date:Last Reviewed:is_datetime": 0
  },
  content: "## Short Answer\n\n**Always check the logs first.** Logs contain error messages that point you directly to the problem. Use `pm2 logs`, `docker logs`, or check your application's log files.\n\n## Detailed Explanation\n\nLogs are your first and most important debugging tool. They show:\n- Exact error messages\n- Stack traces\n- Timing information\n- Configuration issues\n- Dependency problems\n\nMost deployment issues can be diagnosed and fixed by reading the logs carefully.\n\n## How to Check Logs\n\n### PM2\n\n```bash\n# View all logs\npm2 logs\n\n# View logs for specific app\npm2 logs app-name\n\n# View only errors\npm2 logs --err\n\n# Follow logs in real-time\npm2 logs --lines 100\n```\n\n### Docker\n\n```bash\n# View logs\ndocker logs container-name\n\n# Follow logs\ndocker logs -f container-name\n\n# Last 100 lines\ndocker logs --tail 100 container-name\n\n# With timestamps\ndocker logs -t container-name\n```\n\n### Application Logs\n\n```bash\n# Tail application logs\ntail -f /var/log/app/app.log\ntail -f /var/log/app/error.log\n\n# Search logs for errors\ngrep -i error /var/log/app/*.log\n\n# View logs with context\ngrep -B 5 -A 5 \"ERROR\" app.log\n```\n\n## Systematic Troubleshooting Approach\n\n### 1. Check the logs\n- Read error messages carefully\n- Note the exact error type and message\n- Check timestamps to find when error occurred\n\n### 2. Verify configuration\n- Environment variables set correctly?\n- Configuration files present and valid?\n- Paths and file permissions correct?\n\n### 3. Check dependencies\n- All packages installed? (`node_modules` present?)\n- Correct versions installed?\n- Any native module compilation errors?\n\n### 4. Verify environment\n- Required services running (database, Redis, etc.)?\n- Ports available?\n- Network connectivity working?\n\n### 5. Test components individually\n- Can you connect to database manually?\n- Can you run application locally?\n- Do health check endpoints work?\n\n### 6. Check recent changes\n- What changed since last successful deployment?\n- New dependencies added?\n- Configuration modified?\n- Environment differences?\n\n## Common Error Patterns\n\n### \"Module not found\"\n```bash\n# Solution: Install dependencies\nnpm install\n# or\nnpm ci\n```\n\n### \"Permission denied\"\n```bash\n# Solution: Fix file permissions\nchmod +x start.sh\nsudo chown -R appuser:appuser /app\n```\n\n### \"Address already in use\"\n```bash\n# Solution: Kill process on port\nlsof -ti:3000 | xargs kill -9\n```\n\n### \"Cannot connect to...\"\n```bash\n# Solution: Verify service is running and reachable\ntelnet service-host port\n```\n\n## Debugging Tools\n\n### Log Aggregation\n- **PM2**: Built-in log management\n- **Docker**: Centralized logging with log drivers\n- **ELK Stack**: Elasticsearch, Logstash, Kibana for large scale\n- **CloudWatch**: For AWS deployments\n\n### Monitoring\n- **PM2 Monit**: `pm2 monit` for real-time metrics\n- **Docker Stats**: `docker stats` for resource usage\n- **System metrics**: `top`, `htop` for CPU/memory\n\n### Network Debugging\n```bash\n# Check open connections\nnetstat -tulpn\n\n# Check specific port\nlsof -i :3000\n\n# Test connectivity\ncurl http://localhost:3000/health\n```\n\n## When to Escalate\n\nEscalate to senior team member if:\n- Error message is cryptic and not Google-able\n- Problem persists after trying obvious solutions\n- Production is affected\n- Data integrity may be compromised\n- Security-related errors\n\n## Prevention\n\n1. **Automated health checks** before deployment\n2. **Staged deployments** (dev → staging → production)\n3. **Rollback plan** ready for quick recovery\n4. **Monitoring and alerts** for early problem detection\n5. **Deployment checklist** to ensure all steps followed\n\n## Related Questions\n- <mention-page url=\"...\">How do I set up log aggregation?</mention-page>\n- <mention-page url=\"...\">Deployment checklist and best practices</mention-page>\n- <mention-page url=\"...\">How to roll back a failed deployment?</mention-page>\n\n## Last Updated\nOctober 14, 2025"
}]
```

### Step 5: Update FAQ Index

```
Notion:notion-fetch
id: "faq-index-page-id"
```

```
Notion:notion-update-page
page_id: "faq-index-page-id"
command: "insert_content_after"
selection_with_ellipsis: "## Deployment & Troubleshooting..."
new_str: "
- <mention-page url=\"...\">Why does deployment fail with 'port already in use' error?</mention-page>
- <mention-page url=\"...\">Why do I get 'cannot connect to database' errors?</mention-page>
- <mention-page url=\"...\">What's the first thing I should check when deployment fails?</mention-page>
"
```

## Summary Provided to User

```markdown
## FAQ Entries Created ✅

### Conversation Captured
Transformed deployment troubleshooting conversation into 3 comprehensive FAQ entries.

### FAQ Entries Created

1. **Port Already in Use Error**
   - Problem: Deployment fails due to occupied port
   - Solutions: Kill process, use PM2, check node processes
   - Prevention: Use process managers, graceful shutdown
   - Link: <mention-page url="...">Port already in use FAQ</mention-page>

2. **Database Connection Errors**
   - Problem: Cannot connect to database during deployment
   - Troubleshooting: 4-step systematic approach
   - Solutions: By error type (credentials, network, limits)
   - Prevention: Connection pooling, health checks, retry logic
   - Link: <mention-page url="...">Database connection FAQ</mention-page>

3. **General Troubleshooting Approach**
   - Best practice: Always check logs first
   - Tools: PM2 logs, Docker logs, application logs
   - Systematic approach: 6-step debugging process
   - Common errors: Module not found, permissions, ports
   - Link: <mention-page url="...">Troubleshooting first steps FAQ</mention-page>

### Content Structure

Each FAQ includes:
✅ Short answer (quick reference)
✅ Detailed explanation (full context)
✅ Multiple solution options
✅ Code examples and commands
✅ Prevention strategies
✅ Links to related FAQs
✅ Last updated date

### Database Integration

- ✅ Added to FAQ database (not standalone pages)
- ✅ Properties set: Category (Troubleshooting), Tags, Date
- ✅ FAQ index page updated with links
- ✅ Cross-references between related questions

### Value Added

**From conversation** → **To structured knowledge**:
- Casual Q&A → Professional FAQ entries
- Implicit knowledge → Explicit documentation
- One-time help → Reusable resource
- 5-minute conversation → Permanent team knowledge

**Future benefit**:
- Team can self-serve on common issues
- New team members can onboard faster
- Reduces repeated questions
- Improves troubleshooting speed

**Knowledge captured and preserved! 📚**
```

## Key Features Demonstrated

### Content Extraction
- Identified distinct Q&A pairs from conversation
- Extracted commands, solutions, and best practices
- Preserved troubleshooting workflows

### FAQ Structure
- Short answer for quick reference
- Detailed explanation for understanding
- Multiple solutions (Options 1, 2, 3)
- Code examples with comments
- Prevention strategies
- Related questions linking

### Database Integration
- Created in FAQ database (not standalone)
- Set appropriate properties (category, tags, date)
- Updated index page with links
- Cross-referenced related questions

### Value Transformation
- Converted informal conversation to professional docs
- Added structure, examples, and prevention tips
- Made knowledge searchable and discoverable
- Created permanent team resource

Perfect for: FAQ creation, knowledge preservation, team documentation


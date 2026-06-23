---
name: "mobile-best-practices"
description: "Searchable database of 2,461 mobile development best practices for Android, iOS, Flutter, and React Native. Trigger when the user asks to build, review, or optimize a mobile app, or requests guidance on mobile architecture, security, performance, UI patterns, or anti-patterns."
---

# Mobile Best Practices

## Overview

This skill provides access to a curated database of 2,461 mobile development best practices for Android, iOS, Flutter, and React Native. It covers architecture patterns, security (OWASP Mobile Top 10), performance rules, UI components, anti-patterns, libraries, testing patterns, and copy-paste code snippets.

Use this skill when:
- Building or reviewing Android apps (Jetpack Compose or XML layouts)
- Building or reviewing iOS apps (SwiftUI or UIKit)
- Working on Flutter or React Native projects
- Selecting architecture patterns (MVVM, MVI, Clean Architecture, BLoC)
- Auditing mobile security against OWASP Mobile Top 10
- Optimizing performance and preventing ANR/crashes
- Choosing libraries and Gradle dependencies

## Workflow

### Step 1 — Identify the platform and task

Determine the target platform (Android, iOS, Flutter, React Native) and the type of guidance needed (architecture, security, performance, UI, testing, etc.).

### Step 2 — Search the database

Use the search script to find relevant best practices:

```bash
python3 search.py "<query>" --domain <domain> -n 5
```

Available domains:

| Domain | Description |
|--------|-------------|
| `architecture` | MVVM, MVI, Clean Architecture, BLoC, Redux |
| `design-patterns` | Repository, Factory, Observer, Singleton |
| `ui` | Compose, SwiftUI, UIKit, Flutter widgets |
| `anti-patterns` | Common mistakes and how to avoid them |
| `security` | OWASP Mobile Top 10, encryption, data storage |
| `performance` | Recomposition, memory, rendering, battery |
| `testing` | Unit, UI, integration, snapshot testing |
| `libraries` | Recommended third-party libraries |
| `snippets` | Copy-paste code examples |
| `gradle` | Dependency declarations with versions |

Search across all domains:

```bash
python3 search.py "<query>" --all-domains -n 10
```

### Step 3 — Apply the results

Use the returned best practices to:
- Write new code following platform-specific guidelines
- Identify and fix anti-patterns in existing code
- Suggest architecture improvements
- Flag security vulnerabilities with OWASP references
- Recommend performance optimizations

## Search Examples

```bash
# Jetpack Compose performance
python3 search.py "jetpack compose recomposition" --domain performance

# API key security
python3 search.py "API key storage" --domain security

# Flutter state management
python3 search.py "flutter state management" --domain architecture

# React Native memory leaks
python3 search.py "react native memory leak" --domain anti-patterns

# Biometric authentication
python3 search.py "biometric authentication" --all-domains

# Gradle dependency for networking
python3 search.py "retrofit okhttp" --domain gradle
```

## Database Coverage

| Category | Count |
|----------|-------|
| Platform-specific guidelines | 792 |
| Security practices (OWASP-mapped) | 437 |
| Performance rules | 228 |
| Anti-patterns | 243 |
| UI component patterns | 191 |
| Design patterns | 112 |
| Architecture patterns | 49 |
| Libraries & dependencies | 103 |
| Testing patterns | 73 |
| Copy-paste snippets | 81 |
| Gradle dependencies | 78 |
| **Total** | **2,461** |

## Installation

```bash
npx mobile-best-practices install
```

Or install via Codex skill installer:

```
$skill-installer install https://github.com/openai/skills/tree/main/skills/.curated/mobile-best-practices
```

## Source

https://github.com/tungnk123/mobile-best-practices — MIT License

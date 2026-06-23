---
name: copr-cli
description: Operate Fedora COPR from the terminal with reliable command mapping for projects, builds, chroots, packages, permissions, and webhooks. Use when a task asks for copr-cli usage, fixing/diagnosing copr-cli command mistakes, selecting the right subcommand/options, or performing direct COPR API v3 requests with curl.
---

# Copr CLI

Use this skill to execute COPR workflows without trial-and-error across unrelated subcommands.

## Workflow

1. Identify the requested object and action first.
- Objects: project, build, chroot, package, permissions, webhook, monitor.
- Actions: create, list, get, edit/modify, build, cancel, delete, download, request permission.

2. Map request to subcommand from the action map below.
- Start with `references/live-help/` for current installed command usage and options.
- Use `references/copr-cli-manual.asciidoc` for deeper option details and examples.
- Do not brute-force `--help` across all subcommands.
- Run targeted `copr-cli <subcommand> --help` only when one option remains ambiguous.

3. Validate authentication/context before mutating state.
- Run `copr-cli whoami` for authenticated identity.
- Confirm target `<owner>/<project>` and chroot names before `modify`, `delete`, `edit-chroot`, or `cancel`.

4. Execute and verify.
- For builds: capture build ID, then `copr-cli status <id>` or `copr-cli watch-build <id>`.
- For repository regeneration: run `copr-cli regenerate-repos <project>` after impactful changes.

5. Fall back to `curl` only when needed.
- Use `references/copr-api-curl.md` for auth and examples.
- Use `references/copr-api-v3-swagger.json` and `references/copr-api-v3-paths.txt` for endpoint discovery.

## Action Map

- Project lifecycle:
  - Create: `copr-cli create`
  - Read/list: `copr-cli get`, `copr-cli list`
  - Update: `copr-cli modify`
  - Delete/fork: `copr-cli delete`, `copr-cli fork`
  - Regenerate repos: `copr-cli regenerate-repos`

- Builds:
  - Submit SRPM/URL: `copr-cli build`
  - Submit source-specific builds: `buildpypi`, `buildgem`, `buildcustom`, `buildscm`, `build-distgit`
  - Track state: `status`, `watch-build`, `monitor`
  - Manage artifacts/state: `download-build`, `cancel`, `delete-build`, `list-builds`

- Chroots:
  - List available chroots: `copr-cli list-chroots`
  - Read/edit project chroot settings: `get-chroot`, `edit-chroot`
  - Generate mock profile: `mock-config`

- Packages:
  - Add/edit source definitions: `add-package-*`, `edit-package-*`
  - Enumerate/read: `list-packages`, `list-package-names`, `get-package`
  - Lifecycle: `delete-package`, `reset-package`, `build-package`

- Permissions and identity:
  - Identity/token/webhook secret: `whoami`, `new-api-token`, `new-webhook-secret`
  - Roles: `list-permissions`, `edit-permissions`, `request-permissions`

## Resources

- Full CLI manual: `references/copr-cli-manual.asciidoc`
- Current installed top-level help: `references/live-help/00-top-level.help.txt`
- Current installed subcommand index: `references/live-help/subcommands.txt`
- Per-subcommand live help files: `references/live-help/`
- CLI examples: `references/copr-cli-cheat.txt`
- API v3 endpoint index: `references/copr-api-v3-paths.txt`
- API v3 schema: `references/copr-api-v3-swagger.json`
- API curl guide: `references/copr-api-curl.md`
- API client docs: `references/copr-api-client-v3.rst`, `references/copr-api-build-options.rst`, `references/copr-api-package-source-types.rst`

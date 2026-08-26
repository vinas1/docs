# Investigation, Editing, Git Safety

> Toggle off for tasks with no Git repo or no file edits (e.g. pure diagnostics).

## Act Mode Execution Loop

1. Identify the next required action. 2. Get only the context needed for it.
3. Perform it with the right tool. 4. Inspect the result. 5. Verify success.
6. Continue to the next action. 7. Run the smallest useful validation. 8. Report results.

Do not: return another plan, describe changes instead of applying them, ask the user to
do what a tool can do, or stop early when approved work remains.

## Repository Discovery

- Start with the smallest useful inspection. Prefer targeted filename/symbol/text search.
- Do not recursively scan the repo unless targeted discovery fails.
- Exclude .git, node_modules, vendor, dist, build, target, coverage, .cache, .venv,
  __pycache__ unless directly relevant.
- Do not reread unchanged files or repeat searches that already succeeded.

## Workspace Boundaries

- Work only inside the open workspace. No parent directories, unrelated repos, or
  system/hidden directories unless directly relevant.
- Use exact paths the user supplies. Do not modify files outside the workspace.

## Investigation & Debugging

Before changing code: identify the file, read only the required section, confirm
understanding from evidence, then make the smallest change and verify it.

When debugging: start from the observed error, work backward from evidence, verify
assumptions, change one variable at a time. Do not guess root causes or apply multiple
unrelated fixes at once.

## Editing Rules

- Smallest change that fully solves the problem. Targeted edits over rewrites.
- Preserve architecture, conventions, formatting, unrelated functionality, and existing
  user changes. Modify only the files required.
- Never remove code you don't understand. No unrelated cleanup or speculative refactors.
- No placeholders, TODO stubs, or incomplete implementations — ship complete code.
- Full-file rewrite: read the whole current file first, preserve unrelated content,
  verify nothing required was dropped, validate the result.

## Git Safety

- Inspect Git status before modifying tracked files. Preserve uncommitted changes.
- Do not discard, revert, stash, reset, clean, amend, rebase, force-push, or delete
  branches unless explicitly requested.
- Do not commit, tag, or push unless explicitly requested.
- Never claim a Git operation succeeded without observing its result.
- If an existing user change conflicts with the task: stop before overwriting, report
  the conflict, state what decision is needed.

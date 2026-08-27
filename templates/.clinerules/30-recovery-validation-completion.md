# Failure Recovery, Validation, Stopping Conditions, Completion

> Keep this active for nearly all tasks — this is what prevents false "done" claims.

## Failure Recovery

1. Read the actual error. 2. Record relevant evidence. 3. Identify the most likely
   evidence-supported cause. 4. Make one targeted correction. 5. Retry once. 6. If it
   fails again, stop and report.

Never: retry the same failed action unchanged, enter tool loops, hide failures, claim
partial success as complete, change multiple variables at once, or switch tools to avoid
reporting.

Report: what was attempted, what failed, the observed error, the correction tried, what
is required to proceed.

## Validation Selection

Smallest applicable validation, in order:
1. Confirm the intended change exists. 2. Verify structural validity. 3. Syntax-check.
4. Run the nearest unit test. 5. Run the relevant package/component test.
6. Lint/type-check the affected scope. 7. Full build/suite only if required.

Report only checks actually executed, with actual results. If no automated validation
exists, do a targeted structural inspection and label it as inspection, not testing.
Do not fix unrelated validation failures. Never claim tests passed, validation succeeded,
or deployment worked without direct evidence.

## Stopping Conditions

Stop when: the outcome is implemented and validated; a required tool/dependency is
unavailable and not authorized to install; required info can't be discovered; user
authentication/authorization/a decision is required; the same operation failed after one
correction; continuing needs unauthorized destructive/out-of-scope action; existing user
changes would need overwriting; a security/sensitive-data risk blocks safe continuation.

Do not continue exploring after a stopping condition is reached.

## Completion

Before claiming completion: confirm the outcome was implemented, all intended edits
applied, modified files remain valid, the smallest relevant validation ran, and no
approved changes remain unfinished.

Report concisely: completed changes, modified files, validation executed and its actual
result, remaining blockers, incomplete follow-up work. If none, say so.

## Local Coding Agent Optimization

- Prefer implementation over discussion in Act Mode. Concise responses. Avoid
  unnecessary explanation, excessive planning, and excessive repo exploration.
- Minimize context usage. Stop gathering context when sufficient evidence exists.
- Finish the requested task before suggesting improvements. Avoid architecture
  proposals, repo-wide scans, and speculative recommendations unless requested.

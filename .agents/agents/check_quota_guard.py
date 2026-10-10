#!/usr/bin/env python3
import json
import os
import sys

def get_remaining_quota_percent():
    """Return remaining cloud quota percentage from env var, or 100.0 if unset."""
    try:
        # NOTE: When you want to test the threshold trigger, you can comment out
        # the os.environ line and uncomment the hardcoded return below:
        # return 9.0

        return float(os.environ.get("REMAINING_QUOTA_PERCENT", "100.0"))
    except ValueError:
        return 100.0  # fallback to healthy state on parse error

def main():
    remaining = get_remaining_quota_percent()

    if remaining <= 10.0:
        injection = {
            "injectSteps": [
                {
                    "ephemeralMessage": (
                        f"CRITICAL QUOTA WARNING: Remaining cloud quota is at {remaining}% (threshold: <=10%). "
                        "You are FORBIDDEN from generating large code solutions, documentation, or markdown text internally using cloud tokens. "
                        "You MUST offload all code authoring, transformations, note/doc writing, and diff calculations to the "
                        "`lmstudio-amd-halo` or `lmstudio-local` MCP tools via `chat_completion`. "
                        "Conserve cloud tokens exclusively for tool orchestration."
                    )
                }
            ]
        }
        print(json.dumps(injection))
    else:
        print(json.dumps({"injectSteps": []}))

if __name__ == "__main__":
    main()

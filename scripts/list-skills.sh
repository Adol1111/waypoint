#!/usr/bin/env bash
set -euo pipefail

find skills/waypoints skills/setup skills/workflows -mindepth 2 -maxdepth 2 -name SKILL.md -print \
  | while IFS= read -r skill_file; do
      basename "$(dirname "${skill_file}")"
    done \
  | sort

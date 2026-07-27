#!/usr/bin/env bash
set -euo pipefail

find skills -mindepth 3 -maxdepth 3 -name SKILL.md -print \
  | while IFS= read -r skill_file; do
      basename "$(dirname "${skill_file}")"
    done \
  | sort

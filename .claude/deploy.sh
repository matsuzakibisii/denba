#!/bin/bash
set -e

REPO_DIR="/Users/mat/Documents/Claude/Projects/DENBA"
REMOTE="origin"
BASE_BRANCH="main"

cd "$REPO_DIR"

# Pull latest main first
git pull "$REMOTE" "$BASE_BRANCH" --rebase 2>&1

# Check for changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo '{"systemMessage": "⚠️ デプロイする差分がありません。"}'
  exit 0
fi

# Stage all changes
git add -A

# Commit
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "deploy: update files ${TIMESTAMP}"

# Push directly to main
git push "$REMOTE" "$BASE_BRANCH"

echo "{\"systemMessage\": \"✅ mainにデプロイしました (${TIMESTAMP})\"}"

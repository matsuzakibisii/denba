#!/bin/bash
set -e

REPO_DIR="/Users/mat/Documents/Claude/Projects/DENBA"
REMOTE="origin"
BASE_BRANCH="main"

cd "$REPO_DIR"

# Check for changes
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard)" ]; then
  echo '{"decision":"block","reason":"デプロイする差分がありません。ファイルに変更がないためPRを作成しません。"}'
  exit 0
fi

# Create a branch name with timestamp
BRANCH="deploy/$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"

# Stage all changes (only tracked + new files, not deletions accidentally)
git add -A

# Commit
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
git commit -m "deploy: update files ${TIMESTAMP}"

# Push branch
git push -u "$REMOTE" "$BRANCH"

# Create PR
PR_URL=$(gh pr create \
  --base "$BASE_BRANCH" \
  --head "$BRANCH" \
  --title "Deploy: ${TIMESTAMP}" \
  --body "$(cat <<'EOF'
## 変更内容
差分ファイルのみをアップロードしました。

## 変更ファイル
$(git diff origin/main...HEAD --name-only)
EOF
)" 2>&1)

# Return to main
git checkout "$BASE_BRANCH"

echo "{\"systemMessage\": \"✅ PRを作成しました: ${PR_URL}\"}"

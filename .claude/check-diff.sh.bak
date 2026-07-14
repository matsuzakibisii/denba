#!/bin/bash

REPO_DIR="/Users/mat/Documents/Claude/Projects/DENBA"
cd "$REPO_DIR"

git fetch origin main --quiet 2>/dev/null
git pull origin main --rebase --quiet 2>/dev/null || true

# Get diff of uncommitted changes + untracked files
DIFF=$(git diff HEAD 2>/dev/null)
UNTRACKED=$(git ls-files --others --exclude-standard 2>/dev/null)

if [ -z "$DIFF" ] && [ -z "$UNTRACKED" ]; then
  python3 -c "import json; print(json.dumps({
    'hookSpecificOutput': {
      'hookEventName': 'UserPromptSubmit',
      'additionalContext': '差分はありません。デプロイするファイルがないことをユーザーに伝えてください。'
    }
  }))"
  exit 0
fi

SUMMARY=""
if [ -n "$UNTRACKED" ]; then
  SUMMARY="【新規ファイル】\n$UNTRACKED\n"
fi
if [ -n "$DIFF" ]; then
  SUMMARY="${SUMMARY}【変更内容】\n$(echo "$DIFF" | head -100)"
fi

python3 -c "
import json, sys
summary = sys.argv[1]
msg = f'''以下の差分があります。ユーザーに差分を日本語でわかりやすく表示してください。
その後「この内容でデプロイしますか？」と確認を求めてください。
ユーザーが「はい」「OK」「する」などと答えたら /Users/mat/Documents/Claude/Projects/DENBA/.claude/deploy.sh を実行してください。

{summary}
'''
print(json.dumps({
  'hookSpecificOutput': {
    'hookEventName': 'UserPromptSubmit',
    'additionalContext': msg
  }
}))
" "$SUMMARY"

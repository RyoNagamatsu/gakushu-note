#!/bin/sh
# stamp a build id into kaede/index.html and kaede/version.json, then commit and push
set -e
cd "$(dirname "$0")"
V=$(date -u +%Y%m%d%H%M%S)
sed -i "s/const BUILD='[^']*';/const BUILD='$V';/" index.html
printf '{"v":"%s"}' "$V" > version.json
git add -A .
git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
${CLAUDE_SESSION_LINE:-}"
git push -q origin main
git log --oneline | head -1

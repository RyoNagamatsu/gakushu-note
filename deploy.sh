#!/bin/sh
# stamp a build id into index.html and version.json, then commit and push
set -e
cd "$(dirname "$0")"
V=$(date -u +%Y%m%d%H%M%S)
sed -i "s/const BUILD='[^']*';/const BUILD='$V';/" index.html
printf '{"v":"%s"}' "$V" > version.json
git add -A
git commit -q -m "$1

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HxiQktTLpK5k1G46nB5u74"
git push -q origin main
git log --oneline | head -1

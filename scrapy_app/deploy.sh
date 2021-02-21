eval "scrapyd &"
PID=$!
scrapyd-deploy
kill $PID

watchmedo shell-command \
  --patterns="*.py" \
  --command='echo "Reload: $(date)" && kill -HUP `cat gunicorn.pid`'

heroku pg:backups:capture
heroku pg:backups:download
"C:\Program Files\PostgreSQL\9.6\bin\pg_restore.exe" --verbose --clean --no-acl --no-owner -h localhost -U postgres -d otsukare latest.dump
pause

"C:\Program Files\PostgreSQL\9.6\bin\pg_dump.exe" -Fc --no-acl --no-owner -h localhost -U postgres otsukare > "C:\Users\Damnt\Dropbox\latest.dump"
pause
heroku pg:backups:restore "https://www.dropbox.com/s/nkibf2dg2k3j5e1/latest.dump?dl=0" DATABASE_URL
heroku ps:restart
pause
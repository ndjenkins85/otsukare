call "C:\Users\Damnt\Anaconda3\Scripts\activate.bat"
cd C:\Users\Damnt\Documents\Otsukare

@echo off
set /p title= Title:
set /p description= Description:
For /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c-%%a-%%b)
For /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)

echo %mydate%_%mytime% >> otsukare/static/changelog.txt 
echo %title% >> otsukare/static/changelog.txt
echo %description% >> otsukare/static/changelog.txt

git add --all
git commit -m %title% -m %description%
git push

git push heroku master
heroku open

heroku logs --tail
call "C:\Users\Damnt\Anaconda3\Scripts\activate.bat"
cd C:\Users\Damnt\Documents\Otsukare

@echo off
set /p title= Title:

git add --all
git commit -m %title%
git push

pause
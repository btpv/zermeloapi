@echo off
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%%ldt:~4,2%%ldt:~6,2%%ldt:~8,2%%ldt:~10,2%
@REM py -m build
@REM py -m twine upload dist/*
@REM rmdir dist /s
git add *
git commit -m build%ldt%
git push -u origin main
echo %ldt%
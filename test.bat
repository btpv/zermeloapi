@echo off
for /f "delims== tokens=1,2" %%G in (D:\pypi_psw\test_pypi.txt) do set %%G=%%H
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%:%ldt:~10,2%
py -m build
py -m twine upload -u btpv -p %testpypi% --repository testpypi dist/*
rmdir dist /s
git add *
git commit -m "test build %ldt%"
git push -u origin main
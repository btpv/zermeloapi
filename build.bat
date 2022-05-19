@echo off
for /f "delims== tokens=1,2" %%G in (D:\pypi_psw\pypi.txt) do set %%G=%%H
for /F "usebackq tokens=1,2 delims==" %%i in (`wmic os get LocalDateTime /VALUE 2^>NUL`) do if '.%%i.'=='.LocalDateTime.' set ldt=%%j
set ldt=%ldt:~0,4%-%ldt:~4,2%-%ldt:~6,2% %ldt:~8,2%:%ldt:~10,2%
C:\Users\Gebruiker\AppData\Local\Temp\build-env-v3ucgwaw\Scripts\python.exe -m build
C:\Users\Gebruiker\AppData\Local\Temp\build-env-v3ucgwaw\Scripts\python.exe -m twine upload -u btpv -p %pypi%  dist/*
rmdir dist /S /Q
rmdir "src/zermeloapi.egg-info" /S /Q
git add *
git commit -m "build %ldt%"
git push -u origin main
pip install --upgrade zermeloapi
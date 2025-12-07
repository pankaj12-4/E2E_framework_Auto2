@echo off
SET ROOT_PATH=C:\Users\singh\PycharmProjects\PythonProject\Interview_7_dec
cd /d "%ROOT_PATH%"
echo Activating virtual environment...
call venv\Scripts\activate
REM Ensure 'Reports' folder exists
if not exist "Reports" (
    mkdir "Reports"
)
echo Running Extract Fail Test...
pytest Tests/Extract_Fail_Test.py --html=Reports\extract_fail_report.html --self-contained-html
echo.
echo Report generated as Reports\extract_fail_report.html
pause

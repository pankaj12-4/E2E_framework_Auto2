@echo off
SET ROOT_PATH=C:\Users\singh\PycharmProjects\PythonProject\Interview_7_dec
cd /d "%ROOT_PATH%"
echo Activating virtual environment...
call venv\Scripts\activate
REM Ensure 'Reports' folder exists
if not exist "Reports" (
    mkdir "Reports"
)
echo Running Login Fail Test...
pytest Tests/Login_Fail_Test.py --html=Reports\login_fail_report.html --self-contained-html
echo.
echo Report generated as Reports\login_fail_report.html
pause
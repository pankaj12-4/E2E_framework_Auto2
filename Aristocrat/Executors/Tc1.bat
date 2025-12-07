@echo off
SET ROOT_PATH=C:\Users\singh\PycharmProjects\PythonProject\Interview_7_dec
cd /d "%ROOT_PATH%"
echo Activating virtual environment...
call venv\Scripts\activate
REM Ensure 'reports' folder exists
if not exist "Reports" (
    mkdir "Reports"
)
echo Running Login Success Test...
pytest Tests/Login_Success_Test.py --html=reports\login_success_report.html --self-contained-html
REM python -m pytest Tests/Login_Success_Test.py --html=report.html --self-contained-html
echo.
echo Report generated as report.html
pause

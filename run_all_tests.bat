@echo off
REM This batch file runs pytest tests and generates Allure reports

SET PROJECT_DIR=%~dp0
SET RESULTS_DIR=%PROJECT_DIR%allure-results
SET REPORT_DIR=%PROJECT_DIR%allure-report
SET HISTORY_DIR=%PROJECT_DIR%allure-report\history

REM Clean previous test results
if exist "%RESULTS_DIR%" rmdir /s /q "%RESULTS_DIR%"
if exist "%REPORT_DIR%" rmdir /s /q "%REPORT_DIR%"

REM Run pytest with Allure reporting
echo Running tests...
pytest --alluredir=%RESULTS_DIR% Features/

REM Check if tests ran successfully
if %ERRORLEVEL% neq 0 (
    echo Tests failed with error level %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)

REM Generate Allure report
echo Generating Allure report...
allure generate %RESULTS_DIR% --clean -o %REPORT_DIR%

REM Copy history for trend graphs if it exists
if exist "%HISTORY_DIR%" (
    xcopy /Y /E "%HISTORY_DIR%" "%RESULTS_DIR%\history\"
)

REM Open the report in default browser
echo Opening Allure report...
allure open %REPORT_DIR%

exit /b 0
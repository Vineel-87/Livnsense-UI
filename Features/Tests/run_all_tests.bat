@echo off
title LivNSense - Pytest Test Runner

echo ========================================
echo Starting LivNSense Pytest Automation...
echo ========================================

REM Navigate to the project root directory
cd /d C:\Users\User\PycharmProjects\LivnsenseTestingBDD

REM Activate virtual environment
IF EXIST ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
) ELSE (
    echo ERROR: Virtual environment not found!
    pause
    exit /b
)

REM Go to the test folder
cd Features\Tests

REM Run all Python test files using pytest and generate Allure results
echo Running Pytest test scripts...
pytest --alluredir=reports\allure-results

REM Serve the Allure report
IF EXIST "reports\allure-results" (
    echo Launching Allure Report...
    allure serve reports\allure-results
) ELSE (
    echo WARNING: Allure results not found!
)

echo.
echo ========================================
echo Test execution finished.
echo ========================================
pause

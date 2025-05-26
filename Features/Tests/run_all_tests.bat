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

REM Run all test files with names like 1_test_*.py, 2_test_*.py, etc.
echo Running Pytest test scripts on all numbered test files...
pytest --alluredir=reports\allure-results --clean-alluredir

REM Generate Allure Report
IF EXIST "reports\allure-results" (
    echo Generating Allure Report...
    ..\..\allure-2.17.0\bin\allure generate reports\allure-results -o reports\allure-report --clean

    echo Launching Allure Report in Browser...
    ..\..\allure-2.17.0\bin\allure open reports\allure-report
) ELSE (
    echo WARNING: Allure results not found!
)

echo.
echo ========================================
echo Test execution finished.
echo ========================================
pause

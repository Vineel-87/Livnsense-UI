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

echo ========================================================
echo Generating Allure Report...

REM Generate the report from the correct path
allure generate reports\allure-results -o reports\allure-report --clean

echo Launching Allure Report in Browser...
allure open reports\allure-report

pause



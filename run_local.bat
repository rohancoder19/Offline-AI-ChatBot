@echo off
echo ===================================================
echo   Starting Offline and Cloud AI Chatbot (Local)
echo ===================================================
echo.
echo Activating virtual environment (nit_gen1)...
call .\nit_gen1\Scripts\activate.bat

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Failed to activate virtual environment.
    echo Please make sure the 'nit_gen1' folder exists.
    goto end
)

echo Starting Streamlit app...
streamlit run app4.py

:end
echo.
echo Press any key to exit...
pause > nul

@echo off
echo ====================================
echo  Adaptive Benefit Questionnaire
echo ====================================
echo.
echo Installing dependencies...
python -m pip install -r requirements.txt
echo.
echo Starting Flask application...
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
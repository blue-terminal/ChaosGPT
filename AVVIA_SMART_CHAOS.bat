@echo off
title SMART CHAOS AGENT v5.3
color 0A
cd /d "%~dp0"

echo ========================================================
echo        AVVIO SMART CHAOS AGENT - CORE v5.3
echo ========================================================
echo Cartella corrente: %CD%
echo Verifica interprete Python...

where python >nul 2>nul
if %errorlevel% neq 0 (
    color 0C
    echo [ERRORE] Python non e stato trovato nel PATH di sistema!
    echo Assicurati di aver installato Python e aggiunto al PATH.
    pause
    exit /b 1
)

echo [OK] Interprete Python rilevato.
echo Avvio in corso di smart_chaos.py...
echo ========================================================

python smart_chaos.py

if %errorlevel% neq 0 (
    color 0C
    echo.
    echo [ERRORE] Il programma e terminato con codice di errore %errorlevel%.
)

echo.
echo Premi un tasto per chiudere questa finestra...
pause >nul

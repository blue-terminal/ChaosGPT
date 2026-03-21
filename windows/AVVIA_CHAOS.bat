@echo off
title ChaosGPT Runner
color 0a
echo --- AVVIO CHAOS GPT WINDOWS ---
echo Installazione requisiti...
pip install requests pyautogui pillow duckduckgo-search
cls
echo Esecuzione ChaosGPT...
python chaos_win.py
pause

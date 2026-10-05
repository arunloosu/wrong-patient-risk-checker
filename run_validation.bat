@echo off
python src\evaluate.py
python -m unittest discover -s tests -v
pause

@echo off
cd gui_assets
python -m venv PySilon
pip install pillow
python builder.py %*
cd ..
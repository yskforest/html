python -m venv venv_for_exe
venv_for_exe\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pyinstaller $Args[0] --onefile --clean
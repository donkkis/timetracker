dist/tt: tt.py
	rm -rf dist build
	pyinstaller --onefile tt.py
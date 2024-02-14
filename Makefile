dist/tt: tt.py services.py commands.py
	rm -rf dist build
	pyinstaller --onefile tt.py
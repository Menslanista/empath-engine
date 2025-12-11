.PHONY: init install clean

init: install
	@echo "Emotion inference service initialized"

install:
	pip install -r requirements.txt

clean:
	rm -rf venv/
	pip uninstall -r requirements.txt -y 2>/dev/null || true
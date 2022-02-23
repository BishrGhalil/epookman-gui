all: install

install:
	pip install -r requirements.txt
	python setup.py install_exec install --optimize=1 --record=install_log.log

uninstall:
	rm -rf ~/.local/bin/epookman-gui

run:
	python3 epookman-gui.py

clean:
	find epookman_gui -depth -name __pycache__ -type d -exec rm -r -- {} \;
	find -depth -name "*.log" -type f -exec rm -rf -- {} \;
	find -depth -name "*.pyc" -type f -exec rm -rf -- {} \;
	rm -rf dist build epookman_gui.egg-info

.PHONE: clean run

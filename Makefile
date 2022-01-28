all: install

install:
	python setup.py install_exec install --optimize=1 --record=install_log.log

uninstall:
	rm -rf /usr/bin/epookman

run:
	python3 epookman.py

clean:
	find epookman -depth -name __pycache__ -type d -exec rm -r -- {} \;
	find -depth -name "*.log" -type f -exec rm -rf -- {} \;
	rm -rf dist build epookman.egg-info

.PHONE: clean run

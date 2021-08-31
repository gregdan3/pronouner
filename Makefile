.PHONY: init run

init:
	pdm install
run:
	pdm run ./pronouner.py

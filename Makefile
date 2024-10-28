all: run

run:
	python3 launch.py

cont:
	rm -f frontier.shelve
	python3 launch.py

clean_all:
	rm -f frontier.shelve
	rm -f frontier_shelve.json
	rm -f ./data/*.json
	find . -type d -name "__pycache__" -exec rm -rf {} +
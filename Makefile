all: run

run:
	python3 launch.py

clean:
	rm -f frontier.shelve
	rm -f ./data/*.json
	find . -type d -name "__pycache__" -exec rm -rf {} +
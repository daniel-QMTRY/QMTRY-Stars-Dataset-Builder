.PHONY: setup build app clean

setup:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

build:
	python scripts/build_stars_dataset.py --start 2024-01-01 --end 2024-12-31

app:
	streamlit run streamlit/app.py

clean:
	rm -rf output_demo/*.csv evidence/*.json

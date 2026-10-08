# Dark-Web Threat Taxonomy

This synthetic Python project classifies threat reports and assigns a transparent review priority. The priority score supports queue ordering; it is not a probability, legal finding, identity claim, or guilt judgment.

## Run the example

```bash
cd dark-web-threat-taxonomy
PYTHONPATH=src python src/main.py
```

The example uses a synthetic service-log summary. It produces a score, review band, and component rationale.

## Run tests

```bash
cd dark-web-threat-taxonomy
python -m unittest discover -s tests
```

The project uses only the Python standard library.

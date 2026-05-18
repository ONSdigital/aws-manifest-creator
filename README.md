# AWS Manifest Creator

Scans a folder or file in S3 and generates a 'folder.mani' JSON manifest describing the dataset, including file metadata (MD5 checksum, size, path) and dataset provenance.

## Setup
Requires Python 3.x and [Poetry](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

## Running Tests
```bash
poetry run pytest -v
```

## Usage
```bash
poetry run python manifest_creator.py \
  --path ./my-dataset \
  --sourceName ons_tdz \
  --description "My dataset description" \
  --version 1 \
  --dataset my_dataset \
  --sensitivity low
```


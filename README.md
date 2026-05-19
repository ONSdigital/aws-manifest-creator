# AWS Manifest Creator

Generates dataset manifest (.mani) JSON files describing S3 objects, including file metadata (MD5 checksum, size, path) and dataset provenance.

## Architecture
All dependencies are injected behind abstract interfaces, keeping the core logic decoupled from AWS, GCP, or any specific storage or config system.

Object Created event
        │
        ▼
  lambda_handler
        │
        ├── ManifestConfigProvider       → resolves dataset metadata
        ├── DataSourceInterface          → lists files and checksums
        ├── generate_manifest()          → pure function, no I/O
        ├── ManifestDestinationInterface → decides where .mani goes
        └── ManifestPublisherInterface   → writes the manifest

# Setup
Requires Python 3.x and [Poetry](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

# Running Tests

Unit tests only (no AWS required)
```bash
poetry run pytest -v
```

# Local Usage (on-premise/filesystem)
```bash
poetry run python manifest_creator.py \
  --path ./my-dataset \
  --sourceName ons_tdz \
  --description "My dataset description" \
  --version 1 \
  --dataset my_dataset \
  --sensitivity low
```

# Adding a New Provider
Each interface lives in its own module. To add a new implementation:

1. Subclass the relevant ABC (DataSourceProvider, ManifestPublisher, etc.)
2. Implement the single abstract method
3. Inject it into lambda_handler via its parameter
4. Write a unit test — no infrastructure required

See interfaces/manifest_publishers_interface.py for a minimal example (InMemoryManifestPublisher).
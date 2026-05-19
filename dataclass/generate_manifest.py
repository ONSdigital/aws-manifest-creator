import datetime

from dataclasses import dataclass
from src.models import ManifestConfig, DataSourceFile


SCHEMA_VERSION = 2


@dataclass
class ManifestFileEntry:
    name: str
    relative_path: str
    md5sum: str
    size_bytes: int

    def to_json_style_dict(self) -> dict:
        """
        Preserves the camelCase JSON shape downstream consumers expect
        """
        return {
            "name": self.name,
            "relativePath": self.relative_path,
            "md5sum": self.md5sum,
            "sizeBytes": self.size_bytes,
        }


@dataclass
class ManifestData:
    schema_version: int
    source_name: str
    description: str
    manifest_created: str
    dataset: str
    version: int
    sensitivity: str
    iteration_l1: str
    iteration_l2: str
    iteration_l3: str
    iteration_l4: str
    full_size_megabytes: str
    files: list[ManifestFileEntry]

    def to_json_style_dict(self) -> dict:
        """
        Preserves the camelCase JSON shape downstream consumers expect
        """
        return {
            "schemaVersion": self.schema_version,
            "source_name": self.source_name,
            "description": self.description,
            "manifest_created": self.manifest_created,
            "dataset": self.dataset,
            "version": self.version,
            "sensitivity": self.sensitivity,
            "iteration_l1": self.iteration_l1,
            "iteration_l2": self.iteration_l2,
            "iteration_l3": self.iteration_l3,
            "iteration_l4": self.iteration_l4,
            "fullSizeMegabytes": self.full_size_megabytes,
            "files": [file.to_json_style_dict() for file in self.files],
        }


def generate_manifest(config: ManifestConfig, files: list[DataSourceFile]) -> ManifestData:
    """
    Generates a manifest dict from a config and a list of DataSourceFiles.
    Pure function — no I/O. Source and destination are handled by providers.

    Output shape:
    {
        "schemaVersion": 2,
        "sourceName": "...",
        "description": "...",
        "manifestCreated": "2024-01-01T00:00:00+00:00",
        "dataset": "...",
        "version": 1,
        "sensitivity": "low|medium|high",
        "iterationL1": "",
        "iterationL2": "",
        "iterationL3": "",
        "iterationL4": "",
        "fullSizeMegabytes": "0.000005",  # formatted string, 6dp
        "files": [
            {
                "name": "...",
                "relativePath": "...",
                "md5sum": "...",
                "sizeBytes": 123
            }
        ]
    }
    """
    total_bytes = sum(f.size_bytes for f in files)
    full_size_mb = "{0:.6f}".format(total_bytes / 1_000_000)

    return ManifestData(
        schema_version = SCHEMA_VERSION,
        source_name = config.source_name,
        description = config.description,
        manifest_created = _isotime(),
        dataset = config.dataset,
        version = int(config.version),
        sensitivity = config.sensitivity.lower(),
        iteration_l1 = config.iteration_l1 or "",
        iteration_l2 = config.iteration_l2 or "",
        iteration_l3 = config.iteration_l3 or "",
        iteration_l4 = config.iteration_l4 or "",
        full_size_megabytes = full_size_mb,
        files = [
            ManifestFileEntry(
                name=file.name,
                relative_path=file.relative_path,
                md5sum=file.md5,
                size_bytes=int(file.size_bytes),
            )
            for file in files
        ]
    )


def _isotime() -> str:
    now = datetime.datetime.now()
    if now.utcoffset() is None:
        return now.isoformat() + "+00:00"
    return now.isoformat()



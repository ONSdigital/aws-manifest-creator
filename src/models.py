from dataclasses import dataclass

@dataclass
class DataSourceFile:
    """
    Represents a file from any source, in a source-agnostic manner.
    Populated by a DataSourceProvider implementation.
    """
    name: str
    relative_path: str
    size_bytes: int
    md5: str


@dataclass
class ManifestConfig:
    """
    All metadata required to generate a manifest.
    Populated by a ManifestConfig provider implementation
    """
    path: str
    source_name: str
    description: str
    version: int
    dataset: str
    sensitivity: str
    iteration_l1: str = ""
    iteration_l2: str = ""
    iteration_l3: str = ""
    iteration_l4: str = ""
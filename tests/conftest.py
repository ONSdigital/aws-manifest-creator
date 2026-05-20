import pytest

from src.models import ManifestMetadata


@pytest.fixture
def valid_config(tmp_path) -> ManifestMetadata:
    """
    A valid Metadata dataclass object pointing at a real temp directory.
    Override individual fields in tests to exercise specific behaviours.
    """
    return ManifestMetadata(
        path=str(tmp_path),
        source_name="onz_tdz",
        description="Test dataset",
        version=1,
        dataset="valid_dataset",
        sensitivity="low",
        iteration_l1="",
        iteration_l2="",
        iteration_l3="",
        iteration_l4="",
    )

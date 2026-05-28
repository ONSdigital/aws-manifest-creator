import pytest

from interfaces.data_source_interface import DataSourceInterface
from interfaces.metadata_fetcher_interface import MetadataFetcherInterface
from lambda_handler import lambda_handler
from services.manifest_uploader_service import InMemoryManifestUploaderService
from src.models import ManifestMetadata, DataSourceFile


class StubMetadataFetcherInterface(MetadataFetcherInterface):
    def __init__(self, metadata: ManifestMetadata):
        self._metadata = metadata

    def get_metadata(self, bucket: str, key: str) -> ManifestMetadata:
        return self._metadata


class StubDataSourceInterface(DataSourceInterface):
    def __init__(self, files: list[DataSourceFile]):
        self._files = files

    def list_files(self, location: str) -> list[DataSourceFile]:
        return self._files


@pytest.fixture
def s3_event():
    return {
        "Records": [{
            "s3": {
                "bucket": {"name": "my-bucket"},
                "object": {"key": "datasets/mydata/file.csv"}
            }
        }]
    }


@pytest.fixture
def stub_config(tmp_path) -> ManifestMetadata:
    return ManifestMetadata(
        path=str(tmp_path),
        source_name='ons_tdz',
        description='Test dataset',
        version=1,
        dataset='valid_dataset',
        sensitivity='low',
    )


@pytest.fixture
def stub_files() -> list[DataSourceFile]:
    return [
        DataSourceFile(
            name='file.csv',
            relative_path='datasets/mydata',
            size_bytes=5,
            md5='abc123'
        )
    ]



# def test_lambda_handler_returns_success_on_valid_event(s3_event, stub_config, stub_files):
#     # arrange
#     publisher = InMemoryManifestUploaderService()
#
#     # act
#     result = lambda_handler(
#         event=s3_event,
#         context=None,
#         config_provider=StubMetadataFetcherInterface(stub_config),
#         data_source=StubDataSourceInterface(stub_files),
#         resolver=SamePrefixResolver(),
#         publisher=publisher
#     )
#
#     # assert
#     assert result["status"] == "success"
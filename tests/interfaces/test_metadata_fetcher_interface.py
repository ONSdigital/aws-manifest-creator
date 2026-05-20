import boto3
import pytest

from moto import mock_aws

from interfaces.metadata_fetcher_interface import EnvironmentMetadataFetcherInterface, S3MetadataFetcherInterface


class TestEnvironmentMetadataFetcherInterface:
    @pytest.fixture
    def environment_metadata_env_vars(self, monkeypatch):
        monkeypatch.setenv('SOURCE_NAME', 'ons_tdz')
        monkeypatch.setenv('DESCRIPTION', 'Test dataset')
        monkeypatch.setenv('VERSION', '1')
        monkeypatch.setenv('DATASET', 'my_dataset')
        monkeypatch.setenv('SENSITIVITY', 'low')

    @pytest.fixture
    def fetcher(self):
        return EnvironmentMetadataFetcherInterface()

    def test_environment_metadata_fetcher_interface_returns_manifest_metadata(self, environment_metadata_env_vars, fetcher):
        # act
        result = fetcher.get_metadata('my-bucket', 'datasets/file.csv')

        # assert
        assert result.source_name == 'ons_tdz'
        assert result.description == 'Test dataset'
        assert result.version == 1
        assert result.dataset == 'my_dataset'
        assert result.sensitivity == 'low'

    def test_environment_metadata_fetcher_interface_sets_path_from_bucket_and_key(self, environment_metadata_env_vars, fetcher):
        # act
        result = fetcher.get_metadata('my-bucket', 'datasets/file.csv')

        # assert
        assert result.path == 'my-bucket/datasets/file.csv'

    def test_environment_metadata_fetcher_interface_casts_version_to_integer(self, environment_metadata_env_vars, fetcher):
        # act
        result = fetcher.get_metadata('my-bucket', 'datasets/file.csv')

        # assert
        assert isinstance(result.version, int)
        assert result.version == 1

    def test_environment_metadata_fetcher_interface_defaults_optional_iterations_to_empty_string(self, environment_metadata_env_vars, fetcher):
        # act
        result = fetcher.get_metadata('my-bucket', 'datasets/file.csv')

        # assert
        assert result.iteration_l1 == ''
        assert result.iteration_l2 == ''
        assert result.iteration_l3 == ''
        assert result.iteration_l4 == ''

    def test_environment_metadata_fetcher_interface_reads_optional_iterations_when_present(self, environment_metadata_env_vars, monkeypatch, fetcher):
        # arrange
        monkeypatch.setenv('ITERATION_L1', 'benedict_cumberbatch')

        # act
        result = fetcher.get_metadata('my-bucket', 'datasets/file.csv')

        # assert
        assert result.iteration_l1 == 'benedict_cumberbatch'
        assert result.iteration_l2 == ''
        assert result.iteration_l3 == ''
        assert result.iteration_l4 == ''

    def test_environment_metadata_fetcher_interface_raises_when_required_env_var_missing(self, environment_metadata_env_vars, monkeypatch, fetcher):
        # arrange
        monkeypatch.delenv("SOURCE_NAME", raising=False)

        # act & assert
        with pytest.raises(KeyError):
            fetcher.get_metadata('my-bucket', 'datasets/file.csv')


@mock_aws
class TestS3MetadataFetcherInterface:
    @pytest.fixture
    def s3_bucket(self):
        """
        Spins up a fake S3 bucket via moto - no real AWS calls made :raised_hands:
        """
        with mock_aws():
            s3 = boto3.client("s3", region_name="eu-west-2")
            s3.create_bucket(
                Bucket="test-bucket",
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
            )
            yield s3

    @pytest.fixture
    def fetcher(self):
        return S3MetadataFetcherInterface()


    @pytest.fixture
    def upload_data(self, s3_bucket):
        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/file.csv",
            Body=b'a,b,c',
            Metadata={
                'SOURCE_NAME': 'ons_tdz',
                'DESCRIPTION': 'Test dataset',
                'VERSION': '1',
                'DATASET': 'my_dataset',
                'SENSITIVITY': 'low'
            }
        )

    def test_s3_metadata_fetcher_interface_returns_manifest_metadata(self, s3_bucket, upload_data, fetcher):
        # act
        result = fetcher.get_metadata("test-bucket", "datasets/file.csv")

        # assert
        assert result.path == "test-bucket/datasets/file.csv"

    def test_s3_metadata_fetcher_interface_defaults_optional_iterations_to_empty_string(self, s3_bucket, upload_data, fetcher):
        # act
        result = fetcher.get_metadata("test-bucket", "datasets/file.csv")

        # assert
        assert result.iteration_l1 == ''
        assert result.iteration_l2 == ''
        assert result.iteration_l3 == ''
        assert result.iteration_l4 == ''

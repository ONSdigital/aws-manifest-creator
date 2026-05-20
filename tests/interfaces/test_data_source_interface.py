import boto3
import hashlib
import pytest

from moto import mock_aws

from interfaces.data_source_interface import LocalDataSourceInterface, S3DataSourceInterface


@mock_aws
class TestS3DataSourceInterface:
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

    def test_s3_data_source_interface_lists_files_in_prefix(self, s3_bucket):
        # arrange
        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/mydata/file.csv",
            Body=b'a,b,c'
        )

        # act
        files = S3DataSourceInterface().list_files("test-bucket/datasets/mydata")

        # assert
        assert len(files) == 1
        assert files[0].name == "file.csv"

    def test_s3_data_source_interface_skips_mani_files(self, s3_bucket):
        # arrange
        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/mydata/file.csv",
            Body=b'a,b,c'
        )

        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/mydata/folder.mani",
            Body=b'{}'
        )

        # act
        files = S3DataSourceInterface().list_files("test-bucket/datasets/mydata")

        # assert
        assert len(files) == 1
        assert files[0].name == "file.csv"

    def test_s3_data_source_interface_returns_correct_file_size(self, s3_bucket):
        # arrange
        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/mydata/file.csv",
            Body=b'this is 16 bytes'
        )

        # act
        files = S3DataSourceInterface().list_files("test-bucket/datasets/mydata")

        # assert
        assert files[0].size_bytes == 16

    def test_s3_data_source_interface_returns_correct_md5_for_single_part_upload(self, s3_bucket):
        # arrange
        content = b'Meats and cheeses always pleases'
        s3_bucket.put_object(
            Bucket="test-bucket",
            Key="datasets/mydata/file.csv",
            Body=content
        )
        expected_md5 = hashlib.md5(content).hexdigest()

        # act
        files = S3DataSourceInterface().list_files("test-bucket/datasets/mydata")

        # assert
        assert files[0].md5 == expected_md5

    def test_s3_data_source_interface_returns_empty_for_empty_prefix(self, s3_bucket):
        # act
        files = S3DataSourceInterface().list_files("test-bucket/datasets/mydata")

        # assert
        assert files == []


class TestLocalDataSourceInterface:
    def test_local_datasource_interface_lists_files_in_directory(self, tmp_path):
        # arrange
        (tmp_path / "benedict.csv").write_bytes(b"a,b,c")

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert len(files) == 1
        assert files[0].name == "benedict.csv"

    def test_local_datasource_interface_skips_mani_files(self, tmp_path):
        # arrange
        (tmp_path / "folder.mani").write_bytes(b"a,b,c")

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert len(files) == 0

    def test_local_datasource_interface_returns_correct_file_size(self, tmp_path):
        # arrange
        (tmp_path / "benedict.csv").write_bytes(b"a,b,c")

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert files[0].size_bytes == 5

    def test_local_datasource_interface_returns_correct_md5(self, tmp_path):
        # arrange
        content = b"hello world"
        (tmp_path / "benedict.csv").write_bytes(content)
        expected_md5 = hashlib.md5(content).hexdigest()

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert files[0].md5 == expected_md5

    def test_local_datasource_interface_walks_subdirectories(self, tmp_path):
        # arrange
        (tmp_path / "sub").mkdir()
        (tmp_path / "sub" / "deep.csv").write_bytes(b"x")

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert any(file.name == "deep.csv" for file in files)

    def test_local_datasource_interface_returns_empty_for_empty_directory(self, tmp_path):
        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert files == []

    def test_local_datasource_interface_lists_multiple_files(self, tmp_path):
        # arrange
        (tmp_path / "a.csv").write_bytes(b"x")
        (tmp_path / "b.csv").write_bytes(b"y")
        (tmp_path / "c.csv").write_bytes(b"z")

        # act
        files = LocalDataSourceInterface().list_files(str(tmp_path))

        # assert
        assert len(files) == 3

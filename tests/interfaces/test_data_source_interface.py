import hashlib

from interfaces.data_source_interface import LocalDataSourceInterface


class TestS3DataSourceInterface:
    # TODO!
    pass


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

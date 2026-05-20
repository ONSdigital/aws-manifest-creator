import json

import pytest

from services.manifest_uploader_service import InMemoryManifestUploaderService, LocalManifestUploaderService


class TestInMemoryManifestUploader:
    @pytest.fixture
    def publisher(self):
        return InMemoryManifestUploaderService()

    def test_in_memory_manifest_publisher_interface_publishes_manifest_to_destination(self, publisher):
        # arrange
        manifest = {"schemaVerion": 2, "dataset": "my_dataset"}

        # act
        publisher.save(manifest, "test/folder.mani")

        # assert
        assert publisher.published["test/folder.mani"] == manifest

    def test_in_memory_manifest_publisher_interface_returns_destination_as_location(self, publisher):
        # act
        location = publisher.save({}, "test/folder.mani")

        # assert
        assert location == "test/folder.mani"

    def test_in_memory_manifest_publisher_interface_stores_multiple_manifests(self, publisher):
        # act
        publisher.save({"dataset": "a"}, "dest/a.mani")
        publisher.save({"dataset": "b"}, "dest/b.mani")

        # assert
        assert len(publisher.published) == 2


class TestLocalManifestUploader:
    @pytest.fixture
    def uploader(self):
        return LocalManifestUploaderService()

    def test_local_manifest_uploader_interface_writes_manifest_to_disk(self, uploader, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")
        manifest = {"schemaVerion": 2, "dataset": "my_dataset"}

        # act
        uploader.save(manifest, destination)

        # assert
        with open(destination) as f:
            written = json.load(f)
        assert written == manifest

    def test_local_manifest_uploader_interface_returns_destination_path(self, uploader, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")

        # act
        location = uploader.save({}, destination)

        # assert
        assert location == destination

    def test_local_manifest_uploader_interface_overwrites_existing_file(self, uploader, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")

        # act
        uploader.save({"dataset": "first"}, destination)
        uploader.save({"dataset": "second"}, destination)

        # assert
        # TODO: Assert the negative
        with open(destination) as f:
            written = json.load(f)
        assert written["dataset"] == "second"
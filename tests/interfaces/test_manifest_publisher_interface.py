import json

import pytest

from interfaces.manifest_publisher_interface import InMemoryManifestPublisherInterface, LocalManifestPublisherInterface


class TestInMemoryManifestPublisher:
    @pytest.fixture
    def publisher(self):
        return InMemoryManifestPublisherInterface()

    def test_in_memory_manifest_publisher_interface_publishes_manifest_to_destination(self, publisher):
        # arrange
        manifest = {"schemaVerion": 2, "dataset": "my_dataset"}

        # act
        publisher.publish(manifest, "test/folder.mani")

        # assert
        assert publisher.published["test/folder.mani"] == manifest

    def test_in_memory_manifest_publisher_interface_returns_destination_as_location(self, publisher):
        # act
        location = publisher.publish({}, "test/folder.mani")

        # assert
        assert location == "test/folder.mani"

    def test_in_memory_manifest_publisher_interface_stores_multiple_manifests(self, publisher):
        # act
        publisher.publish({"dataset": "a"}, "dest/a.mani")
        publisher.publish({"dataset": "b"}, "dest/b.mani")

        # assert
        assert len(publisher.published) == 2


class TestLocalManifestPublisher:
    @pytest.fixture
    def publisher(self):
        return LocalManifestPublisherInterface()

    def test_local_manifest_publisher_interface_writes_manifest_to_disk(self, publisher, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")
        manifest = {"schemaVerion": 2, "dataset": "my_dataset"}

        # act
        publisher.publish(manifest, destination)

        # assert
        with open(destination) as f:
            written = json.load(f)
        assert written == manifest

    def test_local_manifest_publisher_interface_returns_destination_path(self, publisher, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")

        # act
        location = publisher.publish({}, destination)

        # assert
        assert location == destination

    def test_local_manifest_publisher_interface_overwrites_existing_file(self, publisher, tmp_path):
        # arrange
        destination = str(tmp_path / "folder.mani")

        # act
        publisher.publish({"dataset": "first"}, destination)
        publisher.publish({"dataset": "second"}, destination)

        # assert
        # TODO: Assert the negative
        with open(destination) as f:
            written = json.load(f)
        assert written["dataset"] == "second"
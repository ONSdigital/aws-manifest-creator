import json

import boto3

from abc import abstractmethod, ABC


class ManifestPublisherInterface(ABC):
    @abstractmethod
    def publish(self, manifest: dict, destination: str):
        """
        Publish the manifest dict to the given destination.
        Destination is intentionally a plain string — each implementation
        interprets it however makes sense for that target.
        Returns the final location of the published manifest.
        """
        pass

class S3ManifestPublisherInterface(ManifestPublisherInterface):
    """
    Publishes the manifest JSON to an S3 object.
    destination format: "bucket-name/path/to/folder.mani"
    """
    def __init__(self):
        self.s3 = boto3.client('s3')

    def publish(self, manifest: dict, destination: str) -> str:
        bucket, key = destination.split('/', 1)
        self.s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(manifest),
            ContentType='application/json'
        )
        return f"s3://{bucket}/{key}"


class LocalManifestPublisherInterface(ManifestPublisherInterface):
    """
    Writes the manifest JSON to the local filesystem.
    Preserves backwards compatibility with the original on-premise script.
    destination: a local file path, e.g. "/tmp/folder.mani"
    """
    def publish(self, manifest: dict, destination: str) -> str:
        with open(destination, 'w') as file:
            json.dump(manifest, file)
        return destination


class InMemoryManifestPublisherInterface(ManifestPublisherInterface):
    """
    Captures published manifests in memory.
    No I/O — intended for use in unit tests only.

    Usage:
        publisher = InMemoryManifestPublisher()
        publisher.publish(manifest, "test/folder.mani")
        assert publisher.published["test/folder.mani"]["schemaVersion"] == 2
    """

    def __init__(self):
        self.published: dict[str, dict] = {}

    def publish(self, manifest: dict, destination: str) -> str:
        self.published[destination] = manifest
        return destination


class GCSManifestPublisherInterface(ManifestPublisherInterface):
    """
    Example interface: Publishes the manifest JSON to a GCP Cloud Storage object.
    destination format: "bucket-name/path/to/folder.mani"
    Requires: google-cloud-storage
    """
    def publish(self, manifest: dict, destination: str) -> str:
        raise NotImplementedError("GCSManifestPublisher is not yet implemented")

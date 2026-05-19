import hashlib
import os

import boto3

from abc import ABC, abstractmethod

from interfaces.checksum_interface import ChecksumInterface, ETagChecksumInterface
from src.models import DataSourceFile


class DataSourceInterface(ABC):
    @abstractmethod
    def list_files(self, location: str) -> list[DataSourceFile]:
        """
        Given a location string, return a list of DataSourceFile objects.
        Location is intentionally a plain string — each implementation interprets it however makes sense for that source
        i.e., on-prem server, AWS S3 object or Google Cloud Storage object.
        """
        pass


class S3DataSourceInterface(DataSourceInterface):
    """
    Lists files from an S3 bucket/prefix.
    location format: "bucket-name/prefix/path"
    """
    def __init__(self, checksum_interface: ChecksumInterface = None):
        self.s3 = boto3.client("s3")
        self.checksum_interface = checksum_interface or ETagChecksumInterface()

    def list_files(self, location: str) -> list[DataSourceFile]:
        bucket, prefix = location.rsplit("/", 1)
        response = self.s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

        return [
            DataSourceFile(
                name=obj["Key"].split("/")[-1],
                relative_path="/".join(obj["Key"].split("/")[:-1]),
                size_bytes=obj["Size"],
                md5=self.checksum_interface.get_md5(bucket, obj["Key"]),
            )
            for obj in response.get("Contents", [])
            if not obj["Key"].endswith(".mani")
        ]


class LocalDataSourceInterface(DataSourceInterface):
    """
    Lists files from the local filesystem.
    Preserves backwards compatibility with the original on-premise script.
    location: a local directory or file path.
    """
    def list_files(self, location: str) -> list[DataSourceFile]:
        files = []
        for root, _, filenames in os.walk(location):
            for filename in filenames:
                if filename.endswith(".mani"):
                    continue
                filepath = os.path.join(root, filename)
                files.append(DataSourceFile(
                    name=filename,
                    relative_path=os.path.relpath(root, location),
                    size_bytes=os.path.getsize(filepath),
                    md5=hashlib.md5(open(filepath, "rb").read()).hexdigest(),
                ))
        return files

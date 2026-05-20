import boto3
import os

from abc import abstractmethod, ABC

from src.models import ManifestMetadata


class MetadataFetcherInterface(ABC):
    @abstractmethod
    def get_metadata(self, bucket: str, key: str) -> ManifestMetadata:
        """
        Return a ManifestMetadata object for the given datasource.
        bucket and key are passed to allow context-aware config resolution,
        e.g., reading sidecar files or object metadata
        """


class EnvironmentMetadataFetcherInterface(MetadataFetcherInterface):
    """
    Reads config from Lambda environment variables.
    Suitable for first iteration where all files in the bucket share the same metadata

    Required env vars:
        SOURCE_NAME
        DESCRIPTION
        VERSION
        DATASET
        SENSITIVITY

    Optional env vars:
        ITERATION_L1,
        ITERATION_L2,
        ITERATION_L3,
        ITERATION_L4,
    """
    def get_metadata(self, bucket: str, key: str) -> ManifestMetadata:
        return ManifestMetadata(
            path=f"{bucket}/{key}",
            source_name=os.environ['SOURCE_NAME'],
            description=os.environ['DESCRIPTION'],
            version=int(os.environ['VERSION']),
            dataset=os.environ['DATASET'],
            sensitivity=os.environ['SENSITIVITY'],
            iteration_l1=os.environ.get('ITERATION_L1', ''),
            iteration_l2=os.environ.get('ITERATION_L2', ''),
            iteration_l3=os.environ.get('ITERATION_L3', ''),
            iteration_l4=os.environ.get('ITERATION_L4', ''),
        )


class S3MetadataFetcherInterface(MetadataFetcherInterface):
    """
    Reads metadata from S3 object (x-amz-meta-* headers).
    Set at upload time by the producing system.

    Expected metadata keys:
        source-name, description, version, dataset,
        sensitivity, iteration-l1..l4 (optional)
    """
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_metadata(self, bucket:str, key:str) -> ManifestMetadata:
        head = self.s3.head_object(Bucket=bucket, Key=key)
        meta = head["Metadata"]

        return ManifestMetadata(
            path=f"{bucket}/{key}",
            source_name=meta.get("source_name", ""),
            description=meta.get("description", ""),
            version=int(meta.get("version", "")),
            dataset=meta.get("dataset", ""),
            sensitivity=meta.get("sensitivity", ""),
            iteration_l1=meta.get("iteration_l1", ""),
            iteration_l2=meta.get("iteration_l2", ""),
            iteration_l3=meta.get("iteration_l3", ""),
            iteration_l4=meta.get("iteration_l4", ""),
        )

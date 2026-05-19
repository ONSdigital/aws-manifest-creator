import boto3
import hashlib

from abc import ABC


class ChecksumInterface(ABC):
    """Return the MD5 hex digest for the given S3 object."""
    pass


class ETagChecksumInterface(ChecksumInterface):
    """
    Uses the S3 ETag as the MD5.
    Valid for single-part uploads only.

    TODO: For multipart uploads, ETag is a composite hash and will not
     match a true MD5. Replace with DownloadChecksumProvider or
     MetadataChecksumProvider when multipart support is required.
    """
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_md5(self, bucket: str, key: str) -> str:
        head = self.s3.head_object(Bucket=bucket, Key=key)
        return head["ETag"].strip('"')


class DownloadChecksumInterface(ChecksumInterface):
    """
    Downloads the file from S3 and computes MD5 directly.
    Accurate for both single and multipart uploads.

    NOTE: Incurs download cost and Lambda timeout risk for large files.
    Consider MetadataChecksumProvider for large datasets.
    """
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_md5(self, bucket: str, key: str) -> str:
        obj = self.s3.get_object(Bucket=bucket, Key=key)
        return hashlib.md5(obj["Body"].read()).hexdigest()


class MetadataChecksumInterface(ChecksumInterface):
    """
    Reads MD5 from S3 object metadata (x-amz-meta-md5).
    Most efficient option — requires upload process to set the metadata.
    """
    def __init__(self):
        self.s3 = boto3.client("s3")

    def get_md5(self, bucket: str, key: str) -> str:
        head = self.s3.head_object(Bucket=bucket, Key=key)
        return head["Metadata"]["md5"]
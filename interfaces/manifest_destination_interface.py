from abc import abstractmethod, ABC


class ManifestDestinationInterface(ABC):
    @abstractmethod
    def get(self, source_bucket: str, source_key: str) -> tuple[str, str]:
        """
        Given the source file location, return (destination_bucket, destination_key) for the .mani file
        """


class SamePrefixDestinationInterface(ManifestDestinationInterface):
    """
    Places the .mani file in the same bucket and prefix as the source file.
    e.g. my-bucket/datasets/mydata/file.csv
      -> my-bucket/datasets/mydata/file.csv.mani
    """

    def get(self, source_bucket: str, source_key: str) -> tuple[str, str]:
        return source_bucket, source_key + '.mani'


class CentralDestinationInterface(ManifestDestinationInterface):
    """
    Places all .mani files in a central bucket under a configurable prefix.
    e.g. my-bucket/datasets/mydata/file.csv
      -> manifest-bucket/manifests/file.csv.mani
    """
    def __init__(self, manifest_bucket: str, prefix: str = 'manifests/'):
        self.manifest_bucket = manifest_bucket
        self.prefix = prefix

    def get(self, source_bucket: str, source_key: str) -> tuple[str, str]:
        filename = source_key.split('/')[-1]
        return self.manifest_bucket, f"{self.prefix}{filename}.mani"


class FolderDestinationInterface(ManifestDestinationInterface):
    """
    Places a single folder.mani at the prefix (folder) level
    rather than per-file, matching the original on-premise behaviour.
    e.g. my-bucket/datasets/mydata/file.csv
      -> my-bucket/datasets/mydata/folder.mani
    """
    def get(self, source_bucket: str, source_key: str) -> tuple[str, str]:
        prefix = '/'.join(source_key.split('/')[:-1])
        return source_bucket, f"{prefix}/folder.mani"

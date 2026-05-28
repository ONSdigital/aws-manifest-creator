import json
import logging

from dataclass.generate_manifest import generate_manifest
from interfaces.data_source_interface import DataSourceInterface
from interfaces.manifest_destination_interface import ManifestDestinationInterface
from services.manifest_uploader_service import ManifestUploaderService
from interfaces.metadata_fetcher_interface import MetadataFetcherInterface
from services.validate import validate
from src.models import ManifestMetadata

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(
        event:dict,
        context,
        metadata: MetadataFetcherInterface = None,
        data_source: DataSourceInterface = None,
        destination: ManifestDestinationInterface = None,
        uploader: ManifestUploaderService = None,
) -> dict:
    """
    Lambda entry point. Triggered by S3 ObjectCreated events.

    All dependencies are injected with production defaults,
    making the handler fully testable without mocking globals.

    Args:
        event:           S3 event notification payload
        context:         Lambda context (unused)
        config_provider: Resolves manifest metadata config
        data_source:     Lists files from the source location
        resolver:        Determines where the .mani file is written
        publisher:       Writes the manifest to its destination

    Returns:
        dict with status and manifest_location on success
    """
    # defaults
    metadata = metadata or MetadataFetcherInterface()
    data_source = data_source or DataSourceInterface()
    destination = destination or ManifestDestinationInterface()
    uploader = uploader or ManifestUploaderService()

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    # avoid infinite loop — .mani creation would retrigger this Lambda
    if key.endswith(".mani"):
        logger.info(json.dumps({
            "action": "skipped",
            "reason": "manifest file",
            "key": key,
        }))
        return {"status": "skipped", "reason": "manifest file"}

    logger.info(json.dumps({"action": "processing", "bucket": bucket, "key": key}))

    # resolve config
    manifest_metadata: ManifestMetadata = metadata.get_metadata(bucket, key)

    # validate
    is_valid, errors = validate(manifest_metadata)
    if not is_valid:
        logger.error(json.dumps({
            "action": "validation_failed",
            "errors": errors,
        }))
        raise ValueError(f"Invalid manifest: {errors}")

    # list source files
    files = data_source.list_files(f"{bucket}/{key}")
    if not files:
        logger.warning(json.dumps({
            "action": "no_files_found",
            "location": f"{bucket}/{key}",
        }))
        raise ValueError(f"No files found at {bucket}/{key}")

    # generate manifest
    mani = generate_manifest(manifest_metadata, files)

    # resolve destination and publish
    destination_bucket, destination_key = destination.get(bucket, key)
    location = uploader.save(mani, f"{destination_bucket}/{destination_key}")

    logger.info(json.dumps({
        "action": "manifest_published",
        "manifest_location": location,
        "file_count": len(files)
    }))

    return {
        "status": "success",
        "manifest_location": location,
        "file_count": len(files)
    }


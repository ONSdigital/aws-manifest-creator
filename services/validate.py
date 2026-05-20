import os.path
import re

from src.models import ManifestMetadata


def validate(manifest_metadata: ManifestMetadata) -> tuple[bool, list[str]]:
    """
    Validates the ManifestMetadata before generating the Manifest.
    Returns (is_valid, list_of_errors)
    """

    errors = []
    valid_chars = re.compile("^[a-z0-9_]*$")
    valid_sensitivity = {"low", "medium", "high"}

    if not os.path.exists(manifest_metadata.path):
        errors.append("path does not exist")

    if not valid_chars.match(manifest_metadata.dataset):
        errors.append("dataset can only contain a-z, 0-9 and _")

    for level, value in [
        ('iteration_l1', manifest_metadata.iteration_l1),
        ('iteration_l2', manifest_metadata.iteration_l2),
        ('iteration_l3', manifest_metadata.iteration_l3),
        ('iteration_l4', manifest_metadata.iteration_l4),
    ]:
        if value and not valid_chars.match(value):
            errors.append(f"{level} can only contain a-z, 0-9 and _")

    try:
        version = int(manifest_metadata.version)
        if not (0 < version <= 99):
            errors.append(f"version can only be between 0 and 99")
    except (ValueError, TypeError):
        errors.append("version can only be between 0 and 99")


    if manifest_metadata.sensitivity.lower() not in valid_sensitivity:
        errors.append("sensitivity can only be one of low, medium, high")

    return len(errors) == 0, errors
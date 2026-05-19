import pytest
from dataclass.generate_manifest import generate_manifest, ManifestData

from src.models import DataSourceFile


@pytest.fixture
def sample_files() -> list[DataSourceFile]:
    return [
        DataSourceFile(
            name="benedict.csv",
            relative_path="datasets/mydata",
            size_bytes=5,
            md5="abc123",
        ),
        DataSourceFile(
            name="cumberbatch.csv",
            relative_path="datasets/mydata",
            size_bytes=10,
            md5="def456",
        )
    ]


@pytest.fixture
def manifest(valid_config, sample_files) -> ManifestData:
    return generate_manifest(valid_config, sample_files)


class TestManifestShape:
    def test_generate_manifest_contains_schema_version(self, manifest):
        assert manifest.schema_version == 2

    def test_generate_manifest_contains_source_name(self, manifest):
        assert manifest.source_name == 'onz_tdz'

    def test_generate_manifest_contains_description(self, manifest):
        assert manifest.description == 'Test dataset'

    def test_generate_manifest_contains_manifest_created_timestamp(self, manifest):
        assert manifest.manifest_created is not None
        assert '+00:00' in manifest.manifest_created

    def test_generate_manifest_contains_dataset(self, manifest):
        assert manifest.dataset == 'valid_dataset'

    def test_generate_manifest_contains_version(self, manifest):
        assert manifest.version == 1

    def test_generate_manifest_stores_version_as_an_integer(self, valid_config, sample_files):
        # arrange
        valid_config.version = "2"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert isinstance(manifest.version, int)

    # TODO: Explicitly handle value errors
    @pytest.mark.xfail()
    def test_generate_manifest_raises_value_error_when_version_is_invalid(self, valid_config, sample_files):
        # arrange
        valid_config.version = "Blubberwhale Capncrunch"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert isinstance(manifest.version, int)

    def test_generate_manifest_contains_sensitivity(self, manifest):
        assert manifest.sensitivity == "low"

    def test_generate_manifest_stores_sensitivity_as_lowercase(self, valid_config, sample_files):
        # arrange
        valid_config.sensitivity = "HIGH"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.sensitivity == "high"

    # TODO: Explicitly handle value errors
    @pytest.mark.xfail()
    def test_generate_manifest_handles_error_when_sensitivity_is_invalid(self, valid_config, sample_files):
        # arrange
        valid_config.sensitivity = "Bendersnap Crumplehorn"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.sensitivity in ["low", "medium", "high"]

    def test_generate_manifest_contains_iteration_l1(self, valid_config, sample_files):
        # arrange
        valid_config.iteration_l1 = "Benedict"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.iteration_l1 == "Benedict"

    def test_generate_manifest_contains_iteration_l2(self, valid_config, sample_files):
        # arrange
        valid_config.iteration_l2 = "Cumberbatch"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.iteration_l2 == "Cumberbatch"

    def test_generate_manifest_contains_iteration_l3(self, valid_config, sample_files):
        # arrange
        valid_config.iteration_l3 = "foo"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.iteration_l3 == "foo"

    def test_generate_manifest_contains_iteration_l4(self, valid_config, sample_files):
        # arrange
        valid_config.iteration_l4 = "bar"

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.iteration_l4 == "bar"

    def test_generate_manifest_stores_none_iterations_as_empty_string(self, valid_config, sample_files):
        # arrange
        valid_config.iteration_l1 = None

        # act
        manifest = generate_manifest(valid_config, sample_files)

        # assert
        assert manifest.iteration_l1 == ''

    def test_generate_manifest_stores_empty_iteration_l1_as_empty_string(self, manifest):
        assert manifest.iteration_l1 == ""

    def test_generate_manifest_stores_empty_iteration_l2_as_empty_string(self, manifest):
        assert manifest.iteration_l2 == ""

    def test_generate_manifest_stores_empty_iteration_l3_as_empty_string(self, manifest):
        assert manifest.iteration_l3 == ""

    def test_generate_manifest_stores_empty_iteration_l4_as_empty_string(self, manifest):
        assert manifest.iteration_l4 == ""

    def test_generate_manifest_contains_full_size_megabytes(self, manifest):
        assert manifest.full_size_megabytes == "0.000015"


class TestManifestFiles:
    def test_generate_manifest_contains_list_of_files(self, manifest):
        assert isinstance(manifest.files, list)

    def test_generate_manifest_contains_correct_number_of_files(self, manifest):
        assert len(manifest.files) == 2

    def test_generate_manifest_contains_correct_keys_for_files(self, manifest):
        assert manifest.files[0].name is not None
        assert manifest.files[0].relative_path is not None
        assert manifest.files[0].md5sum is not None
        assert manifest.files[0].size_bytes is not None

        assert manifest.files[1].name is not None
        assert manifest.files[1].relative_path is not None
        assert manifest.files[1].md5sum is not None
        assert manifest.files[1].size_bytes is not None

    def test_generate_manifest_contains_correct_name_of_files(self, manifest):
        assert manifest.files[0].name == "benedict.csv"
        assert manifest.files[1].name == "cumberbatch.csv"

    def test_generate_manifest_contains_correct_md5_of_files(self, manifest):
        assert manifest.files[0].md5sum == "abc123"
        assert manifest.files[1].md5sum == "def456"

    def test_generate_manifest_contains_file_entry_size_as_integer(self, manifest):
        assert isinstance(manifest.files[0].size_bytes, int)
        assert isinstance(manifest.files[1].size_bytes, int)


class TestManifestSize:
    def test_generate_manifest_contains_full_size_megabytes_as_string(self, manifest):
        assert isinstance(manifest.full_size_megabytes, str)

    def test_generate_manifest_contains_full_size_megabytes_in_six_decimal_places(self, manifest):
        # arrange
        decimal_part = manifest.full_size_megabytes.split(".")[1]

        # assert
        assert len(decimal_part) == 6

    def test_generate_manifest_totals_full_size_megabytes(self, manifest):
        assert manifest.full_size_megabytes == "0.000015"   # 5 bytes + 10 bytes = 0.000015 MB







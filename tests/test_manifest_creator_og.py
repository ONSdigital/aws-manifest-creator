import json
import os
import pytest

from argparse import Namespace
from manifest_creator_og import validate, GenerateManifest


class TestValidate:
    @pytest.fixture
    def allargs(self):
        return Namespace(
            path=os.getcwd(),
            sourceName="ons_tdz",
            description="Test dataset for validation",
            version="1",
            dataset="valid_dataset",
            sensitivity="low",
            iterationl1=None,
            iterationl2=None,
            iterationl3=None,
            iterationl4=None
        )

    def test_validate_returns_true(self, allargs):
        # act
        result = validate(allargs)

        # assert
        assert result == True

    def test_validate_rejects_invalid_path(self, allargs):
        # arrange
        allargs.path = "None"   # invalid path

        # act
        result = validate(allargs)

        # assert
        assert result == False

    def test_validate_rejects_invalid_characters(self, allargs):
        # arrange
        allargs.dataset = "INVALID dataset name"

        # act
        result = validate(allargs)

        # assert
        assert result == False

    @pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
    def test_validate_rejects_invalid_characters_in_iteration1(self, allargs):
        # arrange
        allargs.iterationl1 = "INVALID iteration!!!"

        # act
        result = validate(allargs)

        # assert
        assert result == False

    @pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
    def test_validate_rejects_invalid_characters_in_iteration2(self, allargs):
        # arrange
        allargs.iterationl2 = "INVALID iteration!!!"

        # act
        result = validate(allargs)

        # assert
        assert result == False

    @pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
    def test_validate_rejects_invalid_characters_in_iteration3(self, allargs):
        # arrange
        allargs.iterationl3 = "INVALID iteration!!!"

        # act
        result = validate(allargs)

        # assert
        assert result == False

    @pytest.mark.xfail(reason="hasattr() always returns True, short-circuiting the or — see validate()")
    def test_validate_rejects_invalid_characters_in_iteration4(self, allargs):
        # arrange
        allargs.iterationl4 = "INVALID iteration!!!"

        # act
        result = validate(allargs)

        # assert
        assert result == False

    def test_validate_rejects_invalid_version(self, allargs):
        # arrange
        allargs.version = 100

        # act
        result = validate(allargs)

        # assert
        assert result == False

    def test_validate_rejects_invalid_sensitivity_level(self, allargs):
        # arrange
        allargs.sensitivity = "INVALID sensitivity level!!!"

        # act
        result = validate(allargs)

        # assert
        assert result == False


class TestGenerateManifest:
    @pytest.fixture
    def temp_dataset(self, tmp_path):
        test_file = tmp_path / "test_file.csv"
        test_file.write_text("a, b, c")
        return tmp_path

    @pytest.fixture
    def manifest_output(self, tmp_path):
        return str(tmp_path / "folder.mani")

    @pytest.fixture
    def generated_manifest(self, temp_dataset, manifest_output):
        GenerateManifest(
            path=str(temp_dataset),
            sourceName='ons_tdz',
            description='Test dataset',
            version='1',
            dataset='my_dataset',
            sensitivity='low',
            iterationl1=None,
            iterationl2=None,
            iterationl3=None,
            iterationl4=None,
            schemaVersion=1,
            output_path=manifest_output
        )
        with open(manifest_output) as manifest_file:
            return json.load(manifest_file)

    def test_generate_manifest_contains_dataset_name(self, generated_manifest):
        assert generated_manifest["dataset"] == "my_dataset"

    def test_generate_manifest_contains_description(self, generated_manifest):
        assert generated_manifest["description"] == "Test dataset"

    def test_generate_manifest_contains_files(self, generated_manifest):
        assert "files" in generated_manifest

        assert generated_manifest["files"][0]["md5sum:"] == '64f47382e7ddc46583bf6d2abedf4140'
        assert generated_manifest["files"][0]["name:"] == 'test_file.csv'
        assert generated_manifest["files"][0]["sizeBytes:"] == 7

        # TODO: Note colon in key names. i.e., "name:" - should they be there?
        assert "md5sum:" in generated_manifest["files"][0]
        assert "name:" in generated_manifest["files"][0]
        assert "relativePath:" in generated_manifest["files"][0]
        assert "sizeBytes:" in generated_manifest["files"][0]

    def test_generate_manifest_contains_full_size_megabytes(self, generated_manifest):
        assert generated_manifest["fullSizeMegabytes"] == "0.000007"

    def test_generate_manifest_contains_iteration_l1(self, generated_manifest):
        assert generated_manifest["iterationL1"] == ""

    def test_generate_manifest_contains_iteration_l2(self, generated_manifest):
        assert generated_manifest["iterationL2"] == ""

    def test_generate_manifest_contains_iteration_l3(self, generated_manifest):
        assert generated_manifest["iterationL3"] == ""

    def test_generate_manifest_contains_iteration_l4(self, generated_manifest):
        assert generated_manifest["iterationL4"] == ""

    def test_generate_manifest_contains_manifest_created_time(self, generated_manifest):
        assert "manifestCreated" in generated_manifest

    def test_generate_manifest_contains_schema_version(self, generated_manifest):
        assert generated_manifest["schemaVersion"] == 1

    def test_generate_manifest_contains_sensitivity_level(self, generated_manifest):
        assert generated_manifest["sensitivity"] == "low"

    def test_generate_manifest_contains_source_name(self, generated_manifest):
        assert generated_manifest["sourceName"] == "ons_tdz"

    def test_generate_manifest_contains_version_number(self, generated_manifest):
        assert generated_manifest["version"] == 1

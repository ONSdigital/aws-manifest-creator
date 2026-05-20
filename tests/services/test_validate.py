from services.validate import validate


class TestValidatePath:
    def test_validate_rejects_nonexistent_path(self, valid_config):
        # arrange
        valid_config.path = "/blubberwhale/carrotpatch/is/not/a/valid/path"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("path does not exist" in error for error in errors)

    def test_validate_accepts_existing_path(self, valid_config):
        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0


class TestValidateDataset:
    def test_validate_rejects_uppercase_in_dataset_name(self, valid_config):
        # arrange
        valid_config.dataset = "Butterfree_Cumbersome"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("dataset can only contain a-z, 0-9 and _" in error for error in errors)

    def test_validate_rejects_spaces_in_dataset_name(self, valid_config):
        # arrange
        valid_config.dataset = "Baseballbat Crackerjack"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("dataset can only contain a-z, 0-9 and _" in error for error in errors)

    def test_validate_rejects_special_characters_in_dataset_name(self, valid_config):
        # arrange
        valid_config.dataset = "Buckingham_Curdledmilk!?"   # Who typed a question mark on the Teleprompter?! -Anchorman

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("dataset can only contain a-z, 0-9 and _" in error for error in errors)

    def test_validate_accepts_lowercase_alphanumeric_and_underscore_dataset_name(self, valid_config):
        # arrange
        valid_config.dataset = "benedict_cumberbatch_123"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0


class TestValidateVersion:
    def test_validate_rejects_non_integer_version(self, valid_config):
        # arrange
        valid_config.version = "abc"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("version can only be between 0 and 99" in error for error in errors)

    def test_validate_rejects_string_zero_version(self, valid_config):
        # arrange
        valid_config.version = "0"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("version can only be between 0 and 99" in error for error in errors)

    def test_validate_rejects_integer_zero_version(self, valid_config):
        # arrange
        valid_config.version = 0

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("version can only be between 0 and 99" in error for error in errors)

    def test_validate_rejects_negative_version(self, valid_config):
        # arrange
        valid_config.version = -1

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("version can only be between 0 and 99" in error for error in errors)

    def test_validate_rejects_100_or_above(self, valid_config):
        # arrange
        valid_config.version = 100

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("version can only be between 0 and 99" in error for error in errors)

    def test_validate_accepts_version_that_is_in_range(self, valid_config):
        # arrange
        valid_config.version = 5

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_boundary_version_1(self, valid_config):
        # arrange
        valid_config.version = 1

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_boundary_version_99(self, valid_config):
        # arrange
        valid_config.version = 99

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0


class TestValidateSensitivity:
    def test_validate_rejects_invalid_sensitivity(self, valid_config):
        # arrange
        valid_config.sensitivity = "Brandenburg Coddleswort"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("sensitivity can only be one of low, medium, high" in error for error in errors)

    def test_validate_accepts_low_sensitivity(self, valid_config):
        # arrange
        valid_config.sensitivity = "low"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_medium_sensitivity(self, valid_config):
        # arrange
        valid_config.sensitivity = "medium"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_high_sensitivity(self, valid_config):
        # arrange
        valid_config.sensitivity = "high"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_case_insensitive_sensitivity(self, valid_config):
        # arrange
        valid_config.sensitivity = "HIGH"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0


class TestValidateIterations:
    def test_validate_accepts_none_iteration(self, valid_config):
        # arrange
        valid_config.iteration_l1 = None

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_empty_string_iteration(self, valid_config):
        # arrange
        valid_config.iteration_l1 = ""

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_accepts_valid_iteration(self, valid_config):
        # arrange
        valid_config.iteration_l1 = "valid_iteration_01"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert is_valid
        assert len(errors) == 0

    def test_validate_rejects_invalid_characters_in_iteration(self, valid_config):
        # arrange
        valid_config.iteration_l1 = "Buffalo Camouflage!"

        # act
        is_valid, errors = validate(valid_config)

        # assert
        assert not is_valid
        assert any("iteration_l1 can only contain a-z, 0-9 and _" in error for error in errors)

def test_validate_returns_multiple_errors(valid_config):
    # arrange
    valid_config.iteration_l1 = "Billyray Custardbath!"
    valid_config.sensitivity = "Barnabus Cumbersniff"

    # act
    is_valid, errors = validate(valid_config)

    # assert
    assert not is_valid
    assert len(errors) >= 2
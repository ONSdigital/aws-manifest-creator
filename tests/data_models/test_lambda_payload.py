import pytest

from data_models.lambda_payload import ManifestRequest


def test_manifest_request_required_fields_returns_expected_required_fields():
    """Regression test explicitly listing the required fields to
    prevent accidental removal of required fields during refactoring."""
    # arrange
    expected_fields = {
        "session_id",
        "iteration_l1",
        "iteration_l2",
        "iteration_l3",
        "iteration_l4",
    }

    # act
    actual_fields = ManifestRequest.required_fields()

    # assert
    assert set(actual_fields) == expected_fields


def test_manifest_request_missing_fields_lists_all_required_fields_when_payload_is_empty():
    # arrange
    empty_payload = {}

    # act
    missing_fields = ManifestRequest.missing_fields(empty_payload)

    # assert
    assert "session_id" in missing_fields
    assert "iteration_l1" in missing_fields
    assert "iteration_l2" in missing_fields
    assert "iteration_l3" in missing_fields
    assert "iteration_l4" in missing_fields


@pytest.mark.parametrize("missing_field", [
    "session_id",
    "iteration_l1",
    "iteration_l2",
    "iteration_l3",
    "iteration_l4",
])
def test_manifest_request_missing_fields_lists_individual_required_fields_when_field_is_missing_from_payload(missing_field):
    # arrange
    payload = {
        "session_id": "session-123",
        "iteration_l1": "valid_iteration_l1",
        "iteration_l2": "valid_iteration_l2",
        "iteration_l3": "valid_iteration_l3",
        "iteration_l4": "valid_iteration_l4",
    }

    del payload[missing_field]

    # act
    result = ManifestRequest.missing_fields(payload)

    # assert
    assert result == [missing_field]


@pytest.mark.parametrize("partial_payload, expected_missing_fields", [
    (
        {
            "session_id": "session-123",
            "iteration_l1": "valid_iteration_l1",
        },
        ["iteration_l2", "iteration_l3", "iteration_l4"],
    ),
    (
        {
            "session_id": "session-123",
            "iteration_l2": "valid_iteration_l2",
        },
        ["iteration_l1", "iteration_l3", "iteration_l4"],
    ),
    (
        {
            "iteration_l1": "valid_iteration_l1",
            "iteration_l2": "valid_iteration_l2",
        },
        ["session_id", "iteration_l3", "iteration_l4"],
    ),
])
def test_manifest_request_missing_fields_lists_missing_required_fields_when_payload_is_partially_empty(partial_payload, expected_missing_fields):
    # act
    result = ManifestRequest.missing_fields(partial_payload)

    # assert
    assert result == expected_missing_fields


def test_manifest_request_missing_fields_does_not_list_required_fields_when_payload_is_valid():
    # arrange
    valid_payload = {
        "session_id": "session-123",
        "iteration_l1": "valid_iteration_l1",
        "iteration_l2": "valid_iteration_l2",
        "iteration_l3": "valid_iteration_l3",
        "iteration_l4": "valid_iteration_l4",
    }

    # act
    result = ManifestRequest.missing_fields(valid_payload)

    # assert
    assert "session_id" not in result
    assert "iteration_l1" not in result
    assert "iteration_l2" not in result
    assert "iteration_l3" not in result
    assert "iteration_l4" not in result


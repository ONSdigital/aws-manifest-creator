import json
import pytest

from lambda_function import lambda_handler, _extract_payload, _extract_body

@pytest.fixture
def valid_payload():
    return {
        "session_id": "session-123",
        "iteration_l1": "l1-abc",
        "iteration_l2": "l2-abc",
        "iteration_l3": "l3-abc",
        "iteration_l4": "l4-abc",
    }

class TestLambdaHandler:
    def test_lambda_handler_returns_200_for_valid_request(self, valid_payload):
        # arrange
        event = valid_payload

        # act
        response = lambda_handler(event, None)

        # assert
        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == {
            "message": "Request received successfully",
            **event,
        }

    @pytest.mark.parametrize("missing_field", [
        "session_id",
        "iteration_l1",
        "iteration_l2",
        "iteration_l3",
        "iteration_l4",
    ])
    def test_lambda_handler_returns_400_for_missing_field(self, missing_field):
        # arrange
        event = {
            "session_id": "abc123",
            "iteration_l1": "l1",
            "iteration_l2": "l2",
            "iteration_l3": "l3",
            "iteration_l4": "l4",
        }
        del event[missing_field]

        # act
        response = lambda_handler(event, None)

        # assert
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == {
            "message": "Missing required field(s)",
            "missing_fields": [missing_field],
        }

    @pytest.mark.parametrize("partial_event, expected_missing_fields", [
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
    def test_lambda_handler_returns_400_for_multiple_missing_fields(self, partial_event, expected_missing_fields):
        # act
        response = lambda_handler(partial_event, None)

        # assert
        assert response["statusCode"] == 400
        assert json.loads(response["body"]) == {
            "message": "Missing required field(s)",
            "missing_fields": expected_missing_fields,
        }

class TestExtractPayload:
    def test_extract_payload_returns_direct_invoke_dict_as_is(self, valid_payload):
        """Direct Lambda invocation: `event` IS the payload dict, with no
        API Gateway "body" envelope."""
        # act and assert
        assert _extract_payload(valid_payload) == valid_payload

    def test_extract_payload_extracts_json_string_body_from_api_gateway_event(self, valid_payload):
        """API Gateway proxy integration: the payload is JSON-encoded inside
        event["body"], which must be decoded and returned, not the outer event."""
        # arrange
        event = {"body": json.dumps(valid_payload)}

        # act and assert
        assert _extract_payload(event) == valid_payload

    def test_extract_payload_extracts_dict_body_from_api_gateway_event(self, valid_payload):
        """API Gateway event where `body` has already been decoded to a dict
        (e.g. by test tooling or a prior processing step) rather than left
        as a JSON string."""
        # arrange
        event = {"body": valid_payload}

        # act and assert
        assert _extract_payload(event) == valid_payload

    def test_extract_payload_returns_empty_dict_when_api_gateway_body_is_none(self):
        """API Gateway sends `body: null` for requests with no payload at all;
        this should yield an empty payload rather than raising."""
        # arrange
        event = {"body": None}

        # act and assert
        assert _extract_payload(event) == {}

    def test_extract_payload_raises_type_error_for_unsupported_event_type(self):
        """An event that is neither None, a string, nor a dict (e.g. a list or
        an int) has no defined handling and must fail loudly rather than be
        coerced or ignored."""
        # act and assert
        with pytest.raises(TypeError, match="Unsupported event type"):
            _extract_payload(["not", "a", "dict", "or", "string"])

    def test_extract_payload_raises_type_error_when_body_is_unsupported_type(self):
        """An API Gateway-shaped event whose `body` is neither None, a string,
        nor a dict (e.g. a list or int) must fail loudly. This is delegated to
        _extract_body, but the failure must still surface through
        _extract_payload for any caller that only calls the top-level function."""
        # arrange
        event = {"body": 12345}

        # act and assert
        with pytest.raises(TypeError, match="Unsupported body type"):
            _extract_payload(event)

class TestExtractBody:
    def test_extract_body_returns_empty_dict_when_body_is_none(self):
        """No request body present (`body: null`) yields an empty payload."""
        # act and assert
        assert _extract_body(None) == {}

    def test_extract_body_parses_json_encoded_string_body(self, valid_payload):
        """The common API Gateway proxy-integration shape: `body` is a raw
        JSON string that must be decoded into a dict."""
        # arrange
        body = json.dumps(valid_payload)

        # act and assert
        assert _extract_body(body) == valid_payload

    def test_extract_body_returns_dict_body_as_is(self, valid_payload):
        """`body` may already be a dict (e.g. supplied directly by test
        tooling); it should be returned unchanged."""
        # act and assert
        assert _extract_body(valid_payload) == valid_payload

    def test_extract_body_raises_json_decode_error_for_malformed_json_string(self):
        """A `body` string that isn't valid JSON must surface as a
        JSONDecodeError so the caller can return a 400, rather than being
        misinterpreted or silently dropped."""
        # arrange
        malformed_json = "{not valid json"

        # act and assert
        with pytest.raises(json.JSONDecodeError):
            _extract_body(malformed_json)

    def test_extract_body_raises_type_error_for_unsupported_body_type(self):
        """A `body` that is neither None, a string, nor a dict (e.g. a list,
        int, or bool) has no defined handling and must fail loudly."""
        # act and assert
        with pytest.raises(TypeError, match="Unsupported body type"):
            _extract_body(["not", "a", "dict", "or", "string"])

    def test_extract_body_raises_type_error_for_numeric_body(self):
        """Guards a specific unsupported shape (a bare number) separately from
        the list case above, so the failure mode for each shape is documented
        individually rather than only covered incidentally."""
        # act and assert
        with pytest.raises(TypeError, match="Unsupported body type"):
            _extract_body(42)



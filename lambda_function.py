import json
import logging

from data_models.lambda_payload import ManifestRequest

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Entry point for the Lambda function."""
    try:
        payload = _extract_payload(event)
    except (json.JSONDecodeError, TypeError) as err:
        logger.error("Failed to parse event payload: %s", err)
        return _json_response(400, {
            "message": "Invalid request payload",
            "error": str(err),
        })

    missing_fields = ManifestRequest.missing_fields(payload)

    if missing_fields:
        logger.warning("Missing required field(s): %s", missing_fields)
        return _json_response(400, {
            "message": "Missing required field(s)",
            "missing_fields": missing_fields,
        })

    manifest_request = ManifestRequest.from_payload(payload)
    logger.info("Received valid payload for session_id=%s", manifest_request.session_id)

    return _json_response(200, {
        "message": "Request received successfully",
        **manifest_request.to_dict(),
    })

def _extract_payload(event):
    if isinstance(event, dict) and "body" in event:
        return _extract_body(event["body"])
    if isinstance(event, dict):
        return event
    raise TypeError(f"Unsupported event type {type(event)}")


def _extract_body(body):
    if body is None:
        return {}
    if isinstance(body, str):
        return json.loads(body)
    if isinstance(body, dict):
        return body
    raise TypeError(f"Unsupported body type {type(body)}")


def _json_response(status_code, body_dict):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body_dict),
    }

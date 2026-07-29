from lambda_function import lambda_handler


def test_lambda_handler_returns_200():
    # act
    result = lambda_handler({}, None)

    # assert
    assert result["status_code"] == 200

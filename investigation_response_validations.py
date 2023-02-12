from datetime import datetime

ERROR_MESSAGE = "expected {} to be {}, but actual is {}"


def validate_investigation_json(actual_response_json, expected_name, expected_amount):
    """
    example investigation response format
    "createdAt": "2023-02-10T04:47:25.073Z",
    "name": "Ema Nymptom",
    "amount": "$13",
    "investigationId": "17"

    :param actual_response_json: <request response.json()>
    :param expected_name: <str>
    :param expected_amount: <str>
    :return: None
    """
    expected_fields = ["name", "amount", "investigaitonId", "createdAt"]
    assert actual_response_json['name'] == expected_name, ERROR_MESSAGE.format(
        expected_name, actual_response_json['name']
    )
    assert actual_response_json['amount'] == expected_amount, ERROR_MESSAGE.format(
        expected_amount, actual_response_json['amount']
    )
    try:
        int(actual_response_json["investigationId"])
    except ValueError:
        raise AssertionError(
            f"expected investigationId to be an integer format, actual id '{actual_response_json['investigationId']}'")
    try:
        datetime.strptime(actual_response_json['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        raise AssertionError(
            f"createdAt '{actual_response_json['createdAt']}' "
            f"is not in expected datetime format '%Y-%m-%dT%H:%M:%S.%fZ'")
    assert len(actual_response_json) == len(expected_fields), (
        f"expected fields {expected_fields}, actual response {actual_response_json}")

import requests

BASE_URL = ""
API_TYPE = "investigations"
DEFAULT_AUTH = {"X-API-Key": "test"}
DEFAULT_HEADERS = {"Accept": "application/json"}
DEFAULT_ERROR_FOR_STATUS = "expected status of '{}' but actual is '{}'"
SORTBY_OPTIONS = ["createdAt", "name", "amount", "investigationId"]
ORDER_OPTIONS = ["asc", "desc"]


def get_investigations(
        auth=DEFAULT_AUTH, request_headers=DEFAULT_HEADERS, expected_status=200,
        limit=None, page=None, sortBy=None, order=None, search=None
):
    query_params = auth
    if limit:
        query_params["limit"] = limit
    if page:
        query_params["page"] = page
    if sortBy:
        query_params['sortBy'] = sortBy
    if order:
        query_params['order'] = order
    if search:
        query_params['search'] = search

    response = requests.get(
        f"{BASE_URL}/{API_TYPE}",
        params=query_params,
        headers=request_headers
    )
    assert response.status_code == expected_status, DEFAULT_ERROR_FOR_STATUS.format(
        expected_status, response.status_code
    )
    return response


def get_investigation(
        investigation_id, auth=DEFAULT_AUTH, request_headers=DEFAULT_HEADERS, expected_status=200
):
    response = requests.get(
        f"{BASE_URL}/{API_TYPE}/{investigation_id}",
        params=auth,
        headers=request_headers
    )
    assert response.status_code == expected_status, DEFAULT_ERROR_FOR_STATUS.format(
        expected_status, response.status_code
    )
    return response


def post_investigation(name, amount, request_headers=DEFAULT_HEADERS, expected_status=201):
    """
    Creates a new investigation

    :param name: <str> customer name
    :param amount: <str> purchase amount <discuss with dev/po should this enforce a format?>
    :param request_headers: <dict> request headers to include
    :param expected_status: <int> 201 (documentation says 200 <bug reference #>)
    :return: <response>
    response.json() example
    {
        "createdAt": "2023-02-10T04:47:25.073Z",
        "name": "Ema Nymptom",
        "amount": "13.45",
        "investigationId": "17"
    }
    """
    request_body = {}
    if name:
        request_body['name'] = name
    if amount:
        request_body['amount'] = amount

    response = requests.post(
        f"{BASE_URL}/{API_TYPE}",
        json=request_body
    )

    assert response.status_code == expected_status, DEFAULT_ERROR_FOR_STATUS.format(
        expected_status, response.status_code
    )
    return response


def put_investigation(investigation_id, name=None, amount=None, request_headers=DEFAULT_HEADERS, expected_response=200):
    """
    suggest PATCH for next version since a partial update is made
    204 status is documented but 200 is actual <insert bug reference to fix documentation>
    """
    request_body = {}
    if name:
        request_body['name'] = name
    if amount:
        request_body['amount'] = amount
    response = requests.put(
        f"{BASE_URL}/{API_TYPE}/{investigation_id}",
        json=request_body,
        headers=request_headers
    )

    assert response.status_code == expected_response, DEFAULT_ERROR_FOR_STATUS.format(
        expected_response, response.status_code)
    return response


def delete_investigation(investigation_id, request_header=DEFAULT_HEADERS, expected_response=200):
    """
    Deletes a single investigation based on Investigation ID supplied

    :param investigation_id: <str>
    :param request_header: <dict>
    :param expected_response: <int>
        documentation expects 204 response but actual is 200 <bug ticket to fix documentation>
    :return: response
    """
    response = requests.delete(
        f"{BASE_URL}/{API_TYPE}/{investigation_id}",
        headers=request_header
    )

    assert response.status_code == expected_response, DEFAULT_ERROR_FOR_STATUS.format(
        expected_response, response.status_code)
    return response


if __name__ == "__main__":
    print(get_investigations().json())

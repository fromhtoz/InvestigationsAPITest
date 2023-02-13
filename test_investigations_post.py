import pytest
import random

from investigations_api_wrapper import post_investigation, delete_investigation
from investigation_response_validations import validate_investigation_json


class TestInvestigationsPost:
    """
    Test class for POST investigations endpoint
    """
    @pytest.fixture(params=[
        ("Ema Nympton", "67.89"),
        ("José Smith", "67.89"),
        ("Jane Doe", "$67"),
        ("Max Bacon", "€20.99")
        ], ids=["ascii", "unicode", "currency no decimal", "euros"]
    )
    def setup_investigation(self, request):
        """
        investigation for use in happy path testings
        :return: <dict> {"expected_name": <str>, "expected_amount": <str>, "response": <request response>
        """
        post_response = post_investigation(
            name=request.param[0],
            amount=request.param[1]
        )
        yield {
            "expected_name": request.param[0],
            "expected_amount": request.param[1],
            "response": post_response
        }
        delete_investigation(post_response.json()['investigationId'])

    def test_post_response_base(self, setup_investigation):
        validate_investigation_json(
            setup_investigation['response'].json(),
            setup_investigation['expected_name'],
            setup_investigation['expected_amount']
        )

    def test_post_response_error_missing_name(self):
        response = post_investigation(name=None, amount="12.00", expected_status=400)
        assert "expected error" in response.text
        # this is creating an entry in error, maybe account for clean up?

    # some other stubs for later
    @pytest.mark.skip
    def test_post_response_error_missing_amount(self):
        pass

    @pytest.mark.skip
    def test_post_response_error_no_auth(self):
        pass

    @pytest.mark.skip
    def test_post_response_error_bad_header(self):
        pass

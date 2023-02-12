import pytest
import random

from investigations_api_wrapper import post_investigation, delete_investigation
from investigation_response_validations import validate_investigation_json


class TestPostInvestigations:
    name_options = ["Ema Nympton", "José Smith"]  # ask for expected character set
    amount_options = ["$14", "€20", "67.89"]  # ask for formatting options

    @pytest.fixture()
    def setup_investigation(self):
        """
        investigation for use in happy path testings
        :return: <dict> {"expected_name": <str>, "expected_amount": <str>, "response": <request response>
        """
        name = random.choice(self.name_options)
        amount = random.choice(self.amount_options)
        post_response = post_investigation(
            name=name,
            amount=amount
        )
        yield {
            "expected_name": name,
            "expected_amount": amount,
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

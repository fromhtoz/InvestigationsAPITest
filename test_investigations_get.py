import pytest
import random
import string
import logging
from investigations_api_wrapper import post_investigation, delete_investigation, get_investigations, put_investigation
from investigation_response_validations import validate_investigation_json


class TestInvestigationsGet:

    logger = logging.getLogger(__name__)
    @pytest.fixture(scope="class")
    def get_list_information(self):
        """
        Performs setup for testing the list updates when investigations are added, removed, and modified
        :return: <dict>
        """
        name = "Get Test"
        amount = "100.00"
        before_response = get_investigations()
        post_response = post_investigation(
            name,
            amount
        )
        after_post_response = get_investigations()
        new_name = name.join(random.choices(string.ascii_letters, k=5))
        new_amount = str(round(float(amount) + random.random(), 2))
        put_investigation(
            investigation_id=post_response.json()['investigationId'],
            name=new_name,
            amount=new_amount
        )
        after_put_response = get_investigations()
        delete_investigation(post_response.json()['investigationId'])
        after_delete_response = get_investigations()
        yield {
            "before_response": before_response,
            "post_response": post_response,
            "original_name": name,
            "original_amount": amount,
            "after_post_response": after_post_response,
            "new_name": new_name,
            "new_amount": new_amount,
            "after_put_response": after_put_response,
            "after_delete_response": after_delete_response
        }
        # attempt to delete the investigation in case setup failed before the delete request was executed
        delete_investigation(post_response.json()['investigationId'], expected_response=404)

    def test_get_list_count(self, get_list_information):
        """
        Verify the total count is incremented when an investigation is added, and decremented when one is removed
        """
        before_total = int(get_list_information['before_response'].json()['totalResults'])
        after_total = int(get_list_information['after_post_response'].json()['totalResults'])
        assert before_total + 1 == after_total, (
            f"expected 'totalResults' to be {before_total + 1} after new investigation was added, "
            f"but it was {after_total}")
        after_delete_total = int(get_list_information['after_delete_response'].json()['totalResults'])
        assert before_total  == after_delete_total, (
            f"expected 'totalResults' to be {before_total} after new investigation was removed, "
            f"but it was {after_delete_total}")

    def test_get_list_investigation_update_after_add(self, get_list_information):
        """
        Verify the list is updated after an investigation is added
        """
        added_investigation = self.get_investigation_from_list(
            get_list_information['post_response'].json()['investigationId'],
            get_list_information['after_post_response'].json()["investigations"]
        )
        validate_investigation_json(
            added_investigation,
            get_list_information['original_name'],
            get_list_information['original_amount']
        )
        
    def test_get_list_investigation_update_after_modification(self, get_list_information):
        """
        Verify the list is updated after an investigation is changed
        """
        modified_investigation = self.get_investigation_from_list(
            get_list_information['post_response'].json()['investigationId'],
            get_list_information['after_put_response'].json()["investigations"]
        )
        validate_investigation_json(
            modified_investigation,
            get_list_information['new_name'],
            get_list_information['new_amount']
        )

    def test_get_list_investigation_update_after_removal(self, get_list_information):
        """
        Verify the list is updated after an investigation is removed
        """
        assert self.get_investigation_from_list(
            get_list_information['post_response'].json()['investigationId'],
            get_list_information['after_delete_response'].json()["investigations"]
        ) is None, (f"expected investigation '{get_list_information['post_response'].json()['investigationId']}' "
                    f"to be removed but it is still present")

    @staticmethod
    def get_investigation_from_list(investigation_id, investigation_list):
        """
        Finds the investigation from a list and returns it

        :param investigation_id: <str> the investigation to return
        :param investigation_list: <list> the "investigations" field of a get response
        :return: <dict> of the investigation if found , else None
        """
        for investigation in investigation_list:
            if investigation['investigationId'] == investigation_id:
                return investigation

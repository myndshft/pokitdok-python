from __future__ import absolute_import

import pokitdok
import datetime
import json
import tests
import copy
import platform
from unittest import TestCase
import requests
from tests import client_settings

class TestAPIClient(object):
    """
    Validates that PokitDok API client requests are well formed.
    Httmock (https://pypi.python.org/pypi/httmock/) is used to provide mock HTTP responses.
    """
    ASSERTION_EQ_MSG = 'Expected {} != Actual {}'
    def __init__(self):
        """
            Defines instance attributes used in test cases
            - pd_client = PokitDok API client instance
            - current_request = The requests request object for the current test case request
        """
        self.pd_client = pokitdok.api.connect(**client_settings)

    #
    # ******************************
    # client set up tests
    # ******************************
    #

    def test_connect(self):
        """
        tests the basic init of the client
        :return:
        """
        assert self.pd_client.api_client is not None
        assert self.pd_client.api_client.token is not None
        assert "pokitdok-python" in self.pd_client.base_headers["User-Agent"],\
            self.ASSERTION_EQ_MSG.format("pokitdok-python", self.pd_client.base_headers)

    def test_connect_existing_token(self):
        """
            Tests pokitdok.api.connect (PokitDok.__init__()) with an existing token
            Validates that the API client instantiation supports an existing token
        """
        self.pd_client = pokitdok.api.connect(**client_settings)
        first_token = copy.deepcopy(self.pd_client.token)

        self.pd_client = pokitdok.api.connect(token=first_token, **client_settings)
        second_token = copy.deepcopy(self.pd_client.token)
        # first token should be equal to the second
        assert first_token == second_token

        # validate unique tokens for new client instances
        self.pd_client = pokitdok.api.connect(**client_settings)
        third_token = copy.deepcopy(self.pd_client.token)
        assert third_token not in [first_token, second_token]

    #
    # ******************************
    # error tests
    # ******************************
    #

    def test_http_error_400(self):
        """
        Error Test: test for an expected 400 response via a missing trading_partner id
        """
        self.pd_client = pokitdok.api.connect(**client_settings)
        request = {
            "member": {
                "birth_date": "1970-01-25",
                "first_name": "Jane",
                "last_name": "Doe",
                "id": "W000000000"
            },
            "provider": {
                "first_name": "JEROME",
                "last_name": "AYA-AY",
                "npi": "1467560003"
            },
        }
        response = self.pd_client.eligibility(request)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        error_message = "Unable to find configuration for trading_partner_id: None, transaction_set_name: eligibility"
        assert error_message in response["data"]["errors"]["query"], \
            self.ASSERTION_EQ_MSG.format(error_message, response["data"]["errors"]["query"])
        assert self.pd_client.status_code == 400, self.ASSERTION_EQ_MSG.format("400", self.pd_client.status_code)

    def test_http_error_422(self):
        """
        Error Test: test for an expected 422 response via different types of bad requests
        """
        self.pd_client = pokitdok.api.connect(**client_settings)
        request = "bad request"
        response = self.pd_client.eligibility(request)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        error_message = "This endpoint only accepts JSON requests of <type 'dict'>. Request provided was of <type 'unicode'>."
        assert error_message in response["data"]["errors"]["validation"], \
            self.ASSERTION_EQ_MSG.format(error_message, response["data"]["errors"]["query"])
        assert self.pd_client.status_code == 422, self.ASSERTION_EQ_MSG.format("422", self.pd_client.status_code)

        request = {
            "member": {
                "birth_date": "1970-01-25",
                "first_name": "Jane",
                "last_name": "Doe",
                "id": "1"
            },
            "trading_partner_id": 'MOCKPAYER'
        }
        response = self.pd_client.eligibility(request)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        error_message = "String value is too short."
        assert error_message in response["data"]["errors"]["validation"]["member"]["id"], \
            self.ASSERTION_EQ_MSG.format(error_message, response["data"]["errors"]["query"])
        assert self.pd_client.status_code == 422, self.ASSERTION_EQ_MSG.format("422", self.pd_client.status_code)

        request = {
            "member": {
                "birth_date": "1970-01-25",
                "first_name": "Jane",
                "last_name": "Doe",
                "id": "W000000000"
            },
            "provider": {
                "first_name": "JEROME",
                "last_name": "AYA-AY",
                "npi": "3"
            },
            "trading_partner_id": 'MOCKPAYER'
        }
        response = self.pd_client.eligibility(request)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        error_message = "String value is too short."
        assert error_message in response["data"]["errors"]["validation"]["provider"]["npi"], \
            self.ASSERTION_EQ_MSG.format(error_message, response["data"]["errors"]["query"])
        assert self.pd_client.status_code == 422, self.ASSERTION_EQ_MSG.format("422", self.pd_client.status_code)

    #
    # ******************************
    # get/post/put tests
    # ******************************
    #
    #
    def test_post(self):
        """
        POST Test
        """
        self.pd_client = pokitdok.api.connect(**client_settings)
        request = {
            "member": {
                "birth_date": "1970-01-25",
                "first_name": "Jane",
                "last_name": "Doe",
                "id": "W000000000"
            },
            "provider": {
                "first_name": "JEROME",
                "last_name": "AYA-AY",
                "npi": "1467560003"
            },
            "trading_partner_id": "MOCKPAYER"
        }
        response = self.pd_client.request(self.pd_client.eligibility_url, method='post', data=request)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", self.pd_client.status_code)

    def test_put_delete_claims_activities(self):
        """
            Exercise the workflow of submitting a and deleting a claim'
        """
        test_claim = {
            "transaction_code": "chargeable",
            "trading_partner_id": "MOCKPAYER",
            "billing_provider": {
                "taxonomy_code": "207Q00000X",
                "first_name": "Jerome",
                "last_name": "Aya-Ay",
                "npi": "1467560003",
                "address": {
                    "address_lines": [
                        "8311 WARREN H ABERNATHY HWY"
                    ],
                    "city": "SPARTANBURG",
                    "state": "SC",
                    "zipcode": "29301"
                },
                "tax_id": "123456789"
            },
            "subscriber": {
                "first_name": "Jane",
                "last_name": "Doe",
                "member_id": "W000000000",
                "address": {
                    "address_lines": ["123 N MAIN ST"],
                    "city": "SPARTANBURG",
                    "state": "SC",
                    "zipcode": "29301"
                },
                "birth_date": "1970-01-25",
                "gender": "female"
            },
            "claim": {
                "total_charge_amount": 60.0,
                "service_lines": [
                    {
                        "procedure_code": "99213",
                        "charge_amount": 60.0,
                        "unit_count": 1.0,
                        "diagnosis_codes": [
                            "J10.1"
                        ],
                        "service_date": "2016-01-25"
                    }
                ]
            }
        }
        # assert success of the claim post
        response = self.pd_client.claims(test_claim)
        assert response["meta"].keys() is not None
        assert response["data"].keys() is not None
        assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", self.pd_client.status_code)

        # use the activities endpoint via a GET to analyze the current status of this claim
        activity_id = response["meta"]["activity_id"]
        activity_url = "/activities/" + activity_id
        get_response = self.pd_client.request(activity_url, method='get', data={})
        assert get_response["meta"].keys() is not None
        assert get_response["data"].keys() is not None
        assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", self.pd_client.status_code)

        # look in the history to see if it has transitioned from state "init" to "canceled"
        history = get_response["data"]["history"]
        if len(history) != 1:
            # this means that the claim is been picked up and is processing within the internal pokitdok system
            # we aim to test out the put functionality by deleting the claim,
            # so we need to resubmit a claim to get one that is going to stay in the INIT stage
            response = self.pd_client.claims(test_claim)
            assert response["meta"].keys() is not None
            assert response["data"].keys() is not None
            assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", self.pd_client.status_code)
            activity_id = response["meta"]["activity_id"]
            activity_url = "/activities/" + activity_id

        # exercise the PUT functionality to delete the claim from its INIT status
        put_response = self.pd_client.request(activity_url, method='put', data={"transition": "cancel"})
        assert put_response["meta"].keys() is not None
        assert put_response["data"].keys() is not None
        assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", str(put_response))

        # look in the history to see if it has transitioned from state "init" to "canceled"
        history = put_response["data"]["history"]
        assert len(history) == 3, "Tested for cancelled claim, but recived the following claim history: {}".format(str(history))

        # exercise the PUT functionality to delete an already deleted claim
        put_response = self.pd_client.request(activity_url, method='put', data={"transition": "cancel"})
        assert put_response["data"]["errors"] is not None
        assert self.pd_client.status_code == 422, self.ASSERTION_EQ_MSG.format("422", self.pd_client.status_code)

        # exercise the activities endpoint to get the status of this claims transaction
        activities_response = self.pd_client.activities(response["meta"]["activity_id"])
        assert activities_response["meta"] is not None
        assert activities_response["data"] is not None
        assert self.pd_client.status_code == 200, self.ASSERTION_EQ_MSG.format("200", self.pd_client.status_code)

        # exercise the activities endpoint to get the status of this claims transaction
        activities_response = self.pd_client.activities(response["meta"]["activity_id"])
        assert activities_response["meta"] is not None
        assert activities_response["data"] is not None
        assert self.pd_client.status_code == 404, self.ASSERTION_EQ_MSG.format("404", self.pd_client.status_code)
        assert "is not a valid Activity Id" in activities_response["data"]["errors"]["query"]

#     def test_activities(self):
#         """
#             Tests PokitDok.activities.
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.activities()
#         assert mocked_response is not None
#
#     def test_activities_with_activity_id(self):
#         """
#             Tests PokitDok.activities with a specific activity id
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.activities('activity_id')
#         assert mocked_response is not None
#
#     def test_cash_prices(self):
#         """
#             Tests PokitDok.cash_prices
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.cash_prices(zip_code='94101', cpt_code='95017')
#         assert mocked_response is not None
#
#     def test_ccd(self):
#         """
#             Tests PokitDok.ccd
# \        """
#         with HTTMock(self.mock_api_response):
#             ccd_request = {'trading_partner_id': 'MOCKPAYER'}
#             mocked_response = self.pd_client.ccd(ccd_request)
#         assert mocked_response is not None
#
#     def test_claims(self):
#         """
#             Tests PokitDok.claims
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.claims(tests.claim_request)
#         assert mocked_response is not None
#
#     def test_claims_status(self):
#         """
#             Tests PokitDok.claims_status
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.claims_status(tests.claim_status_request)
#         assert mocked_response is not None
#
#     def test_mpc_code_lookup(self):
#         """
#             Tests PokitDok.mpc (medical procedure code) lookup for a specific code
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.mpc(code='99213')
#         assert mocked_response is not None
#
#     def test_mpc_query(self):
#         """
#             Tests PokitDok.mpc (medical procedure code) query
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.mpc(name='office')
#         assert mocked_response is not None
#
#     def test_icd_convert(self):
#         """
#             Tests PokitDok.icd_convert
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.icd_convert(code='250.12')
#         assert mocked_response is not None
#
#     def test_claims_convert(self):
#         """
#             Tests PokitDok.claims_convert
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.claims_convert(**tests.claims_convert_request)
#         assert mocked_response is not None
#
#     def test_eligibility(self):
#         """
#             Tests PokitDok.eligibility
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.eligibility(tests.eligibility_request)
#         assert mocked_response is not None
#
#     def test_enrollment(self):
#         """
#             Tests PokitDok.enrollment
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.enrollment(tests.enrollment_request)
#         assert mocked_response is not None
#
#     def test_enrollment_snapshot(self):
#         """
#             Tests PokitDok.enrollment_snapshot
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.enrollment_snapshot(**tests.enrollment_snapshot_request)
#         assert mocked_response is not None
#
#     def test_enrollment_snapshots(self):
#         """
#             Tests PokitDok.enrollment_snapshots
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.enrollment_snapshots(snapshot_id='12345')
#         assert mocked_response is not None
#
#     def test_enrollment_snapshot_data(self):
#         """
#             Tests PokitDok.enrollment_snapshot_data
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.enrollment_snapshot_data(snapshot_id='12345')
#         assert mocked_response is not None
#
#     def test_insurance_prices(self):
#         """
#             Tests PokitDok.insurance_prices
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.insurance_prices(cpt_code='87799', zip_code='32218')
#         assert mocked_response is not None
#
#     # ENDPOINT DEPRECATION NOTICE
#     # this test will be removed in a future release
#     def test_payers(self):
#         """
#             Tests PokitDok.payers
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.payers()
#         assert mocked_response is not None
#
#     def test_plans(self):
#         """
#             Tests PokitDok.plans
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.plans()
#         assert mocked_response is not None
#
#     def test_plans_by_state_type(self):
#         """
#             Tests PokitDok.plans lookup with state and plan type criteria
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.plans(state='SC', type='PPO')
#         assert mocked_response is not None
#
#     def test_providers_npi(self):
#         """
#             Tests PokitDok.providers lookup by NPI
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.providers(npi='1467560003')
#         assert mocked_response is not None
#
#     def test_providers_search(self):
#         """
#             Tests PokitDok.providers search by zipcode, specialty, and radius
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.providers(zipcode='29307',
#                                                        specialty='rheumatology',
#                                                        radius='20mi')
#         assert mocked_response is not None
#
#     def test_trading_partners(self):
#         """
#             Tests PokitDok.trading_partners
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.trading_partners()
#         assert mocked_response is not None
#
#     def test_trading_partners_trading_partner_id(self):
#         """
#             Tests PokitDok.trading_partners lookup by trading_partner_id
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.trading_partners(trading_partner_id='MOCKPAYER')
#         assert mocked_response is not None
#
#     def test_referrals(self):
#         """
#             Tests PokitDok.referrals
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.referrals(tests.referrals_request)
#         assert mocked_response is not None
#
#     def test_authorizations(self):
#         """
#             Tests PokitDok.authorizations
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.authorizations(tests.authorization_request)
#         assert mocked_response is not None
#
#     def test_schedulers(self):
#         """
#             Tests PokitDok.schedulers
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.schedulers()
#         assert mocked_response is not None
#
#     def test_schedulers_with_scheduler_uuid(self):
#         """
#             Tests PokitDok.schedulers lookup for a specific resource
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.schedulers(scheduler_uuid='967d207f-b024-41cc-8cac-89575a1f6fef')
#         assert mocked_response is not None
#
#     def test_appointment_types(self):
#         """
#             Tests PokitDok.appointment_types
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.appointment_types()
#         assert mocked_response is not None
#
#     def test_appointment_types_with_appointment_type_uuid(self):
#         """
#             Tests PokitDok.schedulers lookup for a specific resource
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.appointment_types(
#                 appointment_type_uuid='ef987693-0a19-447f-814d-f8f3abbf4860')
#         assert mocked_response is not None
#
#     def test_schedule_slots(self):
#         """
#             Tests PokitDok.schedule_slots
#         :return:
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.schedule_slots(tests.slot_create_request)
#         assert mocked_response is not None
#
#     def test_appointments_with_appointment_uuid(self):
#         """
#             Tests PokitDok.appointments lookup for a specific resource
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.appointments(appointment_uuid='ef987691-0a19-447f-814d-f8f3abbf4859')
#         assert mocked_response is not None
#
#     def test_appointments_with_search(self):
#         """
#             Tests PokitDok.appointments lookup using search criteria: appointment_type, start_date, and end_date
#         """
#         with HTTMock(self.mock_api_response):
#             search_criteria = {
#                 'appointment_type': 'AT1',
#                 'start_date': datetime.date(2016, month=1, day=15),
#                 'end_date': datetime.date(2016, month=1, day=20),
#             }
#             mocked_response = self.pd_client.appointments(**search_criteria)
#         assert mocked_response is not None
#
#     def test_book_appointment(self):
#         """
#             Tests PokitDok.book_appointment
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.book_appointment('ef987691-0a19-447f-814d-f8f3abbf4859',
#                                                               tests.appointment_book_request)
#         assert mocked_response is not None
#
#     def test_cancel_appointment(self):
#         """
#             Tests PokitDok.cancel_appointment
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.cancel_appointment(appointment_uuid='ef987691-0a19-447f-814d-f8f3abbf4859')
#         assert mocked_response is not None
#
#     def test_create_identity(self):
#         """
#             Tests PokitDok.create_identity
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.create_identity(tests.identity_request)
#         assert mocked_response is not None
#
#     def test_identity_with_uuid(self):
#         """
#             Tests PokitDok.identity lookup for a specific resource
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.identity(identity_uuid='881bc095-2068-43cb-9783-cce63036412')
#         assert mocked_response is not None
#
#     def test_identity_search(self):
#         """
#             Tests PokitDok.identity with search criteria of first_name and last_name
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.identity(first_name='Oscar', last_name='Whitmire')
#         assert mocked_response is not None
#
#     def test_update_identity(self):
#         """
#             Tests PokitDok.create_identity
# \        """
#         with HTTMock(self.mock_api_response):
#             updated_request = copy.deepcopy(tests.identity_request)
#             updated_request['email'] = 'oscar@yahoo.com'
#
#             mocked_response = self.pd_client.update_identity(identity_uuid='881bc095-2068-43cb-9783-cce63036412',
#                                                              identity_request=updated_request)
#         assert mocked_response is not None
#
#     def test_identity_history_with_uuid(self):
#         """
#             Tests PokitDok.identity_history lookup to return a change summary for a specific resource
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.identity_history(identity_uuid='881bc095-2068-43cb-9783-cce63036412')
#         assert mocked_response is not None
#
#     def test_identity_history_with_uuid_version(self):
#         """
#             Tests PokitDok.identity_history lookup for a version of a specific resource
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.identity_history(identity_uuid='881bc095-2068-43cb-9783-cce63036412',
#                                                               historical_version=1)
#         assert mocked_response is not None
#
#     def test_identity_match(self):
#         """
#             Tests PokitDok.identity_match
# \        """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.identity_match(tests.identity_match_request)
#         assert mocked_response is not None
#
#     def test_pharmacy_plans(self):
#         """
#             Tests PokitDok.pharmacy_plans
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.pharmacy_plans(trading_partner_id='MOCKPAYER', plan_number='S5820003')
#         assert mocked_response is not None
#
#     def test_pharmacy_formulary(self):
#         """
#             Tests PokitDok.pharmacy_formulary
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.pharmacy_formulary(trading_partner_id='MOCKPAYER', plan_number='S5820003',
#                                                                 ndc='59310-579-22')
#         assert mocked_response is not None
#
#     def test_pharmacy_network_by_npi(self):
#         """
#             Tests PokitDok.pharmacy_network by NPI
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.pharmacy_network(trading_partner_id='MOCKPAYER', plan_number='S5596033',
#                                                                 npi='1912301953')
#         assert mocked_response is not None
#
#     def test_pharmacy_network_search(self):
#         """
#             Tests PokitDok.pharmacy_network search
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.pharmacy_network(trading_partner_id='MOCKPAYER', plan_number='S5596033',
#                                                                 zipcode='94401', radius='10mi')
#         assert mocked_response is not None
#
#     def test_oop_insurance_prices(self):
#         """
#             Tests PokitDok.oop_insurance_prices
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.oop_insurance_prices({
#                 'trading_partner_id': 'MOCKPAYER',
#                 'cpt_bundle': ['81291', '99999'],
#                 'price': {
#                     'amount': '1300',
#                     'currency': 'USD'
#                 }
#             })
#         assert mocked_response is not None
#
#     def test_oop_insurance_estimate(self):
#         """
#             Tests PokitDok.oop_insurance_estimate
#         """
#         with HTTMock(self.mock_api_response):
#             mocked_response = self.pd_client.oop_insurance_estimate({
#                 "trading_partner_id": "MOCKPAYER",
#                 "cpt_bundle": ['81291', '99999'],
#                 "eligibility": {
#                     "member": {
#                         "birth_date": "1972-02-25",
#                         "first_name": "Mose",
#                         "last_name": "Def",
#                         "id": "999999999"
#                     }
#                 }
#             })
#         assert mocked_response is not None
#
#     def test_connect_refresh_token(self):
#         """
#             Tests pokitdok.api.connect and getting a refresh token
#             Validates that the API client instantiation supports an existing token and refreshing a token for auto_refresh
#         """
#         with HTTMock(self.mock_oauth2_token):
#             # get token initial token
#             self.pd_client = pokitdok.api.connect(self.CLIENT_ID, self.CLIENT_SECRET, auto_refresh=True)
#             first_token = copy.deepcopy(self.pd_client.token)
#
#             # expire the token and make sure new token is created and not the same as first token
#             self.pd_client.token['expires_in'] = -10
#             self.pd_client = pokitdok.api.connect(self.CLIENT_ID, self.CLIENT_SECRET, token=self.pd_client.token, auto_refresh=True)
#
#             # attempt to make a call, which should get new token...thus auto_refresh working
#             mocked_response = self.pd_client.pharmacy_plans(trading_partner_id='MOCKPAYER', plan_number='S5820003')
#             assert mocked_response is not None
#             second_token = copy.deepcopy(self.pd_client.token)
#             assert first_token != second_token
#
#             # attempt to make a call, which should NOT get a new token. Shows that token_updater is working to
#             # reset token on PokitDokClient
#             mocked_response = self.pd_client.pharmacy_plans(trading_partner_id='MOCKPAYER', plan_number='S5820003')
#             assert mocked_response is not None
#             third_token = copy.deepcopy(self.pd_client.token)
#             assert second_token == third_token

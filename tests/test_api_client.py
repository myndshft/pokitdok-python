from __future__ import absolute_import

import os
import pokitdok
from unittest import TestCase
import vcr


#Fake client id/secret for local testing
CLIENT_ID = 'HriWakiWYQuCm5IK7yPp'
CLIENT_SECRET = 'jPb7EivoN6qaK9RF9lU8vtfqtjuEq82AruVpGPVA'
BASE_URL = 'http://localhost:5002'
os.environ['DEBUG'] = 'True'


pd_vcr = vcr.VCR(
    cassette_library_dir='tests/fixtures/vcr_cassettes',
    record_mode='once',
    filter_headers=['authorization']
)


class TestAPIClient(TestCase):

    def setUp(self):
        with pd_vcr.use_cassette('access_token.yml'):
            self.pd = pokitdok.api.connect(CLIENT_ID, CLIENT_SECRET, base=BASE_URL)
            assert isinstance(self.pd, pokitdok.api.PokitDokClient)

    def test_activities(self):
        with pd_vcr.use_cassette('activities.yml'):
            activities_response = self.pd.activities()
            assert "meta" in activities_response
            assert "data" in activities_response

    def test_eligibility(self):
        with pd_vcr.use_cassette('eligibility.yml'):
            eligibility_response = self.pd.eligibility({
                "member": {
                    "birth_date": "1970-01-01",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "id": "W000000000"
                },
                "provider": {
                    "first_name": "JEROME",
                    "last_name": "AYA-AY",
                    "npi": "1467560003"
                },
                "service_types": ["health_benefit_plan_coverage"],
                "trading_partner_id": "MOCKPAYER"
            })
            assert "meta" in eligibility_response
            assert "data" in eligibility_response
            print(len(eligibility_response['data']['coverage']['deductibles']))
            assert len(eligibility_response['data']['coverage']['deductibles']) == 8

    def test_payers(self):
        with pd_vcr.use_cassette('payers.yml'):
            payers_response = self.pd.payers()
            assert "meta" in payers_response
            assert "data" in payers_response
            for payer in payers_response['data']:
                assert 'trading_partner_id' in payer

    def test_providers_with_id(self):
        with pd_vcr.use_cassette('providers_id.yml'):
            providers_response = self.pd.providers(npi='1467560003')
            assert "meta" in providers_response
            assert "data" in providers_response
            assert providers_response['data']['provider']['last_name'] == 'AYA-AY'
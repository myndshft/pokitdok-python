from __future__ import absolute_import

import os
import pokitdok
from unittest import TestCase
import vcr


#Fake client id/secret for local testing
CLIENT_ID = 'RqBJvsK2TyFxNHT8m89g'
CLIENT_SECRET = 'OFQjUABycPb7OT08JKJ8hbTu0Tn4Es76tcrNahcg'
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
                "trading_partner_id": "MOCKPAYER",
                "member_id": "W0000000000",
                "provider_id": "1467560003",
                "provider_name": "AYA-AY",
                "provider_first_name": "JEROME",
                "provider_type": "Person",
                "member_name": "JOHN DOE",
                "member_birth_date": "01/01/1970",
                "service_types": ["Health Benefit Plan Coverage"]
            })
            assert "meta" in eligibility_response
            assert "data" in eligibility_response

    def test_providers_with_id(self):
        with pd_vcr.use_cassette('providers_id.yml'):
            providers_response = self.pd.providers(provider_id='1467560003')
            assert "meta" in providers_response
            assert "data" in providers_response
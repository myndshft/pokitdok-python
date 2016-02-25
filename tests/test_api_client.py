from __future__ import absolute_import

import pokitdok
import nose.tools
from httmock import urlmatch, HTTMock, response, all_requests
import datetime
import json
import requests


class TestAPIClient(object):
    """
    Validates that PokitDok API client requests are well formed.
    Httmock (https://pypi.python.org/pypi/httmock/) is used to provide mock HTTP responses.
    """
    BASE_URL = 'https://platform.pokitdok.com/v4/api'
    CLIENT_ID = 'F7q38MzlwOxUwTHb7jvk'
    CLIENT_SECRET = 'O8DRamKmKMLtSTPjK99eUlbfOQEc44VVmp8ARmcY'
    MATCH_NETWORK_LOCATION = r'(.*\.)?pokitdok\.com'
    MATCH_OAUTH2_PATH = r'[/]oauth2[/]token'
    TEST_REQUEST_PATH = '/endpoint'

    def __init__(self):
        """
            Defines test case attributes
            - pd_client: The PokitDok API client instance
            - current_request: The generated requests request object for the current test
        """
        self.pd_client = None
        self.current_request = None

    @urlmatch(netloc=MATCH_NETWORK_LOCATION, path=MATCH_OAUTH2_PATH, method='POST')
    def mock_oauth2_token(self, url, request):
        """
            Returns a mocked OAuth2 token response
            :param url: The request url
            :param request: The requests request object
            :return: mocked OAuth2 token response
        """
        headers = {
            'Server': 'nginx',
            'Date': datetime.datetime.utcnow(),
            'Content-type': 'application/json;charset=UTF-8',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-store'
        }

        content = {
            'access_token': 's8KYRJGTO0rWMy0zz1CCSCwsSesDyDlbNdZoRqVR',
            'token_type': 'bearer',
            'expires': 1393350569,
            'expires_in': 3600
        }

        headers['Content-Length'] = len(json.dumps(content))

        return response(status_code=200, content=content, headers=headers, request=request)

    @urlmatch(netloc=MATCH_NETWORK_LOCATION)
    def mock_api_response(self, url, request):
        """
            Processes an incoming API request and returns a mocked response.
            The incoming API request is cached and made available to tests.
            :param url: The request url
            :param request: The requests request object
            :return: 200 status code response with an empty content body {}
        """
        self.current_request = request
        return response(status_code=200, content={}, request=request)

    def setUp(self):
        """
            Creates a new PokitDok client instance
        """
        with HTTMock(self.mock_oauth2_token):
            self.pd_client = pokitdok.api.connect(self.CLIENT_ID, self.CLIENT_SECRET)

    def test_connect(self):
        """
            Tests pokitdok.api.connect (PokitDok.__init__())
            Validates that the API client is instantiated and has an access token.
        """
        with HTTMock(self.mock_oauth2_token):
            self.pd_client = pokitdok.api.connect(self.CLIENT_ID, self.CLIENT_SECRET)
            nose.tools.assert_is_not_none(self.pd_client.api_client)
            nose.tools.assert_is_not_none(self.pd_client.api_client.token)

    def test_request_post(self):
        """
            Tests the PokitDok.request convenience method with a POST request.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            self.pd_client.request(self.TEST_REQUEST_PATH, method='post', data={'param': 'value'})
            nose.tools.assert_dict_contains_subset(self.pd_client.json_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'POST')

    def test_request_get(self):
        """
            Tests the PokitDok.request convenience method with a GET request.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            self.pd_client.request(self.TEST_REQUEST_PATH, method='get')
            nose.tools.assert_dict_contains_subset(self.pd_client.base_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'GET')

    def test_get(self):
        """
            Tests the PokitDok.get convenience method.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            self.pd_client.get(self.TEST_REQUEST_PATH)
            nose.tools.assert_dict_contains_subset(self.pd_client.base_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'GET')

    def test_post(self):
        """
            Tests the PokitDok.post convenience method.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            self.pd_client.post(self.TEST_REQUEST_PATH, data={'field': 'value'})
            nose.tools.assert_dict_contains_subset(self.pd_client.json_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'POST')

    def test_put(self):
        """
            Tests the PokitDok.put convenience method.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            url = '{0}/{1}'.format(self.TEST_REQUEST_PATH, 123456)
            self.pd_client.put(url, data={'first_name': 'Oscar', 'last_name': 'Whitmire'})
            nose.tools.assert_dict_contains_subset(self.pd_client.json_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'PUT')

    def test_delete(self):
        """
            Tests the PokitDok.delete convenience method.
            Validates that the requests request is configured correctly and has the appropriate headers.
        """
        with HTTMock(self.mock_api_response):
            url = '{0}/{1}'.format(self.TEST_REQUEST_PATH, 123456)
            self.pd_client.delete(url)
            nose.tools.assert_dict_contains_subset(self.pd_client.base_headers, self.current_request.headers)
            nose.tools.assert_equal(self.current_request.method, 'DELETE')

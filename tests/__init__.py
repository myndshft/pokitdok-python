from tests.resource_requests import *

import os
base_url = 'https://platform.pokitdok.com'
client_id = os.environ['POKITDOK_CLIENT_ID']
client_secret = os.environ['POKITDOK_CLIENT_SECRET']
client_settings = {
    'client_id': client_id,
    'client_secret': client_secret,
    'base': base_url
}

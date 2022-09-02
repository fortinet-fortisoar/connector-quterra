from .make_rest_api_call import MakeRestApiCall
from .get_blacklist_status import get_blacklist_status


def _check_health(config):
    try:
        params = {
            "domain_name": "https://google.com",
            "response_format": "Json"
        }
        resp = get_blacklist_status(config, params)
        return True
    except Exception as e:
        raise Exception(e)
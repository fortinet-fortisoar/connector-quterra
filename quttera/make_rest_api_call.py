import requests
import time
from connectors.core.connector import get_logger, ConnectorError
from connectors.core.utils import update_connnector_config

error_msg = {
    401: 'Authentication failed due to invalid credentials',
    429: 'Rate limit was exceeded',
    403: 'Token is invalid or expired',
    "ssl_error": 'SSL certificate validation failed',
    'time_out': 'The request timed out while trying to connect to the remote server',
}

logger = get_logger("quterra")


class MakeRestApiCall:

    def __init__(self, config):
        self.server_url = config.get('server_url').strip().strip('/')
        if not self.server_url.startswith('http') or not self.server_url.startswith('https'):
            self.server_url = 'https://' + self.server_url
        self.api_key = config.get("api_key")
        self.verify_ssl = config.get("verify_ssl", True)

    def make_request(self, endpoint='', params=None, data=None, method='GET', headers=None, url=None, json_data=None):
        try:
            if url is None:
                url = f"{self.server_url}/api/v3/{self.api_key}{endpoint}"

            response = requests.request(method=method, url=url,
                                        headers=headers, data=data, json=json_data, params=params, verify=self.verify_ssl)

            if response.ok:
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response.text
            else:
                logger.error("Error: {0}".format(response.json()))
                raise ConnectorError('{0}'.format(error_msg.get(response.status_code, response.text)))
        except requests.exceptions.SSLError as e:
            logger.exception('{0}'.format(e))
            raise ConnectorError('{0}'.format(error_msg.get('ssl_error')))
        except requests.exceptions.ConnectionError as e:
            logger.exception('{0}'.format(e))
            raise ConnectorError('{0}'.format(error_msg.get('time_out')))
        except Exception as e:
            logger.error('{0}'.format(e))
            raise ConnectorError('{0}'.format(e))
from .make_rest_api_call import MakeRestApiCall


def start_integrity_scan(config, params):
    domain_name = params.pop("domain_name", '')
    response_format = params.pop('response_format', 'Json')

    endpoint = f"/integrity/scan/{domain_name}.{response_format.lower()}"
    method = "POST"  # GET/POST/PUT/DELETE

    MK = MakeRestApiCall(config=config)
    response = MK.make_request(endpoint=endpoint, method=method, params=params)
    return response
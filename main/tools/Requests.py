import requests

def get_request(url, headers=None, params=None, session=None):
    session = session or requests.session()
    try:
        response = session.get(url, headers=headers, json=params)
        return response
    except Exception as e:
        raise

def post_request(url, headers=None, params=None, session=None):
    session = session or requests.session()
    try:
        response = session.post(url, headers=headers, json=params)
        return response
    except Exception as e:
        raise

def put_request(url, headers=None, params=None, session=None):
    session = session or requests.session()
    try:
        response = session.put(url, headers=headers, json=params)
        return response
    except Exception as e:
        raise
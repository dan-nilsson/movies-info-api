'''
API helper functions
'''
import requests, os, json
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')
SALT = os.getenv('SALT')
SEED_ENDP = os.getenv('SEED_ENDP')

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, 'data.json')

def json_load() -> dict:
    with open(data_path, 'r') as file:
        return json.load(file)

def json_dump(data) -> None:
    with open(data_path, 'w') as file:
        json.dump(data, file, indent=4)

def get_req_json(endpoint,params=None,headers=None,timeout=1):
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.JSONDecodeError:
        print('The returned data was not JSON format.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

def get_req_full(endpoint,params=None,headers=None,timeout=1):
    try:
        response = requests.get(endpoint, params=params, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.JSONDecodeError:
        print('The returned data was not JSON format.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

def post_req_json(endpoint,data,params=None,headers=None,timeout=1) -> None:
    try:
        response = requests.post(endpoint, json=data, params=params, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None


def put_req_json(endpoint, index, data, params=None, headers=None, timeout=1) -> None:
    try:
        response = requests.put(f'{endpoint}/{index}', json=data, params=params, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.InvalidURL:
        print('The index is invalid.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

def patch_req_json(endpoint, index, data, params=None, headers=None, timeout=1) -> None:
    try:
        response = requests.patch(f'{endpoint}/{index}', json=data, params=params, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.InvalidURL:
        print('The index is invalid.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

def delete_req(endpoint, index, params=None, headers=None, timeout=1) -> None:
    try:
        response = requests.delete(f'{endpoint}/{index}', params=params, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.InvalidURL:
        print('The index is invalid.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

def options_req(endpoint, params=None, headers=None, timeout=1) -> None:
    try:
        response = requests.options(endpoint, params=params, headers=headers, timeout=timeout)
        return response
    except requests.exceptions.Timeout:
        print('The request timed out.',response.url)
    except requests.exceptions.ConnectionError:
        print('Could not connect to the server.')
    except requests.exceptions.HTTPError as error:
        print(f'The server gave an error: {error.response.status_code}')
    except requests.exceptions.InvalidURL:
        print('The index is invalid.')
    except requests.exceptions.RequestException as error:
        print(f'Something else went wrong: {type(error).__name__}')
    return None

dummy_product = {
    "title": "Test Product",
    "price": 500,
    "description": "A good product",
    "image": "https://avatars.githubusercontent.com/u/583231",
    "category": "electronics"
}
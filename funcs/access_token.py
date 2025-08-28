import requests
import keys

from requests.auth import HTTPBasicAuth


# Access Token Generator

def access_token_generator():
    api_url ="https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(api_url, auth=HTTPBasicAuth(keys.consumer_key, keys.consumer_secret))
    json_access_token = r.json()
    generated_access_token = json_access_token['access_token']
    print(generated_access_token)

    return generated_access_token

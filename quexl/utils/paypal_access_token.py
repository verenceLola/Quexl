import base64

import environ
import requests

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)
# reading .env file
environ.Env.read_env()


def paypal_token():
    try:
        client_ID = env.str("PAYPAL_CLIENT_ID", "")
        client_Secret = env.str("PAYPAL_CLIENT_SECRET", "")
        url = "https://api.sandbox.paypal.com/v1/oauth2/token"
        data = {
            "client_id": client_ID,
            "client_secret": client_Secret,
            "grant_type": "client_credentials",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic {0}".format(
                base64.b64encode(
                    (client_ID + ":" + client_Secret).encode()
                ).decode()
            ),
        }

        token = requests.post(url, data, headers=headers)
        return token
    except Exception as e:
        raise (e)

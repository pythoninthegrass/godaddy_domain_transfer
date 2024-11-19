#!/usr/bin/env python

import requests
from decouple import config
from godaddy_domain_transfer import GoDaddyTransferPrep
from textwrap import dedent

API_KEY = config("API_KEY")
API_SECRET = config("API_SECRET")
DOMAIN = config("DOMAIN", default="example.com")
NEW_EMAIL = config("NEW_EMAIL", default=None)


def get_shopper_id(api_key, api_secret):
    headers = {
        "Authorization": f"sso-key {api_key}:{api_secret}",
        "Content-Type": "application/json"
    }
    response = requests.get("https://api.godaddy.com/v1/shoppers/@self", headers=headers)
    if response.status_code == 200:
        return response.json().get("shopperId")
    return None


def main():
    shopper_id = get_shopper_id(API_KEY, API_SECRET)
    prep = GoDaddyTransferPrep(API_KEY, API_SECRET)
    success, message, auth_code = prep.prepare_domain_transfer(
        DOMAIN,
        shopper_id=shopper_id,
        new_email=NEW_EMAIL
    )

    if success:
        print(dedent(f"""\
        Domain ready for transfer!
        Authorization Code: {auth_code}
        Next steps:
        1. Go to your new registrar's transfer page
        2. Enter your domain name and authorization code
        3. Complete payment for transfer
        4. Approve transfer email from GoDaddy when received"""))
    else:
        print(f"Error preparing domain: {message}")


if __name__ == "__main__":
    main()

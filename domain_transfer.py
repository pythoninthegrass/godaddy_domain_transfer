import requests
import time
from typing import Dict, Optional, Tuple
from requests.exceptions import RequestException


class GoDaddyTransferPrep:
    """Prepares domains for transfer away from GoDaddy"""

    def __init__(self, api_key: str, api_secret: str, dev: bool = False):
        self.base_url = "https://api.ote-godaddy.com/v1" if dev else "https://api.godaddy.com/v1"
        self.headers = {
            "Authorization": f"sso-key {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }

    def _make_request(self, method: str, url: str, **kwargs) -> Dict:
        """Make API request with error handling"""
        try:
            response = requests.request(method, url, headers=self.headers, **kwargs)
            if response.status_code == 200:
                return response.json() if response.content else {}
            elif response.status_code == 400:
                raise RequestException(f"Bad request: {response.json().get('message', 'Unknown error')}")
            response.raise_for_status()
            return response.json() if response.content else {}
        except RequestException as e:
            raise RequestException(f"API request failed: {str(e)}")

    def update_email(self, shopper_id: str, new_email: str) -> bool:
        """Update shopper email address"""
        try:
            self._make_request("PATCH", f"{self.base_url}/shoppers/{shopper_id}",
                            json={"email": new_email})
            return True
        except RequestException:
            return False

    def prepare_domain_transfer(
        self, domain: str,
        shopper_id: Optional[str] = None,
        new_email: Optional[str] = None
    ) -> Tuple[bool, str, Optional[str]]:
        """Prepare domain for transfer, optionally updating email"""
        try:
            if shopper_id and new_email:
                if not self.update_email(shopper_id, new_email):
                    return False, "Failed to update email address", None
                time.sleep(5)

            status = self.get_domain_status(domain)

            if status.get("privacy", False):
                self.disable_privacy(domain)
                time.sleep(5)

            if status.get("locked", False):
                self.unlock_domain(domain)
                time.sleep(5)

                new_status = self.get_domain_status(domain)
                if new_status.get("locked", False):
                    return False, "Failed to unlock domain", None

            auth_code = self.get_auth_code(domain)
            if not auth_code:
                return False, "Failed to retrieve authorization code", None

            return True, "Domain ready for transfer", auth_code

        except RequestException as e:
            return False, f"API error: {str(e)}", None

    def get_domain_status(self, domain: str) -> Dict:
        return self._make_request("GET", f"{self.base_url}/domains/{domain}")

    def unlock_domain(self, domain: str) -> None:
        self._make_request("PATCH", f"{self.base_url}/domains/{domain}",
                          json={"locked": False})

    def disable_privacy(self, domain: str) -> None:
        self._make_request("DELETE", f"{self.base_url}/domains/{domain}/privacy")

    def get_auth_code(self, domain: str) -> Optional[str]:
        response = self._make_request("GET", f"{self.base_url}/domains/{domain}")
        return response.get("authCode")

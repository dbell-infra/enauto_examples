import requests
import json
import time

class Meraki:
    def __init__(self, baseurl, api_key, auto_rate_limit=False):
        self.baseurl = baseurl
        self.api_key = api_key
        self.default_org = None
        self.default_network = None
        self.man_rate_limit = None
        self.auto_rate_limit = auto_rate_limit
        self.holddown = 0

    def get(self, endpoint, debug=False):
        headers = {
            'X-Cisco-Meraki-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        if debug:
            print(f"Executing GET request against endpoint: {endpoint} \n  Base URL: {self.baseurl}")
        if self.man_rate_limit:
            if debug:
                print(f"Manual rate limiting configured: Timer is {str(self.man_rate_limit)} ")
            time.sleep(self.man_rate_limit)

        if self.auto_rate_limit:
            time.sleep(self.holddown)

        response = requests.get(headers=headers, url=f"{self.baseurl}/{endpoint}")

        if response.status_code == 429 and self.auto_rate_limit:
            if debug:
                print('Call failed for Too Many Requests, Rate Limiting calls')
            call_failed = True
            while call_failed:
                self.holddown += 5
                if debug:
                    print(f"Current hold down: {str(self.holddown)}")
                time.sleep(self.holddown)
                response = requests.get(headers=headers, url=f"{self.baseurl}/{endpoint}")
                if response.status_code != 429:
                    call_failed = False

        if response.status_code == "200" or "201" and self.auto_rate_limit:
            if self.holddown > 0:
                self.holddown -= 1

        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        return response.json()

    def get_orgs(self,pp=False, debug=False):
        kwargs = {
            "endpoint": "/organizations",
            "debug": debug
        }

        response = self.get(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response

    def get_networks(self, org=None, pp=False, debug=False):
        if self.default_org and not org:
            org = self.default_org
        kwargs = {
            "endpoint": f"/organizations/{org}/networks",
            "debug": debug
        }

        response = self.get(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response

    def get_devices(self, network=None, pp=False, debug=False):
        if self.default_network and not network:
            network = self.default_network

        kwargs = {
            "endpoint": f"/networks/{network}/devices",
            "debug": debug
        }

        response = self.get(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response

    def get_device(self, serial, pp=False, debug=False, urloption=None):


        kwargs = {
            "endpoint": f"/devices/{serial}",
            "debug": debug
        }

        if urloption:
            kwargs['endpoint'] = kwargs["endpoint"] + urloption

        response = self.get(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response
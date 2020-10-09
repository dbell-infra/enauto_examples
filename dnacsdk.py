import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning


class Dnac:
    def __init__(self, username, password, base_url, disable_warnings=False, disable_verification=False):
        self.user = username
        self.password = password
        self.baseurl = base_url
        self.auth_endpoint = "system/api/v1/auth/token"
        self.verify = True
        auth_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if disable_warnings:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        if disable_verification:
            self.verify = False

        auth = requests.post(url=f"{self.baseurl}/{self.auth_endpoint}",
                             auth=(self.user, self.password),
                             verify=False,
                             headers=auth_headers)
        # Attempt to authenticate. If this block of code completes it is safe to assume that
        # authentication was successful
        try:
            token = auth.json()['Token']
            self.isauthenticated = True
            self.headers = {
                'Accept': "application/json",
                "Content-Type": "application/json",
                "x-auth-token": token
            }
            self.auth_resp = True
        # If any exceptions are thrown, set isauthenticated to false and set auth_resp
        # to the reason attribute from the request
        except:
            self.isauthenticated = False
            self.auth_resp = auth.reason

    # Helper method that handles GET requests for all getter methods
    def get(self, endpoint, debug=False):
        if debug:
            print(f"Executing GET request against endpoint: {endpoint} \n  Base URL: {self.baseurl}")
        response = requests.get(url=f"{self.baseurl}/{endpoint}", headers=self.headers,
                                verify=self.verify)
        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        return response.json()

    def post(self, endpoint, payload,debug=False,):
        if debug:
            print(f"Executing GET request against endpoint: {endpoint} \n  Base URL: {self.baseurl}")

        response = requests.post(url=f"{self.baseurl}/{endpoint}", headers=self.headers,
                                verify=self.verify, data=payload)
        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        return response.json()


    def get_sites(self, debug=False, pp=False, id=None):
        kwargs = {
            "endpoint": "intent/api/v1/site",
            "debug": debug
        }

        response = self.get(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response

    def get_network_devices(self, debug=False, pp=False, id=None):
        kwargs = {
            "endpoint": "intent/api/v1/network-device",
            "debug": debug
        }
        # if an ID is supplied as an argument, set the endpoint to
        # network-device/{id}
        if id:
            kwargs['endpoint'] = kwargs['endpoint'] + f'/{id}'
            response = self.get(**kwargs)
        else:
            response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_site_health(self, debug=False, pp=False):
        kwargs = {
            "endpoint": "intent/api/v1/site-health",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_network_health(self, debug=False, pp=False):
        kwargs = {
            "endpoint": "intent/api/v1/network-health",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_client_health(self, debug=False, pp=False):
        kwargs = {
            "endpoint": "intent/api/v1/client-health",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_templates(self, debug=False, pp=False, id=None):
        kwargs = {
            "endpoint": "intent/api/v1/template-programmer/template",
            "debug": debug
        }
        if id:
            kwargs['endpoint'] = kwargs['endpoint'] + f'/{id}'
            response = self.get(**kwargs)
        else:
            response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_template_version(self, id, pp=False, debug=False):
        kwargs = {
            "endpoint": f"intent/api/v1/template-programmer/template/version/{id}",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_command_runner_options(self, debug=False, pp=False):
        kwargs = {
            "endpoint": f"intent/api/v1/network-device-poller/cli/legit-reads",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_topology_site(self, debug=False, pp=False):
        kwargs = {
            "endpoint": f"intent/api/v1/topology/site-topology",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_physical_topology(self, debug=False, pp=False, nodetype="device"):
        kwargs = {
            "endpoint": f"intent/api/v1/topology/physical-topology?nodeType={nodetype}",
            "debug": debug
        }
        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def get_tasks(self, debug=False, pp=False, id=None):
        kwargs = {
            "endpoint": f"intent/api/v1/task",
            "debug": debug
        }
        if id:
            kwargs['endpoint'] = kwargs['endpoint'] + f"/{id}"

        response = self.get(**kwargs)

        if pp:
            return json.dumps(response, indent=2)

        return response

    def create_site(self, site_type, name,  parentname, coord=(None, None), dimensions=(None,None,None), address=None, rfmodel=None, debug=False, pp=False):
        if site_type == "area":
            payload = {
                "type": site_type,
                "site": {
                    site_type: {
                        "name": name,
                        "parentName": parentname
                    }
                }
            }

        if site_type == "building":
            payload = {
                "type": site_type,
                "site": {
                    site_type: {
                        "name": name,
                        "address": address,
                        "parentName": parentname,
                        "latitude": coord[0],
                        "longitude": coord[1]
                    }
                }
            }

        if site_type == "floor":
            payload = {
                "type": site_type,
                "site": {
                    site_type: {
                        "name": name,
                        "address": address,
                        "parentName": parentname,
                        "width": dimensions[0],
                        "length": dimensions[1],
                        "height": dimensions[2],
                        "rfModel": rfmodel
                    }
                }
            }

        kwargs = {
            "endpoint": "intent/api/v1/site",
            "debug": debug,
            "payload": json.dumps(payload)
        }

        response = self.post(**kwargs)

        if pp:
            print(json.dumps(response, indent=2))

        return response






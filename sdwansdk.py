import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time


class Sdwan:
    def __init__(self, user, password, base_url):
        self.user = user
        self.password = password
        self.base_url = base_url
        self.headers = {
            "Accept": 'application/json',
            "ContentType": "application/json"
        }

        login_body = {
            "j_username": user,
            "j_password": password
        }
        self.session = requests.session()
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        self.session.post(f"{self.base_url}/j_security_check", data=login_body, verify=False)
        token_gen = self.session.get(f"{self.base_url}/dataservice/client/token")
        self.token = token_gen.text
        self.session.headers['X-XSRF-TOKEN'] = self.token

    def get_devices(self,pp=None,write=None, dtype=None, hostname=None, debug=None):
        endpoint = '/dataservice/device'
        kwargs = {
            'endpoint': endpoint,
            'pp': pp,
            'write': write,
            'debug': debug
        }

        if hostname:
            response = self.get(**kwargs)
            host_response = [i for i in response if i['host-name'] == hostname]
            return host_response

        if dtype:
            response = self.get(**kwargs)
            data = [i for i in response if i['device-type'] == dtype]
            return data

        response = self.get(**kwargs)

        return response

    def get_users(self, group=None, pp=None, debug=None, write=None):
        endpoint = '/dataservice/admin/user'
        kwargs = {
            "pp": pp,
            "debug": debug,
            "endpoint": endpoint,
            "write": write
        }

        response = self.get(**kwargs)

        if group:
            data = [i for i in response.json()['data'] if group in i['group']]
            return data

        return response

    def create_user(self, group, description, username, password):
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept'] = "application/json"

        payload = {"group":[group],"description": description,"userName": username,"password":password}

        response = self.session.post(url=f"{self.base_url}/dataservice/admin/user",data=json.dumps(payload))

        return response

    def delete_user(self,user):
        response = self.session.delete(url=f"{self.base_url}/dataservice/admin/user/{user}")

        return response

    def get_device_templates(self, pp=None, write=None, name=None, debug=None):
        endpoint = "/dataservice/template/device"
        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug
        }

        if name:
            response = self.get(**kwargs)
            data = [i for i in response if i['templateName'] == name]
            return data

        response = self.get(**kwargs)

        return response

    def attach_device_template(self, device_ids, template_id):
        self.session.headers['Content-Type'] = 'application/json'
        self.session.headers['Accept'] = "application/json"
        # build initial payload and receive response
        init_endpoint = '/dataservice/template/device/config/input'
        payload = {
                  "templateId": template_id,
                  "deviceIds": device_ids,
                  "isEdited": False,
                  "isMasterEdited": False
                }

        init_response = self.session.post(url=f"{self.base_url}{init_endpoint}", data=json.dumps(payload))
        device_resp = init_response.json()['data']
        # make a new call to the attach feature endpoint
        attach_endpoint = 'dataservice/template/device/config/attachfeature'
        # Feed the data section from the /device/config/input call into a new payload for attachment
        attach_payload = {
                          "deviceTemplateList": [
                            {
                              "templateId": template_id,
                              "device": device_resp,
                              "isEdited": False,
                              "isMasterEdited": False
                            }
                          ]
                        }

        # Return the response which contains a UUID for polling
        attach_response = self.session.post(url=f"{self.base_url}/{attach_endpoint}", data=json.dumps(attach_payload))

        return attach_response.json()

    def get_feature_templates(self,pp=None,write=None):
        endpoint = "/dataservice/template/feature"

        kwargs ={
            "pp": pp,
            "write": write,
            "endpoint": endpoint
        }

        response = self.get(**kwargs)

        return response.json()['data']

    def create_device_template(self, payload):
        self.session.headers['Content-Type'] = "application/json"
        self.session.headers['Accept'] = "application/json"
        response = self.session.post(url=f"{self.base_url}/dataservice/template/device/feature/", data=payload)

        return response.json()

    def create_policy_site_list(self,name, entries, pp=None, write=None, debug=None):
        endpoint = '/dataservice/template/policy/list/site'
        payload = {
                "name": name,
                "description": "Desc Not Required",
                "type": "site",
                "listId": None,
                "entries": entries
        }

        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)
        return response

    def create_policy_prefix_list(self, name, type, entries, debug=None, write=None, pp=None):
        endpoint = f'/dataservice/template/policy/list/{type}'
        payload = {
                  "name": name,
                  "description": "Desc Not Required",
                  "type": type,
                  "entries": entries
                }
        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)
        return response

    def create_policy_vpn_list(self, name, vpn_id, debug=None, write=None, pp=None):
        endpoint = '/dataservice/template/policy/list/vpn'
        payload = {
          "name": name,
          "description": "Desc Not Required",
          "type": "vpn",
          "listId": None,
          "entries": [
            {
              "vpn": vpn_id
            }
          ]
        }

        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)
        return response

    def create_policy_network(self, type, vpn_list_id, site_list_id, name, desc, region_name, debug=None, write=None, pp=None):
        endpoint = f"/dataservice/template/policy/definition/{type}"
        payload = {
              "name": name,
              "type": type,
              "description": desc,
              "definition": {
                "vpnList": f"{vpn_list_id}",
                "regions": [
                  {
                    "name": region_name,
                    "siteLists": [
                      f"{site_list_id}"
                    ]
                  }
                ]
              }
            }

        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)

        return response

    def create_policy_definition(self, sequence_list, type, name, description, debug=None, write=None, pp=None):
        endpoint = f"/dataservice/template/policy/definition/{type}"
        payload = {
            "name": name,
            "type": type,
            "description": description,
            "defaultAction": {
                "type": "drop"
            },
            "sequences": sequence_list

        }
        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)
        return response

    def apply_policy_template(self, description, name, policy_def_id, site_list_id, vpn_list_id, net_def_id, debug=None, write=None, pp=None):
        endpoint = '/dataservice/template/policy/vsmart/'
        payload = {
          "policyDescription": description,
          "policyType": "feature",
          "policyName": name,
          "policyDefinition": {
            "assembly": [
              {
                "definitionId": policy_def_id,
                "type": "data",
                "entries": [
                  {
                    "direction": "service",
                    "siteLists": [
                      site_list_id
                    ],
                    "vpnLists": [
                      vpn_list_id
                    ]
                  }
                ]
              },
              {
                "definitionId": net_def_id,
                "type": "mesh"
              }
            ]
          },
          "isPolicyActivated": False
        }
        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug,
            'payload': json.dumps(payload)
        }

        response = self.post(**kwargs)
        return response

    def get_certificates_vedge(self, pp=None, write=None, deviceip=None, debug=None):
        endpoint = f"/dataservice/certificate/vedge/list"
        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}
        if deviceip:
            response = self.get(**args)
            device = [i for i in response if "deviceIP" in i.keys() and i['deviceIP'] == deviceip]
            return device

        response = self.get(**args)

        return response

    def get_sites_bfd(self, pp=None, write=None, detail=None, debug=None):
        endpoint = "/dataservice/device/bfd/sites/summary"
        kwargs = {
            "pp": pp,
            "write": write,
            'endpoint': endpoint,
            'debug': debug
        }

        response = self.get(**kwargs)

        if detail:
            kwargs["endpoint"] = f"/dataservice/device/bfd/sites/detail?state={detail}"

            response = self.get(**kwargs)

        return response

    def get_device_sys_util(self, deviceip, hours='24', pp=None, debug=None, write=None):
        endpoint = '/dataservice/statistics/system/'

        payload = {
              "query": {
                "condition": "AND",
                "rules": [
                  {
                    "value": [
                      hours
                    ],
                    "field": "entry_time",
                    "type": "date",
                    "operator": "last_n_hours"
                  },
                  {
                    "value": [
                      deviceip
                    ],
                    "field": "vdevice_name",
                    "type": "string",
                    "operator": "in"
                  }
                ]
              },
              "fields": [
                "entry_time",
                "count",
                "cpu_user_new",
                "mem_util",
                "mem_used",
                "disk_avail"
              ],
              "sort": [
                {
                  "field": "entry_time",
                  "type": "date",
                  "order": "asc"
                }
              ]
            }

        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug, 'payload': payload}
        response = self.post(**args)

        return response['data']

    def get_device_counters(self, deviceip, pp=None, write=None, debug=None):
        endpoint = f"/dataservice/device/counters?deviceId={deviceip}"
        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}

        return self.get(**args)

    def post(self, endpoint, payload, debug=None, pp=None, write=None):
        self.session.headers['Content-Type'] = "application/json"
        self.session.headers['Accept'] = "application/json"
        if debug:
            print(f"Executing POST against {endpoint}")

        response = self.session.post(url=f"{self.base_url}{endpoint}", data=payload)

        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        if write:
            try:
                with open(f"POST-{str.replace(endpoint,'/','-')}.txt", "w") as file:
                    file.write(json.dumps(response.json(), indent=2))
            except:
                with open(f"POST-{str.replace(endpoint,'/','-')}.txt", "w") as file:
                    file.write(response)

        if pp:
            print(json.dumps(response.json(), indent=2))

        try:
            return response.json()
        except:
            return response.text

    def get(self, endpoint, pp=None, write=None, debug=None):
        if debug:
            print(f"Executing GET against endpoint: {endpoint}")
        response = self.session.get(f"{self.base_url}{endpoint}", headers=self.headers)

        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        if write:
            with open(f"GET-{str.replace(endpoint,'/','-')}.txt", "w") as file:
                file.write(json.dumps(response.json()['data'], indent=2))
        if pp:
            print(json.dumps(response.json()['data'], indent=2))

        return response.json()['data']

    def delete(self, endpoint, pp=None, write=None, debug=None):
        if debug:
            print(f"Executing DELETE against endpoint: {endpoint}")
        response = self.session.delete(f"{self.base_url}{endpoint}", headers=self.headers)

        if debug:
            print(f"  Status: {response.status_code} {response.reason}")

        if pp:
            print(response.text)

        return response.text

    def poll_task(self, uuid, retries=5):
        print(f'Polling {uuid} for status with {retries} retries')

        for i in range(retries):
            response = self.session.get(url=f"{self.base_url}/dataservice/device/action/status/{uuid}")
            result = response.json()['validation']['statusId']
            print(f"Result: {result}")
            if result == 'validation_success':
                break
            time.sleep(5)

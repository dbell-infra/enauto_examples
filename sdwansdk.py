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
        args = {'endpoint': endpoint, 'pp': pp, 'write': write, 'debug': debug}

        # if any of these search parameters need to pretty print the output, we need to collect
        # the response first, then do the search operation, then do json.dumps
        if hostname and not pp:
            response = self.generic_get(**args)
            host_response = [i for i in response if i['host-name'] == hostname]
            return host_response
        if hostname and pp:
            response = self.generic_get(endpoint=endpoint, debug=debug)
            host_response = [i for i in response if i['host-name'] == hostname]
            return json.dumps(host_response, indent=2)

        if dtype and not pp:
            response = self.generic_get(**args)
            data = [i for i in response if i['device-type'] == dtype]
            return data
        if dtype and pp:
            response = self.generic_get(endpoint=endpoint, debug=debug)
            data = [i for i in response if i['device-type'] == dtype]
            return json.dumps(data, indent=2)

        response = self.generic_get(**args)
        # if write is true, write the JSON response body to a text file
        if write:
            with open(f"request-get_devices.txt", "w") as file:
                file.write(response)
        return response

    def get_users(self, group=None, pp=None, debug=None):
        endpoint = '/dataservice/admin/user'
        args = {"pp": pp, "debug": debug, "endpoint": endpoint}
        response = self.generic_get(**args)

        if group and not pp:
            data = [i for i in response.json()['data'] if group in i['group']]
            return data
        if group and pp:
            data = [i for i in response.json()['data'] if group in i['group']]
            return json.dumps(data, indent=2)

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
        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}

        if name and not pp:
            response = self.generic_get(**args)
            data = [i for i in response if i['templateName'] == name]
            return data
        if name and pp:
            response = self.generic_get(endpoint=endpoint, debug=debug)
            data = [i for i in response if i['templateName'] == name]
            return json.dumps(data, indent=2)

        response = self.generic_get(**args)

        if write:
            with open(f"request-get_device_templates.txt", "w") as file:
                file.write(json.dumps(response, indent=2))
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
        response = self.session.get(f"{self.base_url}/dataservice/template/feature", headers=self.headers)
        if write:
            with open(f"request-get_feature_templates.txt", "w") as file:
                file.write(json.dumps(response.json()['data'], indent=2))
        if pp:
            return json.dumps(response.json()['data'], indent=2)
        else:
            return response.json()['data']

    def create_device_template(self, payload):
        self.session.headers['Content-Type'] = "application/json"
        self.session.headers['Accept'] = "application/json"
        response = self.session.post(url=f"{self.base_url}/dataservice/template/device/feature/", data=payload)

        return response.json()

    def create_policy_site_list(self,name, entries):
        endpoint = '/dataservice/template/policy/list/site'
        payload = {
                      "name": name,
                      "description": "Desc Not Required",
                      "type": "site",
                      "listId": None,
                      "entries": entries
                    }
        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def create_policy_prefix_list(self, name, type, entries):
        endpoint = f'/dataservice/template/policy/list/{type}'
        payload = {
                  "name": name,
                  "description": "Desc Not Required",
                  "type": type,
                  "entries": entries
                }

        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def create_policy_vpn_list(self, name, vpn_id):
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

        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def create_policy_network(self, type, vpn_list_id, site_list_id, name, desc, region_name):
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

        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def create_policy_definition(self, sequence_list, type, name, description):
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
        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def apply_policy_template(self, description, name, policy_def_id, site_list_id, vpn_list_id, net_def_id):
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
        response = self.generic_post(endpoint, json.dumps(payload))
        return response

    def get_certificates_vedge(self, pp=None, write=None, deviceip=None, debug=None):
        endpoint = f"/dataservice/certificate/vedge/list"
        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}
        if deviceip and not pp:
            response = self.generic_get(**args)
            device = [i for i in response if "deviceIP" in i.keys() and i['deviceIP'] == deviceip]
            return device

        elif deviceip and pp:
            response = self.generic_get(endpoint=endpoint, debug=debug)
            device = [i for i in response if "deviceIP" in i.keys() and i['deviceIP'] == deviceip]
            return json.dumps(device, indent=2)
        else:
            response = self.generic_get(**args)

        return response

    def get_sites_bfd(self, pp=None, write=None, detail=None, debug=None):
        endpoint = "/dataservice/device/bfd/sites/summary"

        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}
        response = self.generic_get(**args)

        if detail:
            endpoint=f"/dataservice/device/bfd/sites/detail?state={detail}"
            args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}
            response = self.generic_get(**args)

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
        response = self.generic_post(**args)

        if pp:
            return json.dumps(response, indent=2)

        return response['data']

    def get_device_counters(self, deviceip, pp=None, write=None, debug=None):
        endpoint = f"/dataservice/device/counters?deviceId={deviceip}"
        args = {"pp": pp, "write": write, 'endpoint': endpoint, 'debug': debug}

        return self.generic_get(**args)

    def generic_post(self, endpoint, payload, debug=None):
        self.session.headers['Content-Type'] = "application/json"
        self.session.headers['Accept'] = "application/json"
        if debug:
            print(f"Executing POST against {endpoint}")
        response = self.session.post(url=f"{self.base_url}{endpoint}", data=payload)

        try:
            return response.json()
        except:
            return response.text

    def generic_get(self, endpoint, pp=None,write=None, debug=None):
        if debug:
            print(f"Executing GET against endpoint: {endpoint}")
        response = self.session.get(f"{self.base_url}{endpoint}", headers=self.headers)
        if write:
            with open(f"request-generic.txt", "w") as file:
                file.write(json.dumps(response.json()['data'], indent=2))
        if pp:
            return json.dumps(response.json()['data'], indent=2)
        else:
            return response.json()['data']

    def poll_task(self, uuid, retries=5):
        print(f'Polling {uuid} for status with {retries} retries')

        for i in range(retries):
            response = self.session.get(url=f"{self.base_url}/dataservice/device/action/status/{uuid}")
            result = response.json()['validation']['statusId']
            print(f"Result: {result}")
            if result == 'validation_success':
                break
            time.sleep(5)

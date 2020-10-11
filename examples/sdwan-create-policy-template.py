from sdwansdk import Sdwan
import json


# These credentials are for a reservable SD-WAN instance
constructor_config = {
    'user': 'admin',
    'password': 'C1sco12345',
    'base_url': 'https://10.10.20.90:443'
}
sdwan = Sdwan(**constructor_config)

# CREATING A POLICY TEMPLATE

# # Define different object names that comprise the policy
site_list_name = "TEST-site-2"
vpn_list_name = "TEST-vpn"
network_list_name = "TEST-network"
policy_def_name = "TEST-site-policy-definition"
policy_template_name = "TEST-policy-template"

# Define TLOCs for sites used in policy
tloc_1 = '10.10.1.3'
tloc_2 = '10.10.1.15'

# Define a list of sites that use the new VPN created by the policy
sites = [
    {
      "siteId": "1001"
    },
    {
      "siteId": "1002"
    }
  ]

# Define Parameters for create prefix list function
prefix_entry_1 = {
    'entries': [{"ipPrefix": "10.10.21.0/24"}],
    'name': 'test_prefix_list_1',
    'type': 'dataprefix',
    'debug': True,
    "write": True,
    'pp': True
}

prefix_entry_2 = {
    'entries': [{"ipPrefix": "10.10.22.0/24"}],
    'name': 'test_prefix_list_2',
    'type': 'dataprefix',
    'debug': True,
    "write": True,
    'pp': True
}



# Create site list
site_list_uuid = sdwan.create_policy_site_list(name=site_list_name, entries=sites, pp=True, write=True, debug=True)['listId']

print(f"Created site list with ID: {site_list_uuid}")

# Create data prefix lists
prefix_uuid_1 = sdwan.create_policy_prefix_list(**prefix_entry_1)['listId']
print(f"Created data prefix list with ID: {prefix_uuid_1}")

prefix_uuid_2 = sdwan.create_policy_prefix_list(**prefix_entry_2)['listId']
print(f"Created data prefix list with ID: {prefix_uuid_2}")

# Create VPN list
vpn_UUID = sdwan.create_policy_vpn_list(name=vpn_list_name,vpn_id='200', debug=True, write=True, pp=True)['listId']
print(f"Created VPN list with ID: {vpn_UUID}")

# Define Parameters for create policy network function
network = {
    "name": network_list_name,
    'vpn_list_id': vpn_UUID,
    'site_list_id': site_list_uuid,
    'desc': 'a test network',
    'region_name': 'test region',
    'type': 'mesh',
    'debug': True,
    "write": True,
    'pp': True
}
# Create Network
network_UUID = sdwan.create_policy_network(**network)['definitionId']
print(f"Created network with ID: {network_UUID} ")

# Define Policy Sequences
seq_1 = {
      "sequenceId": 1,
      "sequenceName": "Traffic Engineering",
      "baseAction": "accept",
      "sequenceType": "trafficEngineering",
      "sequenceIpType": "ipv4",
      "match": {
        "entries": [
          {
            "field": "sourceDataPrefixList",
            "ref": f"{prefix_uuid_1}"
          },
          {
            "field": "destinationDataPrefixList",
            "ref": f"{prefix_uuid_2}"
          }
        ]
      },
      "actions": [
        {
          "type": "set",
          "parameter": [
            {
              "field": "vpn",
              "value": "100"
            },
            {
              "field": "tloc",
              "value": {
                "ip": f"{tloc_2}",
                "color": "mpls",
                "encap": "ipsec"
              }
            }
          ]
        }
      ]
    }

seq_5 = {
      "sequenceId": 5,
      "sequenceName": "Traffic Engineering",
      "baseAction": "accept",
      "sequenceType": "trafficEngineering",
      "sequenceIpType": "ipv4",
      "match": {
        "entries": [
          {
            "field": "sourceDataPrefixList",
            "ref": f"{prefix_uuid_1}"
          },
          {
            "field": "destinationDataPrefixList",
            "ref": f"{prefix_uuid_2}"
          }
        ]
      },
      "actions": [
        {
          "type": "set",
          "parameter": [
            {
              "field": "vpn",
              "value": "100"
            },
            {
              "field": "tloc",
              "value": {
                "ip": f"{tloc_2}",
                "color": "public-internet",
                "encap": "ipsec"
              }
            }
          ]
        }
      ]
    }
seq_10 = {
      "sequenceId": 10,
      "sequenceName": "Traffic Engineering",
      "baseAction": "accept",
      "sequenceType": "trafficEngineering",
      "sequenceIpType": "ipv4",
      "match": {
        "entries": [
          {
            "field": "sourceDataPrefixList",
            "ref": f"{prefix_uuid_2}"
          },
          {
            "field": "destinationDataPrefixList",
            "ref": f"{prefix_uuid_1}"
          }
        ]
      },
      "actions": [
        {
          "type": "set",
          "parameter": [
            {
              "field": "vpn",
              "value": "100"
            },
            {
              "field": "tloc",
              "value": {
                "ip": f"{tloc_1}",
                "color": "mpls",
                "encap": "ipsec"
              }
            }
          ]
        }
      ]
    }

seq_15 = {
      "sequenceId": 15,
      "sequenceName": "Traffic Engineering",
      "baseAction": "accept",
      "sequenceType": "trafficEngineering",
      "sequenceIpType": "ipv4",
      "match": {
        "entries": [
          {
            "field": "sourceDataPrefixList",
            "ref": f"{prefix_uuid_2}"
          },
          {
            "field": "destinationDataPrefixList",
            "ref": f"{prefix_uuid_1}"
          }
        ]
      },
      "actions": [
        {
          "type": "set",
          "parameter": [
            {
              "field": "vpn",
              "value": "100"
            },
            {
              "field": "tloc",
              "value": {
                "ip": f"{tloc_1}",
                "color": "public-internet",
                "encap": "ipsec"
              }
            }
          ]
        }
      ]
    }
# Collect Sequences as a List
seq_list = [seq_1, seq_5, seq_10, seq_15]

# Define parameters to create policy definition
policy_def = {
    'sequence_list': seq_list,
    'type': 'data',
    'name': policy_def_name,
    'description': 'a new test policy',
    'debug': True,
    "write": True,
    'pp': True
}
# Create policy definition
policy_UUID = sdwan.create_policy_definition(**policy_def)['definitionId']
print(f"Defined policy with ID: {policy_UUID} ")

resp = input("Would you like to apply policy? y/n \n")

if resp == "y":
    # Define parameters for apply template function
    apply_temp = {
        'description': "A Test policy that has been created by API",
        'name': policy_template_name,
        'policy_def_id': policy_UUID,
        'site_list_id': site_list_uuid,
        'vpn_list_id': vpn_UUID,
        'net_def_id': network_UUID,
        'debug': True,
        "write": True,
        'pp': True
    }
    # Apply Template
    sdwan.apply_policy_template(**apply_temp)
    print('Template Application Successful')

    resp = input("Would you like to activate policy? y/n \n")
    if resp == "y":

        # Look in the list of templates to find the newly created template name
        # extract the template ID from the newly created template
        search_response = sdwan.get(endpoint='/dataservice/template/policy/vsmart')
        for item in search_response:
            if item["policyName"] == policy_template_name:
                activate_id = item["policyId"]
        # Activate template and collect the poll ID
        poll_id = sdwan.post(f'/dataservice/template/policy/vsmart/activate/{activate_id}?confirm=true',payload=json.dumps({}))['id']
        print("Activating Template")
        # Poll task endpoint for completion status
        sdwan.poll_task(poll_id)

resp = input("Would you like to roll back? y/n")

if resp == "y":

    # Roll back policy creation
    print("ROLLING BACK CHANGE")
    # Delete data definition
    delete_policy_definition_data_arg = {
        'endpoint': f'/dataservice/template/policy/definition/data/{policy_UUID}',
        'pp': True,
        'debug': True
    }

    sdwan.delete(**delete_policy_definition_data_arg)
    # delete network (mesh) definition
    delete_network_policy_definition_arg = {
        'endpoint': f'/dataservice/template/policy/definition/mesh/{network_UUID}',
        'pp': True,
        'debug': True
    }
    sdwan.delete(**delete_network_policy_definition_arg)
    # Delete VPN list
    delete_policy_list_vpn_arg = {
        'endpoint': f'/dataservice/template/policy/list/vpn/{vpn_UUID}',
        'pp': True,
        'debug': True
    }

    sdwan.delete(**delete_policy_list_vpn_arg)
    # Delete Site list
    delete_policy_list_site_arg = {
        'endpoint': f'/dataservice/template/policy/list/site/{site_list_uuid}',
        'pp': True,
        'debug': True
    }

    sdwan.delete(**delete_policy_list_site_arg)
    # Delete prefix lists
    delete_policy_list_prefix1_arg = {
        'endpoint': f'/dataservice/template/policy/list/dataprefix/{prefix_uuid_1}',
        'pp': True,
        'debug': True
    }

    sdwan.delete(**delete_policy_list_prefix1_arg)

    delete_policy_list_prefix2_arg = {
        'endpoint': f'/dataservice/template/policy/list/dataprefix/{prefix_uuid_2}',
        'pp': True,
        'debug': True
    }

    sdwan.delete(**delete_policy_list_prefix2_arg)

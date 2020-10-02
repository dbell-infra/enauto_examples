from sdwansdk import Sdwan


# These credentials are for a reservable SD-WAN instance
constructor_config = {
    'user': 'admin',
    'password': 'C1sco12345',
    'base_url': 'https://10.10.20.90:443'
}
sdwan = Sdwan(**constructor_config)

# This code will change configurations, uncomment to run

# ATTACHING A DEVICE TEMPLATE

# # Get the target device ID by name
# device_id = test.get_devices(hostname='site3-vedge01')[0]['uuid']
# # Get the target template ID by name
# template_id = test.get_device_templates(name='cloned-temp')[0]['templateId']
# # Collect the UUID from the POST requests for template attachment
# poll_id = test.attach_device_template(device_ids=[device_id], template_id=template_id)['id']
# # Poll UUID for event completion
# test.poll_task(uuid=poll_id)

# CREATING A POLICY TEMPLATE

# # Define different object names that comprise the policy
# site_list_name = "TEST-site"
# vpn_list_name = "TEST-vpn"
# network_list_name = "TEST-network"
# policy_def_name = "TEST-site-policy-definition"
# policy_template_name = "TEST-policy-template"
#
# # Define TLOCs for sites used in policy
# tloc_1 = '10.10.1.3'
# tloc_2 = '10.10.1.15'
#
# # Define a list of sites that use the new VPN created by the policy
# sites = [
#     {
#       "siteId": "1001"
#     },
#     {
#       "siteId": "1002"
#     }
#   ]
#
# # Define Parameters for create prefix list function
# prefix_entry_1 = {
#     'entries': [{"ipPrefix": "10.10.21.0/24"}],
#     'name': 'test_prefix_list_1',
#     'type': 'dataprefix',
# }
#
# prefix_entry_2 = {
#     'entries': [{"ipPrefix": "10.10.22.0/24"}],
#     'name': 'test_prefix_list_2',
#     'type': 'dataprefix',
# }
#
#
# # Create site list
# site_list_uuid = test.create_policy_site_list(name=site_list_name, entries=sites)['listId']
#
# print(f"Created site list with ID: {site_list_uuid}")
#
# # Create data prefix lists
# prefix_uuid_1 = test.create_policy_prefix_list(**prefix_entry_1)['listId']
# print(f"Created data prefix list with ID: {prefix_uuid_1}")
#
# prefix_uuid_2 = test.create_policy_prefix_list(**prefix_entry_2)['listId']
# print(f"Created data prefix list with ID: {prefix_uuid_2}")
#
# # Create VPN list
# vpn_UUID = test.create_policy_vpn_list(name=vpn_list_name,vpn_id='200')['listId']
# print(f"Created VPN list with ID: {vpn_UUID}")
#
# # Define Parameters for create policy network function
# network = {
#     "name": network_list_name,
#     'vpn_list_id': vpn_UUID,
#     'site_list_id': site_list_uuid,
#     'desc': 'a test network',
#     'region_name': 'test region',
#     'type': 'mesh'
# }
# # Create Network
# network_UUID = test.create_policy_network(**network)['definitionId']
# print(f"Created network with ID: {network_UUID} ")
#
# # Define Policy Sequences
# seq_1 = {
#       "sequenceId": 1,
#       "sequenceName": "Traffic Engineering",
#       "baseAction": "accept",
#       "sequenceType": "trafficEngineering",
#       "sequenceIpType": "ipv4",
#       "match": {
#         "entries": [
#           {
#             "field": "sourceDataPrefixList",
#             "ref": f"{prefix_uuid_1}"
#           },
#           {
#             "field": "destinationDataPrefixList",
#             "ref": f"{prefix_uuid_2}"
#           }
#         ]
#       },
#       "actions": [
#         {
#           "type": "set",
#           "parameter": [
#             {
#               "field": "vpn",
#               "value": "100"
#             },
#             {
#               "field": "tloc",
#               "value": {
#                 "ip": f"{tloc_2}",
#                 "color": "mpls",
#                 "encap": "ipsec"
#               }
#             }
#           ]
#         }
#       ]
#     }
#
# seq_5 = {
#       "sequenceId": 5,
#       "sequenceName": "Traffic Engineering",
#       "baseAction": "accept",
#       "sequenceType": "trafficEngineering",
#       "sequenceIpType": "ipv4",
#       "match": {
#         "entries": [
#           {
#             "field": "sourceDataPrefixList",
#             "ref": f"{prefix_uuid_1}"
#           },
#           {
#             "field": "destinationDataPrefixList",
#             "ref": f"{prefix_uuid_2}"
#           }
#         ]
#       },
#       "actions": [
#         {
#           "type": "set",
#           "parameter": [
#             {
#               "field": "vpn",
#               "value": "100"
#             },
#             {
#               "field": "tloc",
#               "value": {
#                 "ip": f"{tloc_2}",
#                 "color": "public-internet",
#                 "encap": "ipsec"
#               }
#             }
#           ]
#         }
#       ]
#     }
# seq_10 = {
#       "sequenceId": 10,
#       "sequenceName": "Traffic Engineering",
#       "baseAction": "accept",
#       "sequenceType": "trafficEngineering",
#       "sequenceIpType": "ipv4",
#       "match": {
#         "entries": [
#           {
#             "field": "sourceDataPrefixList",
#             "ref": f"{prefix_uuid_2}"
#           },
#           {
#             "field": "destinationDataPrefixList",
#             "ref": f"{prefix_uuid_1}"
#           }
#         ]
#       },
#       "actions": [
#         {
#           "type": "set",
#           "parameter": [
#             {
#               "field": "vpn",
#               "value": "100"
#             },
#             {
#               "field": "tloc",
#               "value": {
#                 "ip": f"{tloc_1}",
#                 "color": "mpls",
#                 "encap": "ipsec"
#               }
#             }
#           ]
#         }
#       ]
#     }
#
# seq_15 = {
#       "sequenceId": 15,
#       "sequenceName": "Traffic Engineering",
#       "baseAction": "accept",
#       "sequenceType": "trafficEngineering",
#       "sequenceIpType": "ipv4",
#       "match": {
#         "entries": [
#           {
#             "field": "sourceDataPrefixList",
#             "ref": f"{prefix_uuid_2}"
#           },
#           {
#             "field": "destinationDataPrefixList",
#             "ref": f"{prefix_uuid_1}"
#           }
#         ]
#       },
#       "actions": [
#         {
#           "type": "set",
#           "parameter": [
#             {
#               "field": "vpn",
#               "value": "100"
#             },
#             {
#               "field": "tloc",
#               "value": {
#                 "ip": f"{tloc_1}",
#                 "color": "public-internet",
#                 "encap": "ipsec"
#               }
#             }
#           ]
#         }
#       ]
#     }
# # Collect Sequences as a List
# seq_list = [seq_1, seq_5, seq_10, seq_15]
#
# # Define parameters to create policy definition
# policy_def = {
#     'sequence_list': seq_list,
#     'type': 'data',
#     'name': policy_def_name,
#     'description': 'a new test policy'
# }
# # Create policy definition
# policy_UUID = test.create_policy_definition(**policy_def)['definitionId']
# print(f"Defined policy with ID: {policy_UUID} ")
#
# # Define parameters for apply template function
# apply_temp = {
#     'description': "A Test policy that has been created by API",
#     'name': policy_template_name,
#     'policy_def_id': policy_UUID,
#     'site_list_id': site_list_uuid,
#     'vpn_list_id': vpn_UUID,
#     'net_def_id': network_UUID
#
# }
# # Apply Template
# test.apply_policy_template(**apply_temp)
# print('Template Application Successful')
#
# # Look in the list of templates to find the newly created template name
# # extract the template ID from the newly created template
# search_response = test.generic_get(endpoint='/dataservice/template/policy/vsmart')
# for item in search_response:
#     if item["policyName"] == policy_template_name:
#         activate_id = item["policyId"]
# # Activate template and collect the poll ID
# poll_id = test.generic_post(f'/dataservice/template/policy/vsmart/activate/{activate_id}?confirm=true',payload=json.dumps({}))['id']
# print("Activating Template")
#
# # Poll task endpoint for completion status
# test.poll_task(poll_id)

#SD-WAN GETTER Methods
print('*' * 25)
counter_resp = sdwan.get_device_counters(deviceip='10.10.1.13', pp=True, debug=True)
print(counter_resp)
print('*' * 25)
bfd_sites_resp = sdwan.get_sites_bfd(debug=True, pp=True)
print(bfd_sites_resp)
print('*' * 25)
vedge_cert_resp = sdwan.get_certificates_vedge(debug=True, pp=True, deviceip='10.10.1.13')
print(vedge_cert_resp)
print('*' * 25)
template_resp = sdwan.get_device_templates(debug=True, pp=True, name='vSmart_Template')
print(template_resp)
print('*' * 25)
user_resp = sdwan.get_users(debug=True, pp=True, )
print(user_resp)
print('*' * 25)
dev_resp = sdwan.get_devices(pp=True, hostname='dc-cedge01', debug=True)
print(dev_resp)
print('*' * 25)
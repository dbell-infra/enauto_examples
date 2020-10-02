from dnacsdk import Dnac

# DNA always on sandbox credentials
dnac_conf = {
    "username": "devnetuser",
    "password": "Cisco123!",
    "base_url": "https://sandboxdnac.cisco.com/dna",
    "disable_warnings": True,
    "disable_verification": True
}

dnac = Dnac(**dnac_conf)

# debug option prints the base url and endpoint used in the API call to console before executing request,
# it then collects the HTTP status and reason after request has completed and prints that to console
# pp option pretty prints API response with json.dumps(), this returns a string
# calling without pp will return the original JSON body that can be manipulated with Python

# Uncomment print loop at the bottom of the example to print all calls to console

# GETTING SITE AND FABRIC DATA

# # Request DNAC sites
site_req = dnac.get_sites(debug=True, pp=True)
#
# # Request DNAC site - topology
topology_site_req = dnac.get_topology_site(debug=True, pp=True)


# Request DNAC network devices
network_device_req = dnac.get_network_devices(debug=True, pp=True)

# # Request physical topology. Takes nodetype argument that defaults to "device"
physical_topology_req = dnac.get_physical_topology(debug=True, pp=True)

# Request network device by ID
network_dev_req_by_id = dnac.get_network_devices(debug=True, id="3e48558a-237a-4bca-8823-0580b88c6acf", pp=True)

# ASSURANCE APIS

# Request Site Health
site_health_req = dnac.get_site_health(debug=True, pp=True)

# Request Network Health
network_health_req = dnac.get_network_health(debug=True, pp=True)

# Request Client Health
client_health_req = dnac.get_client_health(debug=True, pp=True)

# TEMPLATE API

# Request Templates
device_template_req = dnac.get_templates(debug=True, pp=True)

# Request template by ID
device_template_by_id_req = dnac.get_templates(debug=True, pp=True, id='07230920-7bca-4f29-a02a-25f1476bc8a1')

# Request versions of a particular template (use parent template id value for id arg)
device_template_version_req = dnac.get_template_version(debug=True, pp=True, id='a7e0362d-677a-41cc-8ec9-7721141832ca')

# COMMAND RUNNER API

# Request commands available for command runner API
command_runner_req = dnac.get_command_runner_options(debug=True, pp=True)

# Task API

# Get list of tasks, or single task by if optional ID param is supplied.
task_req = dnac.get_tasks(debug=True, pp=True, id="f8ed577d-5713-48f6-927b-ce61f3ee975d")

get_request_collection = [
    site_req,
    topology_site_req,
    network_device_req,
    physical_topology_req,
    network_dev_req_by_id,
    site_health_req,
    network_health_req,
    client_health_req,
    device_template_req,
    device_template_by_id_req,
    device_template_version_req,
    command_runner_req,
    task_req,
]

for request in get_request_collection:
    print(request)
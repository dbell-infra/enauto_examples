from merakisdk import Meraki


constructor = {
    'baseurl': 'https://api.meraki.com/api/v1',
    'api_key': '6bec40cf957de430a6f1f2baa056b99a4fac9ea0',
    # auto rate limiting uses a hold down timer and will loop over a failed call incrementing
    # the hold down timer by 5 seconds until it retrieves a status code other than 429.
    # for every subsequent successful call, the hold down timer will decrement by 1 until it reaches 0
    'auto_rate_limit': True
}

meraki = Meraki(**constructor)

# Get a list of organizations that the auth token is permitted to access
orgs = meraki.get_orgs(debug=True)
# From this list of organizations, select a list entry and extract the id
meraki.default_org = orgs[2]['id']
# The organization id can be added as the default org to make calls without
# supplying the org ID. A different id can be used by supplying as a kwarg
networks = meraki.get_networks(debug=True)
# The network id can be added as the default org to make calls without
# supplying the network ID. A different id can be used by supplying as a kwarg
meraki.default_network = networks[0]["id"]
# With the default org and default network defined, we can make a request to the
# the device endpoint without any additional configuration
# Manual rate limiting can be added that sleeps each call for a predefined amount of time
meraki.man_rate_limit = 5
device_serial = meraki.get_devices(debug=True)[2]["serial"]
# A devices serial number was extracted from the previous call, it can be used for
# a call to get device specific information
meraki.man_rate_limit = None
meraki.get_device(serial=device_serial, debug=True, pp=True)
# the url can be optionally extended for platform specific calls
meraki.get_device(serial=device_serial, urloption='/switch/ports', debug=True, pp=True)






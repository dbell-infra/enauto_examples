from sdwansdk import Sdwan


# These credentials are for a reservable SD-WAN instance
constructor_config = {
    'user': 'admin',
    'password': 'C1sco12345',
    'base_url': 'https://10.10.20.90:443'
}
sdwan = Sdwan(**constructor_config)

# SD-WAN GETTER Methods

print('*' * 25)
counter_resp = sdwan.get_device_counters(deviceip='10.10.1.13', pp=True, debug=True, write=True)
print('*' * 25)
bfd_sites_resp = sdwan.get_sites_bfd(debug=True, pp=True, write=True)
print('*' * 25)
vedge_cert_resp = sdwan.get_certificates_vedge(debug=True, pp=True, deviceip='10.10.1.13', write=True)
print('*' * 25)
template_resp = sdwan.get_device_templates(debug=True, pp=True, name='vSmart_Template', write=True)
print('*' * 25)
user_resp = sdwan.get_users(debug=True, pp=True, write=True )
print('*' * 25)
dev_resp = sdwan.get_devices(pp=True, hostname='dc-cedge01', debug=True, write=True)
print('*' * 25)
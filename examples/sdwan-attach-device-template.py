from sdwansdk import Sdwan
constructor_config = {
    'user': 'admin',
    'password': 'C1sco12345',
    'base_url': 'https://10.10.20.90:443'
}
sdwan = Sdwan(**constructor_config)

# ATTACHING A DEVICE TEMPLATE

# Get the target device ID by name
device_id = sdwan.get_devices(hostname='site3-vedge01')[0]['uuid']
# Get the target template ID by name
template_id = sdwan.get_device_templates(name='cloned-temp')[0]['templateId']
# Collect the UUID from the POST requests for template attachment
poll_id = sdwan.attach_device_template(device_ids=[device_id], template_id=template_id)['id']
# Poll UUID for event completion
sdwan.poll_task(uuid=poll_id)

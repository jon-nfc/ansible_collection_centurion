import json

from ansible.module_utils.common.text.converters import to_text
from ansible.module_utils.urls import open_url
from ansible.plugins.inventory import BaseInventoryPlugin


DOCUMENTATION = '''
---
module: centurion
plugin_type: inventory
short_description: Centurion ERP Inventory
description:
    - "An Inventory Plugin to fetch inventory from Centurion ERP."
options:
    plugin:
        description: token that ensures this is a source file for the 'centurion' plugin.
        required: True
        choices: ['nofusscomputing.centurion.centurion']
    api_endpoint:
        description: Endpoint of the Centurion API
        required: true
        env:
            - name: CENTURION_API
    token:
        required: false
        description:
            - NetBox API token to be able to read against NetBox.
        env:
            - name: CENTURION_TOKEN
    validate_certs:
        description:
            - Allows skipping of validation of SSL certificates. Set to C(false) to disable certificate validation.
        default: true
        type: boolean
author:
    - jon @jon_nfc
'''



class InventoryModule(BaseInventoryPlugin):

    NAME = 'nofusscomputing.centurion.centurion'


    def __init__(self):
        super().__init__()

        self.headers = {
            'Authorization': 'Token 7d501c956363e60df0cfd770db36f54226f079d707346f776ab31d5f40d16542'
        }


    def verify_file(self, path):

        return True


    def fetch_devices(self) -> dict:

        self.display.v("Fetching Devices ")

        response = open_url(
            url = 'https://test.nofusscomputing.com/api/device/',
            headers = self.headers,
            validate_certs=False,
        )

        devices = json.loads(to_text(response.read()))['results']


        return devices


    def fetch_device_config(self, url: str) -> dict:


        self.display.vv(f"Fetching Device Config {url} ")

        response = open_url(
            url = url,
            headers = self.headers,
            validate_certs=False,
        )

        config = json.loads(to_text(response.read()))

        return config


    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        devices = self.fetch_devices()

        self.display.v(f"Parsing returned devices")

        for device in devices:


            self.display.vv(f"Adding device {device['name']} to inventory")


            self.inventory.add_host(host=device['name'])

            config = self.fetch_device_config(device['config'])

            for key, val in config.items():

                self.inventory.set_variable(device['name'], key, val)

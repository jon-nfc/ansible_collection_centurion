import json

from ansible.inventory.group import to_safe_group_name
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
    organization_groups:
        description:
            - Create groups from organization names. Uses format C(organization_<organization.name>).
        default: true
        type: boolean
    token:
        required: false
        description:
            - Centurion API token to be able to read against Centurion.
        env:
            - name: CENTURION_TOKEN
    validate_certs:
        description:
            - Allows skipping of validation of SSL certificates. Set to C(false) to disable certificate validation.
        default: true
        type: boolean
        env:
            - name: VALIDATE_CENTURION_CERTS
author:
    - jon @jon_nfc
'''



EXAMPLES = """
# inventory.yml file in YAML format

plugin: nofusscomputing.centurion.centurion

api_endpoint: http://localhost:8000
token: <token value here>
validate_certs: false

organization_groups: true

# Example Ansible Tower credential Input Configuration:

fields:
  - id: CENTURION_API
    type: string
    label: Centurion Host URL
  - id: CENTURION_TOKEN
    type: string
    label: Centurion API Token
    secret: true
  - id: VALIDATE_CENTURION_CERTS
    label: Validate Centurion SSL Certificate
    type: boolean
required:
  - CENTURION_API
  - CENTURION_TOKEN

# Example Ansible Tower credential Injector Configuration:

env:
  CENTURION_API: '{{ CENTURION_API }}'
  CENTURION_TOKEN: '{{ CENTURION_TOKEN }}'
  VALIDATE_CENTURION_CERTS: '{{ VALIDATE_CENTURION_CERTS | default(true) }}'

"""



class InventoryModule(BaseInventoryPlugin):

    NAME = 'nofusscomputing.centurion.centurion'


    def verify_file(self, path):

        return True


    def fetch_devices(self) -> dict:

        self.display.v("Fetching Devices ")

        response = open_url(
            url = f'{self.api_endpoint}/api/device/',
            headers = self.headers,
            validate_certs = self.validate_certs,
        )

        devices = json.loads(to_text(response.read()))['results']


        return devices


    def fetch_device_config(self, url: str) -> dict:


        self.display.vv(f"Fetching Device Config {url} ")

        response = open_url(
            url = url,
            headers = self.headers,
            validate_certs = self.validate_certs,
        )

        config = json.loads(to_text(response.read()))

        return config


    def fetch_groups(self) -> dict:

        self.display.v("Fetching groups")

        response = open_url(
            url = f'{self.api_endpoint}/api/configuration/',
            headers = self.headers,
            validate_certs = self.validate_certs,
        )

        configuration = json.loads(to_text(response.read()))['results']


        return configuration


    def parse(self, inventory, loader, path, cache=True):
        super().parse(inventory, loader, path)

        self._read_config_data(path=path)


        self.api_endpoint = self.get_option("api_endpoint").strip("/")
        self.token = self.get_option("token")
        self.validate_certs = self.get_option("validate_certs")
        self.organization_groups = self.get_option("organization_groups")

        self.headers = {
            'Authorization': f'Token {self.token}'
        }

        devices = self.fetch_devices()

        self.display.v(f"Parsing returned devices")

        for device in devices:


            self.display.vv(f"Adding device {device['name']} to inventory")


            self.inventory.add_host(host=device['name'])

            if len(device['groups']):

                for group in device['groups']:

                    group_name = to_safe_group_name(
                        name = str(group['name']).lower(),
                        replacer = '_',
                        force = True,
                    )

                    self.inventory.add_group(
                        group = group_name
                    )

                    self.inventory.add_host(
                        host = device['name'],
                        group = group_name,
                    )

            if self.organization_groups:

                organization_group_name = to_safe_group_name(
                    name = 'organization_' + str(device['organization']['name']).lower(),
                    replacer = '_',
                    force = True,
                )

                self.inventory.add_group(
                    group = organization_group_name
                )

                self.inventory.add_host(
                    host = device['name'],
                    group = organization_group_name,
                )

            # see #5
            # config = self.fetch_device_config(device['config'])

            # for key, val in config.items():

            #     self.inventory.set_variable(device['name'], key, val)


        groups = self.fetch_groups()

        self.display.v(f"Parsing returned groups")

        for group in groups:

            self.display.vv(f"Adding group {group['name']} to inventory")

            group_name = to_safe_group_name(
                name = str(group['name']).lower(),
                replacer = '_',
                force = True,
            )

            self.inventory.add_group(
                group = group_name
            )

            if group['parent']:

                self.display.vv(f"Adding group {group['name']} to parent group {group['parent']['name']}")

                parent_group_name = to_safe_group_name(
                    name = str(group['parent']['name']).lower(),
                    replacer = '_',
                    force = True,
                )

                self.inventory.add_child(
                    parent_group_name,
                    group_name,
                )

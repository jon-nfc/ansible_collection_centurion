---
title: Inventory
description: Ansible Playbook to inventroy devices and publish to Centurion ERP
date: 2024-08-19
template: project.html
about: https://github.com/nofusscomputing/ansible_collection_centurion
---

The inventory playbook has been created to inventory devices and to publish the collected inventory to Centurion ERP. The inventory includes details of all software packages installed on the host machine as well as some details regarding the host machine such as UUID and serial number.

The inventory playbook includes the [AWX Feature](../../../playbooks/awx.md) to import the playbook as a job template in AWX / Ansible Automation Platform.

The following job template will be created:

- **Centurion/ITAM/Inventory** Inventory host machines and publish to Centurion ERP

On import to AWX / Ansible Automation Platform a credential type will also be created, 'Collection/No Fuss Computing/Centurion/API' that can be used to supply the required secrets and Centurion host.


!!! warning
    The inventory playbook currently has an issue relating to gathering software starting with L. This issue has been reported and is being worked on [github issue 19](https://github.com/nofusscomputing/ansible_collection_centurion/issues/19)


## Play workflow

The inventory playbook conducts the follwoing tasks:

- Gathers host information

- Gathers sofware information

- Uploads the inventory report to Centurion ERP

- Cleans any leftover files used to create the reports

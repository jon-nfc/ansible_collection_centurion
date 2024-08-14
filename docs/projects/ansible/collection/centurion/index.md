---
title: Centurion
description: No Fuss Computings Companion Ansible Collection Centurion for Centurion ERP.
date: 2024-07-30
template: project.html
about: https://gitlab.com/nofusscomputing/projects/ansible/collections/kubernetes
---

<span style="text-align: center;">

![Project Status - Active](https://img.shields.io/badge/Project%20Status-Active-green?logo=github&style=plastic) 


![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/nofusscomputing/ansible_collection_centurion/ci.yaml?branch=master&style=plastic&logo=github&label=Build&color=%23000) ![GitHub Release](https://img.shields.io/github/v/release/nofusscomputing/ansible_collection_centurion?sort=date&style=plastic&logo=github&label=Release&color=000) 

[![Downloads](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv3%2Fplugin%2Fansible%2Fcontent%2Fpublished%2Fcollections%2Findex%2Fnofusscomputing%2Fcenturion%2F&query=%24.download_count&style=plastic&logo=ansible&logoColor=white&label=Galaxy%20Downloads&labelColor=black&color=cyan)](https://galaxy.ansible.com/ui/repo/published/nofusscomputing/centurion/)



</span>

This Ansible Collection is intended to compliement [Centurion ERP](../../../centurion_erp/index.md).


## Features

- [Inventory plugin](./plugins/inventory.md)


## Ansible Automation Platform / AWX

This collection can be directly added to AAP/AWX. To do so conduct the following:

1. Add the collection as a Project

    `Projects -> Add`

    - name: _Collection/No Fuss Computing/Centurion_

    - Source Control Type: _Git_

    - Source Control URL: _https://gitlab.com/nofusscomputing/projects/ansible/collections/centurion_erp_collection.git_

    - Source Control Branch/Tag/Commit: _set to a branch, tag or commit_

    - `Save`

1. Add a Credential type for the invneotries use

    `Credential Types -> Add`

    - name: _Collection/No Fuss Computing/Centurion_

    - Input configuration:

    ``` yaml

    fields:
        - id: CENTURION_API
            type: string
            label: Centurion Host URL
        - id: CENTURION_TOKEN
            type: string
            label: Centurion API Token
            secret: true
        - id: VALIDATE_CENTURION_CERTS
            type: boolean
            label: Validate Centurion SSL Certificate
        required:
        - CENTURION_API
        - CENTURION_TOKEN

    ```

    - Injector configuration:

    ``` yaml

    env:
        CENTURION_API: '{{ CENTURION_API }}'
        CENTURION_TOKEN: '{{ CENTURION_TOKEN }}'
        VALIDATE_CENTURION_CERTS: '{{ VALIDATE_CENTURION_CERTS | default(true) }}'

    ```

1. Create a Credential

    `Credentials -> Add`

    - name: _Centurion_

    - Credential Type: _Collection/No Fuss Computing/Centurion_

1. Add an inventory

    `Inventoryies -> Add` and complete the fields

    - name: _Centurion_

    - `Save`

1. Add a source to the inventory

    `Inventoryies -> <Centurion Inventory> -> Sources -> Add`

    - name: _Centurion ERP_

    - Source: _Sourced from Project_

    - Credential: _Centurion_
    
    - Project: _Collection/No Fuss Computing/Centurion_

    - Inventory File: _inventory/inventory.yaml_

    - `Save`

1. a

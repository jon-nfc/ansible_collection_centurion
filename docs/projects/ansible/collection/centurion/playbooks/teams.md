---
title: Teams
description: Ansible Playbook for Creating and patching of Centurion ERP teams, including permissions.
date: 2024-08-18
template: project.html
about: https://github.com/nofusscomputing/ansible_collection_centurion
---

The teams playbook has been created for the purpose of creating Centurion ERP teams. It allows teams to be defined as configuration as code which allows standardisation of teams and permissions within an organisation. With this playbook it is possible to create every team within an organisation and define the permissions and notes that are to be applied to that team.

The teams playbook includes the [AWX Feature](../../../playbooks/awx.md) to import the playbook as a job template in AWX / Ansible Automation Platform.

The following job template will be created:

*  **Centurion/Access/Teams** Creation and patching of teams and permissions


!!! info 
    The playbook is able to work with the inventory plugin that is included in this collection.


## Play workflow

The teams playbook gathers information regarding centurion organisations from the ansible inventory. Using this information the play is designed to create new teams, patch permissions and patch notes. The workflow for the playbook is as follows

- Fetch all organisations from Centurion ERP
- Fetch all existing teams within each organisation from Centurion ERP
- Fetch any teams to be created from inventory
- Create new teams
- Patch all teams with required permissions
- Patch all teams with required notes


## Configuration

The teams playbook uses variables that are gathered from inventory. The expected structure of the inventory file is:

```yaml

centurion_erp:
  teams:
    - name: "organisation name"
      teams:
        - name: "team-name"
          permissions: []
          notes: "permissions must be a list"

```

!!! tip "common teams"
    Common teams can be created by using yaml anchors. This is useful when multiple organisations require a common team and permissions to be set.

    ```yaml
    centurion_erp:
      common_teams:
        team_name: &team-name "team_name"
        team_permissions: &team-name-permissions []
        team_name_notes: &team-name-notes "team_notes"

      teams:
        - name: "organisation name"
          teams:
            - name: *team-name
              permissions: *team-name-permissions
              notes: *team-name-notes

    ```


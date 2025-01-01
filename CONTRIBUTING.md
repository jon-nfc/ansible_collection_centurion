# Contribution Guide

First and foremost, thank you for your contribution. If at any stage you are stuck, confused or any other developer prone state, please ask for help.


## Requirements

- Commit Messages use [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) format
- **ALL** CI jobs must pass. if they error, you can view the "details" for what went wrong.

- Ansible:

    - Tasks must be named
    - Task name must reflect their activity
    - All task modules to use FQCN
    - Don't be afraid of white space.
        - Two blanks lines above tasks
        - Two blank lines blow tasks
        - One blank line at the end of the file
    - Any task that "spills" a secret, must use `no_log`


## Dev Env
Development of this project has been setup to be done from VSCodium. The following additional requirements need to be met:

- npm has been installed. _required for `markdown` linting_

    `sudo apt install -y --no-install-recommends npm`

- setup of other requirements can be done with `make prepare`

- **ALL** Linting must pass for Merge to be conducted.

    _`make lint`_


## Makefile

!!! tip "TL;DR"
    Common make commands are `make prepare` then `make docs` and `make lint`

Included within the root of the repository is a makefile that can be used during development to check/run different items as is required during development. The following make targets are available:

- `prepare`

    _prepare the repository. init's all git submodules and sets up a python virtual env and other make targets_

- `docs`

    _builds the docs and places them within a directory called build, which can be viewed within a web browser_

- `lint`

    _conducts all required linting_

    - `ansible-lint`

        _lints ansible directories/files only. should only be used when you only want to check Ansible formatting._

    - `docs-lint`

        _lints the markdown documents within the docs directory for formatting errors that MKDocs may/will have an issue with._

- `clean`

    _cleans up build artifacts and removes the python virtual environment_


## Inventory Plugin

``` bash

# to test use
ansible-inventory -i nofusscomputing.centurion.centurion --list -vvv

```

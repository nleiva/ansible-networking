# Networking collection of Playbooks

![Ansible Lint](https://github.com/nleiva/ansible-networking/workflows/Ansible%20Lint/badge.svg)

This is my collection of Ansible Networking examples. Of course, most of these are recycled from other repositories.

## Inventory

I'm using this [ansible-inventory](https://github.com/nleiva/ansible-inventory/blob/master/hosts) to provide output examples ([DevNet always-on](https://developer.cisco.com/docs/sandbox/#!networking/networking-overview) devices).

## Examples

- [Collect a command output](collect-command.md)
- [F5 Address list](F5/address_list.md)
- [Get IP address from NetBox](NetBox/get_ip.md)
- [Meraki](meraki.md)
- [Multi-line Config](multi-line-config.md)
- [NetBox lookup](NetBox/lookup.md)
- [NTP Compliance](ntp-compliance.md)
- [Parse JSON outputs](test-json.md)
- [Parse IOS XE ACLs](ios-genie-show-acl.md)
- [Parse IOS XE SW Version](ios-genie-show-ver.md)
- [Parsing a Cisco ASA config file](https://github.com/nleiva/ansible-parsing-cisco-asa): Three options to parse data from an unstructured config file.
- [Reading IP address ranges](ip_range.md)
- [Show config differences](show-diff.md)
- [Network resource modules in action](https://github.com/nleiva/ansible-net-modules)

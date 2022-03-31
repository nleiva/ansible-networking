# Networking collection of Playbooks

![Ansible Lint](https://github.com/nleiva/ansible-networking/workflows/Ansible%20Lint/badge.svg)

This is my personal collection of Ansible Networking examples. Of course, most these are recycled from other repositories.

## Inventory

I'm using this [ansible-inventory](https://github.com/nleiva/ansible-inventory/blob/master/hosts) to provide output examples ([DevNet always-on](https://developer.cisco.com/docs/sandbox/#!networking/networking-overview) devices).

## Examples

- [Collect a command output](collect-command.md)
- [F5 Address list](F5/address_list.md)
- [Meraki](meraki.md)
- [Multi-line Config](multi-line-config.md)
- [NTP Compliance](ntp-compliance.md)
- [Parse JSON outputs](test-json.md)
- [Parse IOS XE ACL's](ios-genie-show-acl.md)
- [Parse IOS XE SW Version](ios-genie-show-ver.md)
- [Reading IP address ranges](ip_range.md)
- [Show config differences](show-diff.md)
- [Network resource modules in action](https://github.com/nleiva/ansible-net-modules)

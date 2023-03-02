# Check config diff

## Dependencies

### Collections

Install `cisco.ios`.

```bash
ansible-galaxy collection install cisco.ios
```

## Tasks

Latest version -> [show-diff](show-diff.yml). The following output might be outdated.

```yaml
- name: Backup the config
  cisco.ios.ios_config:
    backup: true
  register: config_output

- name: Print debug message
  ansible.builtin.debug:
    msg: "Backup generated {{ config_output.date }} at {{ config_output.time }}"
  tags: debug

- name: Configure ACL on Cisco IOS device using ios_config module
  cisco.ios.ios_config:
    lines:
      - 10 permit ip host 192.0.2.1 any log
      - 20 permit ip host 192.0.2.2 any log
      - 30 permit ip host 192.0.2.3 any log
      - 40 permit ip host 192.0.2.4 any log
      - 50 permit ip host 192.0.2.5 any log
    parents: ip access-list extended ACL-Ansible-CLI
    before: no ip access-list extended test
    match: exact
    save_when: modified

- name: Configure ACL on Cisco IOS device using ios_acls module
  cisco.ios.ios_acls:
    state: replaced
    config:
      - afi: ipv4
        acls:
          - name: ACL-Ansible-RM
            aces:
              - sequence: 10
                grant: deny
                source:
                  any: true
                destination:
                  address: 198.51.100.0
                  wildcard_bits: 0.0.0.255
                protocol: tcp
              - sequence: 20
                grant: permit
                source:
                  any: true
                destination:
                  any: true
                protocol: tcp

- name: Compare the Cisco IOS running-config to backup config
  cisco.ios.ios_config:
    diff_against: intended
    intended_config: "{{ lookup('file', '{{ config_output.backup_path }}') }}"
  register: diff
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook --diff show-diff.yml

PLAY [ios] *******************************************************************************************************************

TASK [Backup the config] *****************************************************************************************************
changed: [sandbox-iosxe-latest-1.cisco.com]

TASK [Print debug message] ***************************************************************************************************
ok: [sandbox-iosxe-latest-1.cisco.com] => 
  msg: Backup generated 2023-03-02 at 12:49:35

TASK [Configure ACL on Cisco IOS device using ios_config module] *************************************************************
[WARNING]: To ensure idempotency and correct diff the input configuration lines should be similar to how they appear if
present in the running configuration on device
changed: [sandbox-iosxe-latest-1.cisco.com]

TASK [Configure ACL on Cisco IOS device using ios_acls module] ***************************************************************
changed: [sandbox-iosxe-latest-1.cisco.com]

TASK [Compare the Cisco IOS running-config to backup config] *****************************************************************
--- before
+++ after
@@ -148,15 +148,12 @@
 ip ssh rsa keypair-name ssh-key
 ip ssh version 2
 ip scp server enable
-ip access-list extended ACL-Ansible-CLI
+ip access-list extended test
  10 permit ip host 192.0.2.1 any log
  20 permit ip host 192.0.2.2 any log
  30 permit ip host 192.0.2.3 any log
  40 permit ip host 192.0.2.4 any log
  50 permit ip host 192.0.2.5 any log
-ip access-list extended ACL-Ansible-RM
- 10 deny   tcp any 198.51.100.0 0.0.0.255
- 20 permit tcp any any
 control-plane
 banner motd ^C
 Welcome to the DevNet Sandbox for CSR1000v and IOS XE

changed: [sandbox-iosxe-latest-1.cisco.com]

PLAY RECAP *******************************************************************************************************************
sandbox-iosxe-latest-1.cisco.com : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```


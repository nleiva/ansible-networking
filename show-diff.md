# Check config diff

## Variables requiered

- `my_devices`: One or more groups or host patterns, separated by colons. 
- `my_facts`: Whether to collect facts per device: `yes` or `no`.

## Playbook

Latest version -> [show-diff](show-diff.yml). The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"
 
  tasks:
    - name: Backup the config, make changes and then look at the diff
      block:
        - name: Backup the config [{{ ansible_network_os | default("unknown OS") }}]
          ios_config:
            backup: yes
          register: config_output
          
        - name: Print debug message [{{ ansible_network_os | default("unknown OS") }}]
          debug:
            msg: "Backup generated {{ config_output.date }} at {{ config_output.time }}"

        - name: Load new acl into device
          ios_config:
            lines:
              - 10 permit ip host 192.0.2.1 any log
              - 20 permit ip host 192.0.2.2 any log
              - 30 permit ip host 192.0.2.3 any log
              - 40 permit ip host 192.0.2.4 any log
              - 50 permit ip host 192.0.2.5 any log
            parents: ip access-list extended test
            before: no ip access-list extended test
            match: exact

        - name: Check the running-config against backup config
          ios_config:
            diff_against: intended
            intended_config: "{{ lookup('file', 'config_output.backup_path') }}"
      when: ansible_net_system == "ios"
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook -i hosts --diff show-diff.yml -e "my_devices=ios, my_facts=yes"

PLAY [ios,] ****************************************************************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************************************
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: default value for `gather_subset` will be changed to `min` from `!config` v2.11 onwards
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [Backup the config [ios]] *********************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com]

TASK [Print debug message [ios]] *******************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "msg": "Backup generated 2020-07-08 at 09:28:34"
}

TASK [Load new acl into device] ********************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com]

TASK [Check the running-config against backup config] **********************************************************************************************************
--- before
+++ after
@@ -131,12 +131,6 @@
 ip ssh rsa keypair-name ssh-key
 ip ssh version 2
 ip scp server enable
-ip access-list extended test
- permit ip host 192.0.2.1 any log
- permit ip host 192.0.2.2 any log
- permit ip host 192.0.2.3 any log
- permit ip host 192.0.2.4 any log
- permit ip host 192.0.2.5 any log
 control-plane
 banner login ^C
 Built with Ansible

changed: [ios-xe-mgmt-latest.cisco.com]

PLAY RECAP *****************************************************************************************************************************************************
ios-xe-mgmt-latest.cisco.com : ok=5    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```


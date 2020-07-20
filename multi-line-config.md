# Multi-line Config

## Variables required

- `my_devices`: One or more groups or host patterns, separated by colons. 
- `my_facts`: Whether to collect facts per device: `yes` or `no`.
- `my_config`: Config to apply. Ex: 

```yaml
my_config: |
  ip access-list standard TEST_ACL
  permit 192.0.2.1
  remark doc-ip
```

## Playbook

Latest version -> [collect-command](collect-command.yml). The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"

  tasks:
    - name: multiline config
      cli_config:
        config: "{{ my_config }}"
```

## Output

The following output might be outdated.

```bash
SSH password: 
BECOME password[defaults to SSH password]: 

PLAY [ios] *********************************************************************

TASK [multi-line config] *******************************************************
ip access-list standard TEST_ACL
permit 192.0.2.1
remark doc-ip
changed: [18.208.199.107]

PLAY RECAP *********************************************************************
18.208.199.107             : ok=1    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0    
```


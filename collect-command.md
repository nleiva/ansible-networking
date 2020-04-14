# Collecting the output of a given command

## Variables requiered

- `my_devices`: One or more groups or host patterns, separated by colons. 
- `my_facts`: Whether to collect facts per device: `yes` or `no`.
- `my_cmd`: Command to issue. Ex: `show version | i ersion`

## Playbook

Latest version -> [collect-command](collect-command.yml). The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"
 
  tasks: 
    - name: Capture SHOW COMMAND
      cli_command:
        command:  "{{ my_cmd }}"
      register: cmd_output

    - name: Display OUTPUT
      debug:
        msg: Output is {{ cmd_output.stdout }}
```

## Output

The following output might be outdated.

```bash
PLAY [ssh_devices] *************************************************************

TASK [Capture SHOW COMMAND] ****************************************************
ok: [CSR1000V SSH]
ok: [IOS XRv 9000 SSH]
ok: [Nexus 9000v SSH]

TASK [Display OUTPUT] **********************************************************
ok: [CSR1000V SSH] => {
    "msg": "Output is Cisco IOS XE Software, Version 16.11.01a\nCisco IOS Software [Gibraltar], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.11.1a, RELEASE SOFTWARE (fc1)\nlicensed under the GNU General Public License (\"GPL\") Version 2.0.  The\nsoftware code licensed under GPL Version 2.0 is free software that comes\nGPL code under the terms of GPL Version 2.0.  For more details, see the"
}
ok: [IOS XRv 9000 SSH] => {
    "msg": "Output is Cisco IOS XR Software, Version 6.5.3\n Version      : 6.5.3"
}
ok: [Nexus 9000v SSH] => {
    "msg": "Output is Nexus 9000v is a demo version of the Nexus Operating System\n  BIOS: version \n  NXOS: version 9.2(1)\n  System version:"
}

PLAY RECAP *********************************************************************
CSR1000V SSH               : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
IOS XRv 9000 SSH           : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
Nexus 9000v SSH            : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```


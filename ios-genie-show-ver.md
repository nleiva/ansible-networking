# Parse IOS XE SW Version

## Pre-requisites

Have [parse_genie](https://galaxy.ansible.com/clay584/parse_genie) role installed.

```bash
sudo yum install python3-devel
sudo pip3 install psutil
sudo pip3 install paramiko
sudo pip3 install pyats
sudo pip3 install genie

ansible-galaxy install -r roles/requirements.yml
```

## Variables required

- `my_devices`: One or more groups or host patterns, separated by colons. 
- `my_facts`: Whether to collect facts per device: `yes` or `no`.

## Playbook

Latest version -> [ios-genie-show-ver](ios-genie-show-ver.yml). The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"
 
  tasks:
  - name: show version
    ios_command:
      commands:
        - show version
    register: version

  - name: Set Fact Genie Filter
    set_fact:
      pyats_version: "{{ version['stdout'][0] | parse_genie(command='show version', os='ios') }}"

  - name: Debug Pyats facts - all
    debug:
     var: pyats_version.version
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook -i hosts -e "my_devices=ios, my_facts=no" ios-genie-show-ver.yml

PLAY [IOS show version genie example] *****************************************************************************************************

TASK [show version] ***********************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [Set Fact Genie Filter] **************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [Debug Pyats facts - all] ************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "pyats_version.version": {
        "chassis": "CSR1000V",
        "chassis_sn": "9ANAICM566S",
        "compiled_by": "mcpre",
        "compiled_date": "Thu 11-Apr-19 23:59",
        "curr_config_register": "0x2102",
        "disks": {
            "bootflash:.": {
                "disk_size": "7774207",
                "type_of_disk": "virtual hard disk"
            },
            "webui:.": {
                "disk_size": "0",
                "type_of_disk": "WebUI ODM Files"
            }
        },
        "hostname": "csr1000v-1",
        "image_id": "X86_64_LINUX_IOSD-UNIVERSALK9-M",
        "image_type": "production image",
        "last_reload_reason": "reload",
        "license_level": "ax",
        "license_type": "N/A(Smart License Enabled)",
        "main_mem": "2378575",
        "mem_size": {
            "non-volatile configuration": "32768",
            "physical": "8112832"
        },
        "next_reload_license_level": "ax",
        "number_of_intfs": {
            "Gigabit Ethernet": "3"
        },
        "os": "IOS-XE",
        "platform": "Virtual XE",
        "processor_type": "VXE",
        "returned_to_rom_by": "reload",
        "rom": "IOS-XE ROMMON",
        "rtr_type": "CSR1000V",
        "system_image": "bootflash:packages.conf",
        "uptime": "3 days, 1 hour, 40 minutes",
        "uptime_this_cp": "3 days, 1 hour, 41 minutes",
        "version": "16.11.1a",
        "version_short": "16.11"
    }
}

TASK [Debug Pyats facts - version] ********************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "pyats_version.version.version": "16.11.1a"
}

TASK [Debug Pyats facts - uptime] *********************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "pyats_version.version.uptime": "3 days, 1 hour, 40 minutes"
}

PLAY RECAP ********************************************************************************************************************************
ios-xe-mgmt-latest.cisco.com : ok=5    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```


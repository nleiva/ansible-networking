# Meraki

## Variables requiered

- `api_key`: API Key. 
- `org_name`: Organization name, example `DevNet Sandbox`.


## Playbook

Latest version -> [meraki](meraki.yml). The following output might be outdated.

```yaml
- name: Meraki Test
  hosts: localhost
  gather_facts: no
  collections:
    - cisco.meraki

  tasks:
    - name: Query information about all organizations associated to the API user
      meraki_organization:
        auth_key: "{{ api_key }}"
        state: query
      delegate_to: localhost
      register: orgs

    - debug:
        var: orgs.data[2]

    - name: Query all devices in organization {{ org_name }}
      meraki_device:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        state: query
      register: devices

    - debug:
        var: devices.data[16]

    - name: Query management information
      meraki_management_interface:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        state: query
        net_id: "{{ devices.data[16].network_id }}"
        serial: "{{ devices.data[16].serial }}"
      register: mgmt

    - debug:
        var: mgmt

    - name: Query information about all administrators associated to the organization {{ org_name }}
      meraki_admin:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        state: query
      register: admins

    - debug:
        msg: " {{ admins.data[3].name }} at {{ admins.data[3].email }} has API Key -> {{ admins.data[3].has_api_key }}"

    - name: Query SNMP settings in the {{ org_name }} organization
      meraki_snmp:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        state: query
      register: snmp

    - debug:
        var: snmp

    - name: List all networks associated to the {{ org_name }} organization
      meraki_network:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        state: query
      register: nets

    - name: Query network named {{ nets.data[0].name }} in the {{ org_name }} organization
      meraki_network:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        net_name: "{{ nets.data[0].name }}"
        state: query
      register: net

    - name: Query syslog configurations on network named {{ nets.data[0].name }} in the {{ org_name }} organization
      meraki_syslog:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        net_name: "{{ nets.data[0].name }}"
        state: query
      register: syslog

    - debug:
        var: syslog

    - name: List SSID(s) on network {{ nets.data[0].name }}
      meraki_ssid:
        auth_key: "{{ api_key }}"
        org_name: "{{ org_name }}"
        net_name: "{{ nets.data[0].name }}"
        state: query
      register: ssids
        
    - debug:
        var: ssids.data[0]
```

## Output

The following output might be outdated.

```bash
 ⇨  ansible-playbook meraki.yml 
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [Meraki Test] *******************************************************************************************************

TASK [Query information about all organizations associated to the API user] **********************************************
ok: [localhost -> localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "orgs.data[2]": {
        "id": "549236",
        "name": "DevNet Sandbox",
        "url": "https://n149.meraki.com/o/-t35Mb/manage/organization/overview"
    }
}

TASK [Query all devices in organization DevNet Sandbox] ******************************************************************
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "devices.data[16]": {
        "claimed_at": "1519658520.55085",
        "mac": "e0:55:3d:17:d4:23",
        "model": "MX65",
        "name": "",
        "network_id": "L_646829496481105433",
        "public_ip": "64.103.26.57",
        "serial": "Q2QN-9J8L-SLPD"
    }
}

TASK [Query management information] **************************************************************************************
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "mgmt": {
        "changed": false,
        "data": {
            "ddns_hostnames": {
                "active_ddns_hostname": "devnet-sandbox-always-on-wired-vzhddpprjp.dynamic-m.com",
                "ddns_hostname_wan1": "devnet-sandbox-always-on-wired-vzhddpprjp-1.dynamic-m.com",
                "ddns_hostname_wan2": "devnet-sandbox-always-on-wired-vzhddpprjp-2.dynamic-m.com"
            },
            "wan1": {
                "using_static_ip": false,
                "vlan": null,
                "wan_enabled": "not configured"
            },
            "wan2": {
                "using_static_ip": false,
                "vlan": null,
                "wan_enabled": "not configured"
            }
        },
        "failed": false,
        "response": "OK (unknown bytes)",
        "status": 200
    }
}

TASK [Query information about all administrators associated to the organization DevNet Sandbox] **************************
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "msg": " devnetmerakiadmin at devnetmerakiadmin@cisco.com has API Key -> True"
}

TASK [Query SNMP settings in the DevNet Sandbox organization] ************************************************************
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "snmp": {
        "changed": false,
        "data": {
            "hostname": "snmp.meraki.com",
            "peer_ips": null,
            "port": 16100,
            "v2c_enabled": false,
            "v3_auth_mode": "SHA",
            "v3_enabled": false,
            "v3_priv_mode": "AES128"
        },
        "failed": false,
        "response": "OK (unknown bytes)",
        "status": 200
    }
}

TASK [List all networks associated to the DevNet Sandbox organization] ***************************************************
ok: [localhost]

TASK [Query network named DevNet Sandbox ALWAYS ON in the DevNet Sandbox organization] ***********************************
ok: [localhost]

TASK [Query syslog configurations on network named DevNet Sandbox ALWAYS ON in the DevNet Sandbox organization] **********
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "syslog": {
        "changed": false,
        "data": [],
        "failed": false,
        "response": "OK (unknown bytes)",
        "status": 200
    }
}

TASK [List SSID(s) on network DevNet Sandbox ALWAYS ON] ******************************************************************
ok: [localhost]

TASK [debug] *************************************************************************************************************
ok: [localhost] => {
    "ssids.data[0]": {
        "auth_mode": "open",
        "availability_tags": [],
        "available_on_all_aps": true,
        "band_selection": "Dual band operation",
        "enabled": true,
        "ip_assignment_mode": "NAT mode",
        "min_bitrate": 11,
        "name": "DevNet Sandbox ALWAYS ON - wirel",
        "number": 0,
        "per_client_bandwidth_limit_down": 0,
        "per_client_bandwidth_limit_up": 0,
        "radius_accounting_enabled": null,
        "splash_page": "None",
        "ssid_admin_accessible": false,
        "visible": true
    }
}

PLAY RECAP ***************************************************************************************************************
localhost                  : ok=16   changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
```


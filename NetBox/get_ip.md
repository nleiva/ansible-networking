# NetBox

## Dependencies

### Collections

Install `netbox.netbox` and `ansible.utils`.
```bash
ansible-galaxy collection install netbox.netbox ansible.utils
```

#### Python libraries

Install `pynetbox`

```
pip3 install pynetbox
```

#### NetBox credentials

Make your NetBox creadentials available, for example:

```
export NETBOX_URL=https://demo.netbox.dev/
export NETBOX_TOKEN=e150845b04b2f7336180dbb3137e29d963e4b23f
```

## Tasks

Latest version -> [get_ip](get_ip.yml). The following output might be outdated.

```yaml
- name: Get a new /24 inside {{ primary_prefix }} within NetBox
    netbox.netbox.netbox_prefix:
    netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
    netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
    data:
        parent: "{{ primary_prefix }}"
        prefix_length: 24
    state: present
    first_available: true
    register: prefix_info

- name: Print return information from the previous task
    ansible.builtin.debug:
    var: prefix_info
    tags: debug

- name: Allocate IP address from new range
    netbox.netbox.netbox_ip_address:
    netbox_url: "{{ lookup('env', 'NETBOX_URL') }}"
    netbox_token: "{{ lookup('env', 'NETBOX_TOKEN') }}"
    data:
        prefix: "{{ prefix_info['prefix']['prefix'] }}"
    state: new
    register: ip_address_info

- name: Print return information from the previous task
    ansible.builtin.debug:
    var: ip_address_info
    tags: debug

- name: Create variables with IP information
    ansible.builtin.set_fact:
    ip_address: "{{ ip_address_info['ip_address']['address'] | ansible.utils.ipaddr('ip')  }}"
    netmask: "{{ ip_address_info['ip_address']['address'] | ansible.utils.ipaddr('netmask') }}"

- name: Print return information from the previous task
    ansible.builtin.debug:
    msg: 
    - "IP: {{ ip_address }}"
    - "Mask: {{ netmask }}"
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook get_ip.yml --skip-tags=debug

PLAY [Manage NetBox] ************************************************************************************************

TASK [Get a new /24 inside 172.16.0.0/16 within NetBox] *************************************************************
changed: [localhost]

TASK [Allocate IP address from new range] ***************************************************************************
changed: [localhost]

TASK [Create variables with IP information] *************************************************************************
ok: [localhost]

TASK [Print return information from the previous task] **************************************************************
ok: [localhost] => {
    "msg": [
        "IP: 172.16.6.1",
        "Mask: 255.255.255.0"
    ]
}

PLAY RECAP **********************************************************************************************************
localhost                  : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```


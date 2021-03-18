# Reading IP address ranges

## Variables required

### Inputs

JSON file [ip_addresses.json](files/ip_addresses.json).

```json
{
   "syncToken": "0123456789",
   "createDate": "yyyy-mm-dd-hh-mm-ss",
   "prefixes": [
     {
       "ip_prefix": "192.0.2.0/24",
       "region": "region",
       "network_border_group": "network_border_group",
       "service": "subset"
     }
   ],
   "ipv6_prefixes": [
     {
       "ipv6_prefix": "2001:db8:cafe::/64",
       "region": "region",
       "network_border_group": "network_border_group",
       "service": "subset"
     }
   ]  
 }
```


## Playbook

Latest version -> [ip_range](ip_range.yml). The following output might be outdated.

```yaml
- name: Play around with IP address ranges
  hosts: localhost
  connection: local
  become: false
  gather_facts: false
  vars:
    input: "{{ lookup('file','files/ip_addresses.json') | from_json }}"
    test_list: ['192.0.2.18', 'host.fqdn', '::1', '192.168.32.0/24', 'fe80::100/10',
      '2001:db8:cafe::f00/64', True, '', '42540766412265424405338506004571095040/64']

  tasks:
    - name: Create IPv4 List
      set_fact:
        ipv4_list: "{{ input.prefixes }}"

    - name: Create IPv6 List
      set_fact:
        ipv6_list: "{{ input.ipv6_prefixes }}"

    - name: TEST 1
      block:
      - name: Loop over IPv4 addresses
        debug:
          msg: "{{ item.ip_prefix }}"
        with_items: "{{ ipv4_list }}"

    - name: TEST 2
      block:
      - name: Print first and last ip of an IPv4 range (query by index number)
        debug:
          msg: "{{ item.ip_prefix | ipaddr('1') | ipv4('address') }}-{{ item.ip_prefix | ipaddr('-1') | ipv4('address') }}"
        with_items: "{{ ipv4_list }}"

    - name: TEST 3
      block:
      - name: Print first and last ip of an IPv6 range (query by index number)
        debug:
          msg: "{{ item.ipv6_prefix | ipaddr('1') | ipv6('address') }}-{{ item.ipv6_prefix | ipaddr('-1') | ipv6('address') }}"
        with_items: "{{ ipv6_list }}"

    - name: TEST 4
      block:
      - name: Check if values in 'test_list' are in the range of an IPv4 prefix
        debug:
          msg: "{{ test_list | ipaddr(item.ip_prefix) }}"
        with_items: "{{ ipv4_list }}"

    - name: TEST 5
      block:
      - name: Check if values in 'test_list' are in the range of an IPv6 prefix
        debug:
          msg: "{{ test_list | ipaddr(item.ipv6_prefix) }}"
        with_items: "{{ ipv6_list }}"
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook ip_range.yml
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Play around with IP address ranges] ****************************************************************************************

TASK [Create IPv4 List] **********************************************************************************************************
ok: [localhost]

TASK [Create IPv6 List] **********************************************************************************************************
ok: [localhost]

TASK [Loop over IPv4 addresses] **************************************************************************************************
ok: [localhost] => (item={'ip_prefix': '192.0.2.0/24', 'region': 'region', 'network_border_group': 'network_border_group', 'service': 'subset'}) => {
    "msg": "192.0.2.0/24"
}

TASK [Print first and last ip of an IPv4 range (query by index number)] **********************************************************
ok: [localhost] => (item={'ip_prefix': '192.0.2.0/24', 'region': 'region', 'network_border_group': 'network_border_group', 'service': 'subset'}) => {
    "msg": "192.0.2.1-192.0.2.255"
}

TASK [Print first and last ip of an IPv6 range (query by index number)] **********************************************************
ok: [localhost] => (item={'ipv6_prefix': '2001:db8:cafe::/64', 'region': 'region', 'network_border_group': 'network_border_group', 'service': 'subset'}) => {
    "msg": "2001:db8:cafe::1-2001:db8:cafe:0:ffff:ffff:ffff:ffff"
}

TASK [Check if values in 'test_list' are in the range of an IPv4 prefix] *********************************************************
ok: [localhost] => (item={'ip_prefix': '192.0.2.0/24', 'region': 'region', 'network_border_group': 'network_border_group', 'service': 'subset'}) => {
    "msg": [
        "192.0.2.18"
    ]
}

TASK [Check if values in 'test_list' are in the range of an IPv6 prefix] *********************************************************
ok: [localhost] => (item={'ipv6_prefix': '2001:db8:cafe::/64', 'region': 'region', 'network_border_group': 'network_border_group', 'service': 'subset'}) => {
    "msg": [
        "2001:db8:cafe::f00/64"
    ]
}

PLAY RECAP ***********************************************************************************************************************
localhost                  : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


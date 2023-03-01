# NetBox

## Variables required

### Dependencies

Install `netbox.netbox` and `community.general`.
```bash
ansible-galaxy collection install netbox.netbox community.general
```

#### Python libraries

Install `pynetbox` and `jmespath`.

```
pip3 install pynetbox jmespath --user 
```

#### NetBox credentials

Make your NetBox creadentials available, for example:

```
export NETBOX_URL=https://demo.netbox.dev/
export NETBOX_TOKEN=e150845b04b2f7336180dbb3137e29d963e4b23f
```

## Tasks

Latest version -> [lookup](lookup.yml). The following output might be outdated.

```yaml
- name: Get list of sites
    ansible.builtin.set_fact:
    sites: "{{ query('netbox.netbox.nb_lookup', 'sites', api_endpoint=netbox_url, token=netbox_token) }}"

- name: Clean up the output
    ansible.builtin.debug:
    msg: "{{ sites | community.general.json_query('[*].value.name') }}"

- name: Get list of devices with role Core Switch at MDF (ncsu-065) or DM-Buffalo (dm-buffalo) sites
    ansible.builtin.set_fact:
    devices: |
        {{ query('netbox.netbox.nb_lookup', 'devices', api_filter='site=ncsu-065 site=dm-buffalo
        role=core-switch', api_endpoint=netbox_url, token=netbox_token) }}

- name: Print the result
    ansible.builtin.debug:
    msg: "{{ devices | json_query('[*].value.name') }}"
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook lookup.yml --skip-tags=debug

PLAY [Manage NetBox] ************************************************************************************************

TASK [Get list of sites] ********************************************************************************************
ok: [localhost]

TASK [Clean up the output] ******************************************************************************************
ok: [localhost] => {
    "msg": [
        "ATKNB",
        "Butler Communications",
        "D. S. Weaver Labs",
        "DM-Akron",
        "DM-Albany",
        "DM-Binghamton",
        "DM-Buffalo",
        "DM-Camden",
        "DM-NYC",
        "DM-Nashua",
        "DM-Pittsfield",
        "DM-Rochester",
        "DM-Scranton",
        "DM-Stamford",
        "DM-Syracuse",
        "DM-Utica",
        "DM-Yonkers",
        "Grinnells Lab",
        "Gênes",
        "JBB Branch 104",
        "JBB Branch 109",
        "JBB Branch 115",
        "JBB Branch 120",
        "JBB Branch 127",
        "JBB Branch 133",
        "MDF",
        "My First Site",
        "Test Site",
        "foo",
        "ssa-20-20",
        "staging_nellie"
    ]
}

TASK [Get list of devices with role Core Switch at MDF (ncsu-065) or DM-Buffalo (dm-buffalo) sites] *****************
ok: [localhost]

TASK [Print the result] *********************************************************************************************
ok: [localhost] => {
    "msg": [
        "CORE-VSS-1",
        "ncsu-coreswitch1",
        "ncsu-coreswitch2"
    ]
}

PLAY RECAP **********************************************************************************************************
localhost                  : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```


# Parsing JSON outputs

## Variables required

### Dependencies

Install `ansible.utils`.

```bash
ansible-galaxy collection install ansible.utils
```

### Inputs

JSON file [ospf.json](files/ospf.json).

```json
{ 
    "test": {
       "interfaces": {
           "Tunnel0": {
               "neighbors": {
                   "203.0.113.2": {
                       "address": "198.51.100.2",
                       "dead_time": "00:00:39",
                       "priority": 0,
                       "state": "FULL/  -"
                   }
               }
           },
           "Tunnel1": {
               "neighbors": {
                   "203.0.113.2": {
                       "address": "192.0.2.2",
                       "dead_time": "00:00:36",
                       "priority": 0,
                       "state": "INIT/  -"
                   }
               }
           }
       }
    }
}
```


## Playbook

Latest version -> [test-json](test-json.yml). The following output might be outdated.

```yaml
- name: Play around with JSON inputs
  hosts: localhost
  connection: local
  become: false
  gather_facts: false
  vars:
    input: "{{ lookup('file','files/ospf.json') | from_json }}"

  tasks:
    - name: Create interfaces Dictionary
      set_fact:
        interfaces: "{{ input.test.interfaces }}"
  
    - name: Print out flatten interfaces input
      debug:
        msg:  "{{ lookup('ansible.utils.to_paths', interfaces) }}"

    - name: TEST 1
      block:
      - name: Loop over interfaces
        include_tasks: test-json-tasks-1.yml
        with_items: "{{ interfaces | dict2items }}"

    - name: TEST 2
      block:
      - name: Create neighbors dictionary (this is now per interface)
        set_fact:
          neighbors: "{{ interfaces | json_query('*.neighbors') }}"

      - name: Loop over neighbors
        include_tasks: test-json-tasks-2.yml
        with_items: "{{ neighbors }}"
        loop_control:
          loop_var: data

    - name: TEST 3
      block:
      - name: Loop over neighbors
        include_tasks: test-json-tasks-3.yml
        with_items: "{{ neighbors }}"
        loop_control:
          loop_var: data

    - name: TEST 4
      block:
      - name: Loop with deep json_query
        debug:
          var: "{{ item }}"
        with_items: "{{ input | json_query('test.interfaces.*.neighbors[].*.[address, state]') }}"
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook test-json.yml 
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [Play around with JSON inputs] *************************************************************************************************************

TASK [Create interfaces Dictionary] *************************************************************************************************************
ok: [localhost]

TASK [Print out flatten interfaces input] *******************************************************************************************************
ok: [localhost] => {
    "msg": {
        "Tunnel0.neighbors['203.0.113.2'].address": "198.51.100.2",
        "Tunnel0.neighbors['203.0.113.2'].dead_time": "00:00:39",
        "Tunnel0.neighbors['203.0.113.2'].priority": 0,
        "Tunnel0.neighbors['203.0.113.2'].state": "FULL/  -",
        "Tunnel1.neighbors['203.0.113.2'].address": "192.0.2.2",
        "Tunnel1.neighbors['203.0.113.2'].dead_time": "00:00:36",
        "Tunnel1.neighbors['203.0.113.2'].priority": 0,
        "Tunnel1.neighbors['203.0.113.2'].state": "INIT/  -"
    }
}

TASK [Loop over interfaces] *********************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-1.yml for localhost
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-1.yml for localhost

TASK [Print out neighbor data - FORMAT 1] *******************************************************************************************************
ok: [localhost] => {
    "msg": "Neighbor: 203.0.113.2, with address: 198.51.100.2 -> State: FULL"
}

TASK [Print out neighbor data - FORMAT 1] *******************************************************************************************************
ok: [localhost] => {
    "msg": "Neighbor: 203.0.113.2, with address: 192.0.2.2 -> State: INIT"
}

TASK [Create neighbors dictionary (this is now per interface)] **********************************************************************************
ok: [localhost]

TASK [Loop over neighbors] **********************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-2.yml for localhost
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-2.yml for localhost

TASK [Print out neighbor data - FORMAT 2] *******************************************************************************************************
ok: [localhost] => {
    "msg": "Neighbor: 203.0.113.2, with address: 198.51.100.2 -> State: FULL"
}

TASK [Print out neighbor data - FORMAT 2] *******************************************************************************************************
ok: [localhost] => {
    "msg": "Neighbor: 203.0.113.2, with address: 192.0.2.2 -> State: INIT"
}

TASK [Loop over neighbors] **********************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-3.yml for localhost
included: /home/nleiva/Ansible/ansible-networking/test-json-tasks-3.yml for localhost

TASK [Print out a WARNING if OSPF state is not FULL] ********************************************************************************************
skipping: [localhost]

TASK [Print out a WARNING if OSPF state is not FULL] ********************************************************************************************
ok: [localhost] => {
    "msg": "WARNING: Neighbor 203.0.113.2, with address 192.0.2.2 is in state INIT"
}

TASK [Loop with deep json_query] ****************************************************************************************************************
ok: [localhost] => (item=['198.51.100.2', 'FULL/  -']) => {
    "<class 'list'>": "VARIABLE IS NOT DEFINED!",
    "ansible_loop_var": "item",
    "item": [
        "198.51.100.2",
        "FULL/  -"
    ]
}
ok: [localhost] => (item=['192.0.2.2', 'INIT/  -']) => {
    "<class 'list'>": "VARIABLE IS NOT DEFINED!",
    "ansible_loop_var": "item",
    "item": [
        "192.0.2.2",
        "INIT/  -"
    ]
}

PLAY RECAP **************************************************************************************************************************************
localhost                  : ok=15   changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

```


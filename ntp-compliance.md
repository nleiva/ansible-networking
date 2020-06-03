# NTP Compliance

## Pre-requisites

The boto package is required.

```
sudo pip3 install boto3
```

You need AWS credentials to create a Compliance report on S3. You need to export `AWS_ACCESS_KEY` and `AWS_SECRET_KEY` before executing.

## Variables required

- `my_devices`: One or more groups or host patterns, separated by colons. 
- `my_facts`: Whether to collect facts per device: `yes` or `no`.
- `my_bucket`: S3 bucket where to host the report. Ex `mydemo.run`.
- `my_ntp_servers`: List of NTP server IP addresses.

## Playbook

Latest version -> [ios-genie-show-ver][1]. The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"
 
  tasks:
    - name: Check existing NTP Servers
        include_role:
        name: ntpcheck
        when: ansible_network_os is defined

    # Adds NTP server entries in the my_ntp_servers variable if the variable erase is false
    - block:
        - name: Compare NTP servers and remove erroneous entries
        cli_config:
            config: no {{ item }}
        loop: "{{ configured_servers }}"
        when:
            - configured_servers | length > 0
            - item not in required_servers

        - name: Ensure intended NTP servers are present
        cli_config:
            config: "{{ item }}"
        loop: "{{ required_servers }}"
        when: not erase|bool

    - name: Save template to temporary file
        template:
        src: report.j2
        dest: ./temp.html
        mode: '0755'
        when: in_servers | length > 0 or out_servers | length > 0

    # Creates and uploads a report to S3 
    - name: Upload report to S3
        aws_s3:
        bucket: "{{ my_bucket }}"
        src: "./temp.html"
        object: "index.html"
        mode: put
        metadata: 'Content-Type=text/html'
        when: in_servers | length > 0 or out_servers | length > 0
```

## Output

The following output might be outdated.

```bash
⇨  ansible-playbook -i hosts ntp-compliance.yml --extra-vars='{"my_devices": "ios, iosxr", "my_facts": no, "my_bucket": "mydemo.run", "my_ntp_servers": [129.6.15.33, 132.163.96.5]}'

PLAY [NTP Server configuration compliance for Network Elements] *************************************************************************************************************************

TASK [Read inputs and prepare configs] **************************************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => (item=None)
ok: [sbx-iosxr-mgmt.cisco.com] => (item=None)
ok: [ios-xe-mgmt-latest.cisco.com] => (item=None)
ok: [ios-xe-mgmt-latest.cisco.com]
ok: [sbx-iosxr-mgmt.cisco.com] => (item=None)
ok: [sbx-iosxr-mgmt.cisco.com]

TASK [Check existing NTP Servers] *******************************************************************************************************************************************************

TASK [ntpcheck : Check NTP config per vendor OS] ****************************************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/roles/ntpcheck/tasks/ios.yml for ios-xe-mgmt-latest.cisco.com
included: /home/nleiva/Ansible/ansible-networking/roles/ntpcheck/tasks/iosxr.yml for sbx-iosxr-mgmt.cisco.com

TASK [ntpcheck : Get current NTP servers [IOS]] *****************************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [ntpcheck : Remove non config lines [IOS]] *****************************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [ntpcheck : Print current NTP servers [IOS]] ***************************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "configured_servers": [
        "ntp server 129.6.15.32",
        "ntp server 132.163.96.6"
    ]
}

TASK [ntpcheck : Generate data for reporting] *******************************************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/roles/ntpcheck/tasks/report/data.yml for ios-xe-mgmt-latest.cisco.com

TASK [ntpcheck : Determine configuration delta for reporting [ios]] *********************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [ntpcheck : Create list of NEW servers to configure [ios]] *************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 129.6.15.33)
ok: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 132.163.96.5)

TASK [ntpcheck : Create list of servers to remove [ios]] ********************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 129.6.15.32)
ok: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 132.163.96.6)

TASK [ntpcheck : Print out fidings for reporting [ios]] *********************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "msg": [
        "We are missing the following NTP Servers in IOS: ['129.6.15.33', '132.163.96.5']",
        "We will delete these NTP Servers in IOS: ['129.6.15.32', '132.163.96.6']"
    ]
}

TASK [ntpcheck : Get current NTP servers [IOS XR]] **************************************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com]

TASK [ntpcheck : Remove non config lines [IOS XR]] **************************************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com]

TASK [ntpcheck : Print current NTP servers [IOS XR]] ************************************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com] => {
    "configured_servers": [
        "ntp server 129.6.15.32",
        "ntp server 132.163.96.6"
    ]
}

TASK [ntpcheck : Generate data for reporting] *******************************************************************************************************************************************
included: /home/nleiva/Ansible/ansible-networking/roles/ntpcheck/tasks/report/data.yml for sbx-iosxr-mgmt.cisco.com

TASK [ntpcheck : Determine configuration delta for reporting [iosxr]] *******************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com]

TASK [ntpcheck : Create list of NEW servers to configure [iosxr]] ***********************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 129.6.15.33)
ok: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 132.163.96.5)

TASK [ntpcheck : Create list of servers to remove [iosxr]] ******************************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 129.6.15.32)
ok: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 132.163.96.6)

TASK [ntpcheck : Print out fidings for reporting [iosxr]] *******************************************************************************************************************************
ok: [sbx-iosxr-mgmt.cisco.com] => {
    "msg": [
        "We are missing the following NTP Servers in IOSXR: ['129.6.15.33', '132.163.96.5']",
        "We will delete these NTP Servers in IOSXR: ['129.6.15.32', '132.163.96.6']"
    ]
}

TASK [Compare NTP servers and remove erroneous entries] *********************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 129.6.15.32)
changed: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 129.6.15.32)
changed: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 132.163.96.6)
changed: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 132.163.96.6)

TASK [Ensure intended NTP servers are present] ******************************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 129.6.15.33)
changed: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 129.6.15.33)
changed: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 132.163.96.5)
changed: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 132.163.96.5)

TASK [Save template to temporary file] **************************************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com]
changed: [sbx-iosxr-mgmt.cisco.com]

TASK [Upload report to S3] **************************************************************************************************************************************************************
changed: [ios-xe-mgmt-latest.cisco.com]
changed: [sbx-iosxr-mgmt.cisco.com]

TASK [Remove all existing NTP server entries] *******************************************************************************************************************************************
skipping: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 129.6.15.32) 
skipping: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 129.6.15.32) 
skipping: [ios-xe-mgmt-latest.cisco.com] => (item=ntp server 132.163.96.6) 
skipping: [sbx-iosxr-mgmt.cisco.com] => (item=ntp server 132.163.96.6) 

PLAY RECAP ******************************************************************************************************************************************************************************
ios-xe-mgmt-latest.cisco.com : ok=14   changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   
sbx-iosxr-mgmt.cisco.com   : ok=14   changed=4    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0 

```

The report:

![NTP report][2]


[1]: ios-genie-show-ver.yml
[2]: files/pictures/ntp-report.png
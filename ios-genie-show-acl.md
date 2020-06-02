# Collecting the output of a given command

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

Latest version -> [ios-genie-show-acl](ios-genie-show-acl.yml). The following output might be outdated.

```yaml
  hosts: "{{ my_devices }}"
  gather_facts: "{{ my_facts }}"
 
  tasks: 
    - name: SHOW ACL's
      ios_command:
        commands:
          - show ip access-lists
      register: acls

    - name: PARSE with GENIE
      set_fact:
        pyats_acls: "{{ acls['stdout'][0] | parse_genie(command='show ip access-lists', os='iosxe') }}"

    - name: PRINT OUT
      debug:
      var: pyats_acls
```

## Output

The following output might be outdated.

```bash
⇨   ansible-playbook -i hosts -e "my_devices=ios, my_facts=no" ios-genie-show-acl.yml

PLAY [IOS-XE Parse ACL's] *****************************************************************************************************************

TASK [SHOW ACL's] *************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [PARSE with GENIE] *******************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com]

TASK [PRINT OUT] **************************************************************************************************************************
ok: [ios-xe-mgmt-latest.cisco.com] => {
    "pyats_acls": {
        "TEST": {
            "aces": {
                "10": {
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "destination_network": {
                                    "any": {
                                        "destination_network": "any"
                                    }
                                },
                                "protocol": "tcp",
                                "source_network": {
                                    "any": {
                                        "source_network": "any"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "tcp": {
                                "destination_port": {
                                    "operator": {
                                        "operator": "eq",
                                        "port": 80
                                    }
                                },
                                "established": false
                            }
                        }
                    },
                    "name": "10"
                },
                "20": {
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "destination_network": {
                                    "any": {
                                        "destination_network": "any"
                                    }
                                },
                                "protocol": "tcp",
                                "source_network": {
                                    "any": {
                                        "source_network": "any"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "tcp": {
                                "destination_port": {
                                    "operator": {
                                        "operator": "eq",
                                        "port": 443
                                    }
                                },
                                "established": false
                            }
                        }
                    },
                    "name": "20"
                },
                "30": {
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "destination_network": {
                                    "host 8.8.8.8": {
                                        "destination_network": "host 8.8.8.8"
                                    }
                                },
                                "protocol": "tcp",
                                "source_network": {
                                    "any": {
                                        "source_network": "any"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "tcp": {
                                "destination_port": {
                                    "operator": {
                                        "operator": "eq",
                                        "port": 53
                                    }
                                },
                                "established": false
                            }
                        }
                    },
                    "name": "30"
                },
                "40": {
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "destination_network": {
                                    "host 8.8.8.8": {
                                        "destination_network": "host 8.8.8.8"
                                    }
                                },
                                "protocol": "udp",
                                "source_network": {
                                    "any": {
                                        "source_network": "any"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "udp": {
                                "destination_port": {
                                    "operator": {
                                        "operator": "eq",
                                        "port": 53
                                    }
                                },
                                "established": false
                            }
                        }
                    },
                    "name": "40"
                },
                "50": {
                    "actions": {
                        "forwarding": "permit",
                        "logging": "log-none"
                    },
                    "matches": {
                        "l3": {
                            "ipv4": {
                                "destination_network": {
                                    "any": {
                                        "destination_network": "any"
                                    }
                                },
                                "protocol": "tcp",
                                "source_network": {
                                    "192.0.2.0 0.0.0.255": {
                                        "source_network": "192.0.2.0 0.0.0.255"
                                    }
                                }
                            }
                        },
                        "l4": {
                            "tcp": {
                                "established": false
                            }
                        }
                    },
                    "name": "50"
                }
            },
            "name": "TEST",
            "type": "ipv4-acl-type"
        },
        "meraki-fqdn-dns": {
            "name": "meraki-fqdn-dns",
            "type": "ipv4-acl-type"
        }
    }
}

PLAY RECAP ********************************************************************************************************************************
ios-xe-mgmt-latest.cisco.com : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```


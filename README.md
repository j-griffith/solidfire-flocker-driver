SolidFire Plugin for ClusterHQ-Flocker
======================================
Plugin for SolidFire Flocker integration

## Description
This plugin provides the ability to use SolidFire Storage Clusters as backend
devices in a Flocker deployment.

## Installation
Each of the following packages needs to be installed on EVERY Flocker Node

- Open-iSCSI
  * Ubuntu<br>
  ```
  sudo apt-get install open-iscsi
  ```

  * Redhat variants<br>
  ```
  sud yum in stall iscsi-initiator-utils
  ```

- SolidFire Flocker Plugin
  ```
  pip install solidfire-flocker-driver
  ```
   * or<br>

   ```
   git clone https://github.com/solidfire/solidfire-flocker-driver
   cd solidfire-flocker-driver
   sudo python ./setup.py install
   ```
## Configuration
After install, this plugin reads configuration information on each Flocker node
via the /etc/flocker/agent.yml config file.  Note that you will want to use the
same backend entries on each Flocker node.  Below is an example configuration:

```
version: 1
control-service:
    hostname: "192.168.33.10"
dataset:
    backend: "solidfire_flocker_driver"
    endpoint: "https://admin:admin@192.168.160.3:443/json-rpc/7.0"
    profiles: "{'Gold':{'minIOPS': 10000, 'maxIOPS': 15000, 'burstIOPS': 20000},
                'Silver':{'minIOPS': 5000, 'maxIOPS': 10000, 'burstIOPS': 15000},
                'Bronze':{'minIOPS': 1000, 'maxIOPS': 5000, 'burstIOPS': 10000}}"
```

There are also additional optional values that can be specified in case of
using VLAN's for your SVIP, or explicitly providing initiator names:

```
version: 1
control-service:
    hostname: "192.168.33.10"
dataset:
    backend: "solidfire_flocker_driver"
    endpoint: "https://admin:admin@192.168.160.3:443/json-rpc/7.0"
    profiles: "{'Gold':{'minIOPS': 10000, 'maxIOPS': 15000, 'burstIOPS': 20000},
                'Silver':{'minIOPS': 5000, 'maxIOPS': 10000, 'burstIOPS': 15000},
                'Bronze':{'minIOPS': 1000, 'maxIOPS': 5000, 'burstIOPS': 10000}}"
    initiator_name: "iqn.1993-08.org.debian:01:d7e03b6fc8fd"
    svip: "10.10.10.10"

```

Note the format of the endpoint is https://<login>:<password>@<mvip>/json-rpc/<element-version>

Profiles are used to set desired QoS of Volumes via Flockers Storage Profiles.  Modify the IOP
values as desired, however the key names are required.

Currenlty the SolidFire Flocker plugin utilizes Volume Access Groups for tenancy.  It's required
that you create a specific Voume Access Group on the SolidFire Cluster for Flocker, and assign
the initiator IQN of each Flocker Node to the VAG prior to attempting to provision Volumes with
Flocker. The vag_id setting show above would be the SolidFire ID of the Flocker VAG that you
create.

Licensing
---------
Copyright [2015] [SolidFire Inc]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
-------
Please file bugs and issues at the Github issues page. For Flocker specific questions/issues contact the Flocker team at <a href="https://groups.google.com/forum/#!forum/flocker-users">Google Groups</a>. The code and documentation in this module are released with no warranties or SLAs and are intended to be supported via the Open Source community.

#    Copyright 2015 SolidFire Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""SolidFire Plugin for Flocker."""

from solidfire_flocker_driver import solidfire_driver
from flocker import node


DRIVER_NAME = u"solidfire_flocker_driver"


def api_factory(cluster_id, **kwargs):
    kwargs['cluster_id'] = cluster_id
    return solidfire_driver.initialize_driver(
        **kwargs)

FLOCKER_BACKEND = node.BackendDescription(
    name=DRIVER_NAME,
    needs_reactor=False,
    needs_cluster_id=True,  # My understanding is this is always True?
    api_factory=api_factory,
    deployer_type=node.DeployerType.block)

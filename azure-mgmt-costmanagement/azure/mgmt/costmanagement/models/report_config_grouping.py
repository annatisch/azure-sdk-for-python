# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ReportConfigGrouping(Model):
    """The group by expression to be used in the report.

    All required parameters must be populated in order to send to Azure.

    :param type: Required. Has type of the column to group. Possible values
     include: 'Tag', 'Dimension'
    :type type: str or
     ~azure.mgmt.costmanagement.models.ReportConfigColumnType
    :param name: Required. The name of the column to group. This version
     supports subscription lowest possible grain.
    :type name: str
    """

    _validation = {
        'type': {'required': True},
        'name': {'required': True},
    }

    _attribute_map = {
        'type': {'key': 'type', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(ReportConfigGrouping, self).__init__(**kwargs)
        self.type = kwargs.get('type', None)
        self.name = kwargs.get('name', None)

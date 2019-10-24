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

from azure.core import PipelineClient
from msrest import Serializer, Deserializer

from ._configuration import AzureFileStorageConfiguration
from azure.core.exceptions import map_error
from .operations import ServiceOperations
from .operations import ShareOperations
from .operations import DirectoryOperations
from .operations import FileOperations
from . import models


class AzureFileStorage(object):
    """AzureFileStorage


    :ivar service: Service operations
    :vartype service: azure.storage.fileshare._generated.operations.ServiceOperations
    :ivar share: Share operations
    :vartype share: azure.storage.fileshare._generated.operations.ShareOperations
    :ivar directory: Directory operations
    :vartype directory: azure.storage.fileshare._generated.operations.DirectoryOperations
    :ivar file: File operations
    :vartype file: azure.storage.fileshare._generated.operations.FileOperations

    :param version: Specifies the version of the operation to use for this
     request.
    :type version: str
    :param url: The URL of the service account, share, directory or file that
     is the target of the desired operation.
    :type url: str
    """

    def __init__(self, version, url, **kwargs):

        base_url = '{url}'
        self._config = AzureFileStorageConfiguration(version, url, **kwargs)
        self._client = PipelineClient(base_url=base_url, config=self._config, **kwargs)

        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self.api_version = '2019-02-02'
        self._serialize = Serializer(client_models)
        self._deserialize = Deserializer(client_models)

        self.service = ServiceOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.share = ShareOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.directory = DirectoryOperations(
            self._client, self._config, self._serialize, self._deserialize)
        self.file = FileOperations(
            self._client, self._config, self._serialize, self._deserialize)

    def __enter__(self):
        self._client.__enter__()
        return self
    def __exit__(self, *exc_details):
        self._client.__exit__(*exc_details)

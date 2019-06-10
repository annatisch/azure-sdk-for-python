# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

__version__ = "3.0.0a8"

from .common import BlobType, StorageErrorCode
from .blob_client import BlobClient
from .container_client import ContainerClient
from .blob_service_client import BlobServiceClient
from .lease import LeaseClient
from .authentication import SharedKeyCredentials


__all__ = [
    'BlobServiceClient',
    'ContainerClient',
    'BlobClient',
    'BlobType',
    'LeaseClient',
    'SharedKeyCredentials',
    'StorageErrorCode'
]

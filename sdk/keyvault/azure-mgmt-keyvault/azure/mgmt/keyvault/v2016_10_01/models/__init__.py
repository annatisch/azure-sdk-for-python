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

try:
    from ._models_py3 import AccessPolicyEntry
    from ._models_py3 import CheckNameAvailabilityResult
    from ._models_py3 import DeletedVault
    from ._models_py3 import DeletedVaultProperties
    from ._models_py3 import LogSpecification
    from ._models_py3 import Operation
    from ._models_py3 import OperationDisplay
    from ._models_py3 import Permissions
    from ._models_py3 import Resource
    from ._models_py3 import ServiceSpecification
    from ._models_py3 import Sku
    from ._models_py3 import Vault
    from ._models_py3 import VaultAccessPolicyParameters
    from ._models_py3 import VaultAccessPolicyProperties
    from ._models_py3 import VaultCheckNameAvailabilityParameters
    from ._models_py3 import VaultCreateOrUpdateParameters
    from ._models_py3 import VaultPatchParameters
    from ._models_py3 import VaultPatchProperties
    from ._models_py3 import VaultProperties
except (SyntaxError, ImportError):
    from ._models import AccessPolicyEntry
    from ._models import CheckNameAvailabilityResult
    from ._models import DeletedVault
    from ._models import DeletedVaultProperties
    from ._models import LogSpecification
    from ._models import Operation
    from ._models import OperationDisplay
    from ._models import Permissions
    from ._models import Resource
    from ._models import ServiceSpecification
    from ._models import Sku
    from ._models import Vault
    from ._models import VaultAccessPolicyParameters
    from ._models import VaultAccessPolicyProperties
    from ._models import VaultCheckNameAvailabilityParameters
    from ._models import VaultCreateOrUpdateParameters
    from ._models import VaultPatchParameters
    from ._models import VaultPatchProperties
    from ._models import VaultProperties
from ._paged_models import DeletedVaultPaged
from ._paged_models import OperationPaged
from ._paged_models import ResourcePaged
from ._paged_models import VaultPaged
from ._key_vault_management_client_enums import (
    SkuName,
    KeyPermissions,
    SecretPermissions,
    CertificatePermissions,
    StoragePermissions,
    CreateMode,
    Reason,
    AccessPolicyUpdateKind,
)

__all__ = [
    'AccessPolicyEntry',
    'CheckNameAvailabilityResult',
    'DeletedVault',
    'DeletedVaultProperties',
    'LogSpecification',
    'Operation',
    'OperationDisplay',
    'Permissions',
    'Resource',
    'ServiceSpecification',
    'Sku',
    'Vault',
    'VaultAccessPolicyParameters',
    'VaultAccessPolicyProperties',
    'VaultCheckNameAvailabilityParameters',
    'VaultCreateOrUpdateParameters',
    'VaultPatchParameters',
    'VaultPatchProperties',
    'VaultProperties',
    'VaultPaged',
    'DeletedVaultPaged',
    'ResourcePaged',
    'OperationPaged',
    'SkuName',
    'KeyPermissions',
    'SecretPermissions',
    'CertificatePermissions',
    'StoragePermissions',
    'CreateMode',
    'Reason',
    'AccessPolicyUpdateKind',
]

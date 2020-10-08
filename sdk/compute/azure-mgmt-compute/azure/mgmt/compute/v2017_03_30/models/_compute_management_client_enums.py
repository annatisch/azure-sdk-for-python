# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is regenerated.
# --------------------------------------------------------------------------

from enum import Enum, EnumMeta
from six import with_metaclass

class _CaseInsensitiveEnumMeta(EnumMeta):
    def __getitem__(self, name):
        return super().__getitem__(name.upper())

    def __getattr__(cls, name):
        """Return the enum member matching `name`
        We use __getattr__ instead of descriptors or inserting into the enum
        class' __dict__ in order to support `name` and `value` being both
        properties for enum members (which live in the class' __dict__) and
        enum members themselves.
        """
        try:
            return cls._member_map_[name.upper()]
        except KeyError:
            raise AttributeError(name)


class AccessLevel(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):

    NONE = "None"
    READ = "Read"

class CachingTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the caching requirements. :code:`<br>`:code:`<br>` Possible values are:
    :code:`<br>`:code:`<br>` **None** :code:`<br>`:code:`<br>` **ReadOnly**
    :code:`<br>`:code:`<br>` **ReadWrite** :code:`<br>`:code:`<br>` Default: **None for Standard
    storage. ReadOnly for Premium storage**
    """

    NONE = "None"
    READ_ONLY = "ReadOnly"
    READ_WRITE = "ReadWrite"

class DiskCreateOption(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """This enumerates the possible sources of a disk's creation.
    """

    EMPTY = "Empty"
    ATTACH = "Attach"
    FROM_IMAGE = "FromImage"
    IMPORT_ENUM = "Import"
    COPY = "Copy"

class DiskCreateOptionTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies how the virtual machine should be created.:code:`<br>`:code:`<br>` Possible values
    are::code:`<br>`:code:`<br>` **Attach** \u2013 This value is used when you are using a
    specialized disk to create the virtual machine.:code:`<br>`:code:`<br>` **FromImage** \u2013
    This value is used when you are using an image to create the virtual machine. If you are using
    a platform image, you also use the imageReference element described above. If you are using a
    marketplace image, you  also use the plan element previously described.
    """

    FROM_IMAGE = "FromImage"
    EMPTY = "Empty"
    ATTACH = "Attach"

class IPVersion(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Available from Api-Version 2017-03-30 onwards, it represents whether the specific
    ipconfiguration is IPv4 or IPv6. Default is taken as IPv4.  Possible values are: 'IPv4' and
    'IPv6'.
    """

    I_PV4 = "IPv4"
    I_PV6 = "IPv6"

class MaintenanceOperationResultCodeTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The Last Maintenance Operation Result Code.
    """

    NONE = "None"
    RETRY_LATER = "RetryLater"
    MAINTENANCE_ABORTED = "MaintenanceAborted"
    MAINTENANCE_COMPLETED = "MaintenanceCompleted"

class OperatingSystemStateTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The OS State.
    """

    GENERALIZED = "Generalized"
    SPECIALIZED = "Specialized"

class OperatingSystemTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The operating system of the osDiskImage.
    """

    WINDOWS = "Windows"
    LINUX = "Linux"

class ProtocolTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the protocol of listener. :code:`<br>`:code:`<br>` Possible values are: :code:`<br>`\
    **http** :code:`<br>`:code:`<br>` **https**
    """

    HTTP = "Http"
    HTTPS = "Https"

class ResourceSkuCapacityScaleType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The scale type applicable to the sku.
    """

    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    NONE = "None"

class ResourceSkuRestrictionsReasonCode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The reason for restriction.
    """

    QUOTA_ID = "QuotaId"
    NOT_AVAILABLE_FOR_SUBSCRIPTION = "NotAvailableForSubscription"

class RollingUpgradeActionType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The last action performed on the rolling upgrade.
    """

    START = "Start"
    CANCEL = "Cancel"

class RollingUpgradeStatusCode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Code indicating the current status of the upgrade.
    """

    ROLLING_FORWARD = "RollingForward"
    CANCELLED = "Cancelled"
    COMPLETED = "Completed"
    FAULTED = "Faulted"

class SettingNames(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the name of the setting to which the content applies. Possible values are:
    FirstLogonCommands and AutoLogon.
    """

    AUTO_LOGON = "AutoLogon"
    FIRST_LOGON_COMMANDS = "FirstLogonCommands"

class StatusLevelTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The level code.
    """

    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"

class StorageAccountTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the storage account type for the managed disk. Possible values are: Standard_LRS or
    Premium_LRS. NOTE: Managed OS disk storage account type can only be set when you create the
    scale set.
    """

    STANDARD_LRS = "Standard_LRS"
    PREMIUM_LRS = "Premium_LRS"

class UpgradeMode(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the mode of an upgrade to virtual machines in the scale set.:code:`<br />`:code:`<br
    />` Possible values are::code:`<br />`:code:`<br />` **Manual** - You  control the application
    of updates to virtual machines in the scale set. You do this by using the manualUpgrade
    action.:code:`<br />`:code:`<br />` **Automatic** - All virtual machines in the scale set are
    automatically updated at the same time.
    """

    AUTOMATIC = "Automatic"
    MANUAL = "Manual"
    ROLLING = "Rolling"

class VirtualMachineScaleSetSkuScaleType(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """The scale type applicable to the sku.
    """

    AUTOMATIC = "Automatic"
    NONE = "None"

class VirtualMachineSizeTypes(with_metaclass(_CaseInsensitiveEnumMeta, str, Enum)):
    """Specifies the size of the virtual machine. For more information about virtual machine sizes,
    see `Sizes for virtual machines <https://docs.microsoft.com/azure/virtual-machines/virtual-
    machines-windows-sizes?toc=%2fazure%2fvirtual-machines%2fwindows%2ftoc.json>`_.
    :code:`<br>`:code:`<br>` The available VM sizes depend on region and availability set. For a
    list of available sizes use these APIs:  :code:`<br>`:code:`<br>` `List all available virtual
    machine sizes in an availability set
    <https://docs.microsoft.com/rest/api/compute/availabilitysets/listavailablesizes>`_
    :code:`<br>`:code:`<br>` `List all available virtual machine sizes in a region
    <https://docs.microsoft.com/rest/api/compute/virtualmachinesizes/list>`_
    :code:`<br>`:code:`<br>` `List all available virtual machine sizes for resizing
    <https://docs.microsoft.com/rest/api/compute/virtualmachines/listavailablesizes>`_
    """

    BASIC_A0 = "Basic_A0"
    BASIC_A1 = "Basic_A1"
    BASIC_A2 = "Basic_A2"
    BASIC_A3 = "Basic_A3"
    BASIC_A4 = "Basic_A4"
    STANDARD_A0 = "Standard_A0"
    STANDARD_A1 = "Standard_A1"
    STANDARD_A2 = "Standard_A2"
    STANDARD_A3 = "Standard_A3"
    STANDARD_A4 = "Standard_A4"
    STANDARD_A5 = "Standard_A5"
    STANDARD_A6 = "Standard_A6"
    STANDARD_A7 = "Standard_A7"
    STANDARD_A8 = "Standard_A8"
    STANDARD_A9 = "Standard_A9"
    STANDARD_A10 = "Standard_A10"
    STANDARD_A11 = "Standard_A11"
    STANDARD_A1_V2 = "Standard_A1_v2"
    STANDARD_A2_V2 = "Standard_A2_v2"
    STANDARD_A4_V2 = "Standard_A4_v2"
    STANDARD_A8_V2 = "Standard_A8_v2"
    STANDARD_A2_M_V2 = "Standard_A2m_v2"
    STANDARD_A4_M_V2 = "Standard_A4m_v2"
    STANDARD_A8_M_V2 = "Standard_A8m_v2"
    STANDARD_D1 = "Standard_D1"
    STANDARD_D2 = "Standard_D2"
    STANDARD_D3 = "Standard_D3"
    STANDARD_D4 = "Standard_D4"
    STANDARD_D11 = "Standard_D11"
    STANDARD_D12 = "Standard_D12"
    STANDARD_D13 = "Standard_D13"
    STANDARD_D14 = "Standard_D14"
    STANDARD_D1_V2 = "Standard_D1_v2"
    STANDARD_D2_V2 = "Standard_D2_v2"
    STANDARD_D3_V2 = "Standard_D3_v2"
    STANDARD_D4_V2 = "Standard_D4_v2"
    STANDARD_D5_V2 = "Standard_D5_v2"
    STANDARD_D11_V2 = "Standard_D11_v2"
    STANDARD_D12_V2 = "Standard_D12_v2"
    STANDARD_D13_V2 = "Standard_D13_v2"
    STANDARD_D14_V2 = "Standard_D14_v2"
    STANDARD_D15_V2 = "Standard_D15_v2"
    STANDARD_DS1 = "Standard_DS1"
    STANDARD_DS2 = "Standard_DS2"
    STANDARD_DS3 = "Standard_DS3"
    STANDARD_DS4 = "Standard_DS4"
    STANDARD_DS11 = "Standard_DS11"
    STANDARD_DS12 = "Standard_DS12"
    STANDARD_DS13 = "Standard_DS13"
    STANDARD_DS14 = "Standard_DS14"
    STANDARD_DS1_V2 = "Standard_DS1_v2"
    STANDARD_DS2_V2 = "Standard_DS2_v2"
    STANDARD_DS3_V2 = "Standard_DS3_v2"
    STANDARD_DS4_V2 = "Standard_DS4_v2"
    STANDARD_DS5_V2 = "Standard_DS5_v2"
    STANDARD_DS11_V2 = "Standard_DS11_v2"
    STANDARD_DS12_V2 = "Standard_DS12_v2"
    STANDARD_DS13_V2 = "Standard_DS13_v2"
    STANDARD_DS14_V2 = "Standard_DS14_v2"
    STANDARD_DS15_V2 = "Standard_DS15_v2"
    STANDARD_F1 = "Standard_F1"
    STANDARD_F2 = "Standard_F2"
    STANDARD_F4 = "Standard_F4"
    STANDARD_F8 = "Standard_F8"
    STANDARD_F16 = "Standard_F16"
    STANDARD_F1_S = "Standard_F1s"
    STANDARD_F2_S = "Standard_F2s"
    STANDARD_F4_S = "Standard_F4s"
    STANDARD_F8_S = "Standard_F8s"
    STANDARD_F16_S = "Standard_F16s"
    STANDARD_G1 = "Standard_G1"
    STANDARD_G2 = "Standard_G2"
    STANDARD_G3 = "Standard_G3"
    STANDARD_G4 = "Standard_G4"
    STANDARD_G5 = "Standard_G5"
    STANDARD_GS1 = "Standard_GS1"
    STANDARD_GS2 = "Standard_GS2"
    STANDARD_GS3 = "Standard_GS3"
    STANDARD_GS4 = "Standard_GS4"
    STANDARD_GS5 = "Standard_GS5"
    STANDARD_H8 = "Standard_H8"
    STANDARD_H16 = "Standard_H16"
    STANDARD_H8_M = "Standard_H8m"
    STANDARD_H16_M = "Standard_H16m"
    STANDARD_H16_R = "Standard_H16r"
    STANDARD_H16_MR = "Standard_H16mr"
    STANDARD_L4_S = "Standard_L4s"
    STANDARD_L8_S = "Standard_L8s"
    STANDARD_L16_S = "Standard_L16s"
    STANDARD_L32_S = "Standard_L32s"
    STANDARD_NC6 = "Standard_NC6"
    STANDARD_NC12 = "Standard_NC12"
    STANDARD_NC24 = "Standard_NC24"
    STANDARD_NC24_R = "Standard_NC24r"
    STANDARD_NV6 = "Standard_NV6"
    STANDARD_NV12 = "Standard_NV12"
    STANDARD_NV24 = "Standard_NV24"

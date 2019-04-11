# Azure Storage Python SDK

## Design

The Blob storage API is spread across three clients; each corresponding to the conceptual scope with which a user might wish to engage with the Storage service.
- The service account
- A container
- An individual blob.

It is intended that a user can either navigate the client hierarchy as needed, or instantiate their desired client directly. In addition to this, the basic operations of upload and download can be found at the module level, whereby no client is needed.

The 3-tiered design is intended to separate out the functionality according to common user scenarios. For example, we anticipate the majority of users only using a ContainerClient, to navigate the contents of a container, download blobs and upload new ones. A ContainerClient represents a single container, although its existence is not confirmed until one attempts to run operations on that container.

Account-level operations - including listing the containers within the account - exist on the BlobStorageClient, including creating new containers and deleting them. Creating containers with the BlobStorageClient also provides a simple means of getting a ContainerClient for that container to begin operating within that scope.

Navigating the client hierarchy in this way means that the configured pipeline is shared between clients to accommodate sharing an open connection pool.

Lastly, the BlobClient provides a means of accessing and modifying the particulars of a specific blob. This includes constructing that blob in its type-appropraite steps (e.g. `add_block` with `set_block_ids` for a block blob). A BlobClient is type-aware, and as such this client is intended for people literate in Azure Storage terminology and know exactly what blob types they are working with and how to do so.

While a user may have limited permissions to access the service according to one of these tiers - the operations performed by each client are not exclusively correlated to permissions.


## Module level operations
```python
# Returns a BlobClient
azure.storage.blob.upload_blob(blob_url, data, credentials=None, configuration=None, **kwargs)

# Returns a streamable content iterator
azure.storage.blob.download_blob(blob_url, credentials=None, configuration=None, **kwargs)
```

## BlobStorageClient API
```python
azure.storage.blob.BlobStorageClient(uri, credentials=None, configuration=None)

BlobStorageClient.make_url(container=None, protocol=None, sas_token=None)

BlobStorageClient.generate_shared_access_signature(
    container_name=None, resource_types, permission, expiry, start=None, ip=None, protocol=None)


# Returns dict of account information (SKU and account type)
BlobStorageClient.get_account_information(timeout=None)

# Returns ServiceStats 
BlobStorageClient.get_service_stats(timeout=None)

# Returns ServiceProperties (or dict?)
BlobStorageClient.get_service_properties(timeout=None)

# Returns None
BlobStorageClient.set_service_properties(
    logging=None, hour_metrics=None, minute_metrics=None, cors=None, target_version=None, timeout=None, delete_retention_policy=None, static_website=None)

# Returns a generator of container objects - with names, properties, etc
BlobStorageClient.list_container_properties(
    prefix=None, num_results=None, include_metadata=False, marker=None, timeout=None)

# Returns a ContainerClient
BlobStorageClient.create_container(
    container_name, metadata=None, public_access=None, timeout=None)

# Returns None
BlobStorageClient.delete_container(
    container, snapshot=None, lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a ContainerClient
BlobStorageClient.get_container_client(container, snaphot=None)
```

## ContainerClient API
```python
azure.storage.blob.ContainerClient(
    uri, credentials=None, container_name=None, snapshot=None, configuration=None,
    protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)


ContainerClient.make_url(blob=None, protocol=None, sas_token=None)

ContainerClient.generate_shared_access_signature(
    blob=None, resource_types, permission, expiry, start=None, ip=None, protocol=None)

# Returns a Lease object, that can be run in a context manager
ContainerClient.acquire_lease(
    lease_duration=-1,
    proposed_lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)

# Returns approximate time remaining in the lease period, in seconds
ContainerClient.break_lease(
    lease_break_period=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)

# Returns dict of account information (SKU and account type)
ContainerClient.get_account_infomation(timeout=None)

# Returns ContainerProperties
ContainerClient.get_container_properties(container, lease=None, timeout=None)

# Returns metadata as dict
ContainerClient.get_container_metadata(container, lease=None, timeout=None)

# Returns container-updated property dict (Etag and last modified)
ContainerClient.set_container_metadata(container, metadata=None, lease=None, if_modified_since=None, timeout=None)

# Returns access policies as a dict
ContainerClient.get_container_acl(container, lease=None, timeout=None)

# Returns container-updated property dict (Etag and last modified)
ContainerClient.set_container_acl(
    container, signed_identifiers=None, public_access=None lease=None, if_modified_since=None, if_unmodified_since=None, timeout=None)

# Returns a iterable (auto-paging) response of BlobProperties
ContainerClient.list_blob_properties(prefix=None, include=None, timeout=None)

# Returns a generator that honors directory hierarchy 
ContainerClient.walk_blob_propertes(prefix=None, include=None, delimiter="/", timeout=None)

# Blob type enum
azure.storage.blob.BlobType.BlockBlob
azure.storage.blob.BlobType.PageBlob
azure.storage.blob.BlobType.AppendBlob

# By default, uploads as a BlockBlob, unless alternative blob_type is specified.
# Returns a BlobClient
ContainerClient.upload(
    blob,
    data=None,
    length=None,
    blob_type=BlobType.BlockBlob,
    metadata=None,
    content_settings=None,
    validate_content=False,
    lease=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None,
    timeout=None,
    premium_page_blob_tier=None,  # Page only
    sequence_number=None  # Page only
    maxsize_condition=None,  # Append only
    appendpos_condition=None)  # Append only

# Returns a data generator (stream)
ContainerClient.download(
    blob, snapshot=None, offset=None, length=None, validate_content=False, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a pollable object to check operation status and abort
ContainerClient.copy_blob(
    blob, copy_source,
    metadata=None,
    source_if_modified_since=None,
    source_if_unmodified_since=None,
    source_if_match=None,
    source_if_none_match=None,
    destination_if_modified_since=None,
    destination_if_unmodified_since=None,
    destination_if_match=None,
    destination_if_none_match=None,
    destination_lease=None,
    source_lease=None,
    timeout=None,
    premium_page_blob_tier=None,  # Page only
    requires_sync=None)  # Block only

# Returns None
ContainerClient.delete_blob(
    blob, snapshot=None, lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns None
ContainerClient.undelete_blob(blob, timeout=None)

# Returns a BlobClient
ContainerClient.get_blob_client(blob, blob_type, snapshot=None)
```

## BlobClient API
```python
azure.storage.blob.BlobClient(
    uri, blob_type, credentials=None, container_name=None, blob_name=None, snapshot=None, configuration=None)


ContainerClient.make_url(protocol=None, sas_token=None)

ContainerClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)


# Returns BlobProperties
BlobClient.get_blob_properties(
    lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_blob_properties(
    content_settings=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a dict of metadata
BlobClient.get_blob_metadata(
    lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_blob_metadata(
    metadata=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns snapshot properties
BlobClient.create_snapshot(
    metadata=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, lease=None, timeout=None)

# Returns None
BlobClient.set_tier(blob_tier, timeout=None)

# Returns a Lease object, that can be run in a context manager
BlobClient.acquire_lease(
    lease_duration=-1,
    proposed_lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)

# Returns approximate time remaining in the lease period, in seconds
BlobClient.break_lease(
    lease_break_period=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)

# Only works where type is BlobBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.add_block(
    data, block_id, validate_content=False, lease=None, timeout=None)

# Only works where type is BlobBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.add_block_from_url(
    copy_source_url, source_range_start, source_range_end, block_id, source_content_md5=None, lease=None, timeout=None)

# Only works where type is BlobBlob, otherwise raises InvalidOperation
# Returns a tuple of two sets - committed and uncommitted blocks
BlobClient.get_block_ids(
    blob, block_list_type=None, snapshot=None, lease=None, timeout=None)

# Only works where type is BlobBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_block_ids(
    blob, block_list, lease=None, content_settings=None, metadata=None, validate_content=False, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.create_pageblob(
    content_length, content_settings=None, sequence_number=None, metadata=None, lease_id=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None, premium_page_blob_tier=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns a list of page ranges
BlobClient.get_page_ranges(
    blob, start_range=None, end_range=None, snapshot=None, lease=None, previous_snapshot_diff=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_sequence_number(
    blob, sequence_number_action, sequence_number=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.resize_blob(
    blob, content_length, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.update_page(
    blob, page, start_range, end_range, lease=None, validate_content=False, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.clear_page(
    blob, start_range, end_range, lease=None, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns a pollable object to check operation status and abort
BlobClient.incremental_copy(
    blob, copy_source, metadata=None, destination_if_modified_since=None, destination_if_unmodified_since=None, destination_if_match=None, destination_if_none_match=None, destination_lease=None, source_lease=None, timeout=None):

# Only works where type is AppendBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.create_appendblob(
    content_settings=None, metadata=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is AppendBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag, last modified, append offset, committed block count)
BlobClient.append_block(
    blob, data, validate_content=False, maxsize_condition=None, appendpos_condition=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)
```

## Lease
```python
BlobStorageLease.renew(
    if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobStorageLease.release(if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobStorageLease.change(
    proposed_lease_id, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

#### Samples

container = ContainerClient(...)

lease = container.aquire_lease('my_container'):
properties = client.get_properties(lease=lease)
lease.release()

with container.aquire_lease() as lease:
    downdload = container.download('test_data', lease=lease)
    for data in download:
        file_handle.write(data)
        lease.renew()
    # Lease is released on exiting the context

```

## Scenarios

### Upload/download blob via ContainerClient
```python
from azure.storage.blob import ContainerClient

creds = SharedKeyCredentials(account_name, acocunt_key)
container_client = ContainerClient(account_url, container_name, credentials=creds)

# Upload block blob to container, returns a BlobCient for that blob
blob_client = container_client.upload("test-data", upload_data)

# Upload page blob to container, returns a BlobCient for that blob
blob_client = container_client.upload("test-data", upload_data, blob_type=BlobType.PageBlob)

# Upload append blob to container, returns a BlobCient for that blob
blob_client = container_client.upload("test-data", upload_data, blob_type=BlobType.AppendBlob)

# Download blob from container, returns a BlobCient for that blob
handle = container_client.download("test-data")

# Consume data and write to file
with open(output_file, 'wb') as output_data:
    for data in handle:
        output_data.write(data)
```

### Upload/download blob via BlobStorageClient
```python
from azure.storage.blob import BlobStorageClient, BlobType


storage_client = BlobStorageClient.from_url(storage_url, credentials=None, configuration=None)
container_client = storage_client.get_container_client("my-container")

# Upload block blob to container
container_client.upload("test-data", upload_data)

```

### Enumerate blobs in a container
```python
from azure.storage.blob import BlobStorageClient, SharedKeyCredentials

creds = SharedKeyCredentials(account_name, acocunt_key)
storage_client = BlobStorageCient(account_name, credentials=creds)

container_client = storage_client.get_container_client('my-container')

for blob in container_client.list_blob_properties(prefix='/test'):
    print(blob.metadata)

for blob in container_client.walk_blob_properties():
    try:
        print(blob.metadata)
    except AttributeError:
        print(list(blob))
```

### Manage containers
```python
from azure.storage.blob import BlobStorageClient

creds = SharedKeyCredentials(account_name, acocunt_key)
storage_client = BlobStorageCient(account_url, credentials=creds)

try:
    container_client = storage_client.get_container_client('my-container')
    container_client.upload("blob_name", upload_data)
except ResourceNotFound:
    container_client = storage_client.create_container('my-container')
    container_client.upload("blob_name", upload_data)


for container in storage_client.list_container_properties():
    storage_client.delete_container(container)
```

### Working directly with a blob URL
```python
blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

# Upload to a blob
from azure.core.storage.blob import upload_blob
with open('my_file.txt', rb) as upload_data:
    upload_blob(blob_url, upload_data)

# Download a blob
from azure.core.storage.blob import download_blob
with open('my_file.txt', rb) as download_data:
    for data in download_blob(blob_url):
        download_data.write(data)
```
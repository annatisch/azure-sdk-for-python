# Azure Storage Python SDK


## BlobStorageClient API
```python
azure.storage.blob.BlobStorageClient(
    account_name, credentials, configuration=None, protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)

azure.storage.blob.BlobStorageClient.from_connection_string(
    conn_str, configuration=None)

azure.storage.blob.BlobStorageClient.from_url(
    account_url, configuration=None)


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
BlobStorageClient.list_containers(
    prefix=None, num_results=None, include_metadata=False, marker=None, timeout=None)

# Returns None
BlobStorageClient.create_container(
    container_name, metadata=None, public_access=None, timeout=None)

# Returns ContainerProperties
BlobStorageClient.get_container_properties(container, lease=None, timeout=None)

# Returns metadata as dict
BlobStorageClient.get_container_metadata(container, lease=None, timeout=None)

# Returns container-updated property dict (Etag and last modified)
BlobStorageClient.set_container_metadata(container, metadata=None, lease=None, if_modified_since=None, timeout=None)

# Returns access policies as a dict
BlobStorageClient.get_container_acl(container, lease=None, timeout=None)

# Returns container-updated property dict (Etag and last modified)
BlobStorageClient.set_container_acl(
    container, signed_identifiers=None, public_access=None lease=None, if_modified_since=None, if_unmodified_since=None, timeout=None)

# Returns None
BlobStorageClient.delete_container(
    container, snapshot=None, lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a Lease object, that can be run in a context manager
BlobStorageClient.acquire_lease(
    container,
    lease_duration=-1,
    proposed_lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)

# Returns a ContainerClient
BlobStorageClient.get_container(container, lease=None, timeout=None)
```

## ContainerClient API
```python
azure.storage.blob.ContainerClient(
    account_name, credentials, container_name, lease=None, configuration=None,
    protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)

azure.storage.blob.ContainerClient.from_url(
    url, credentials=None, configuration=None)

azure.storage.blob.ContainerClient.from_connection_string(
    conn_str, container_name, configuration=None)


ContainerClient.make_url(blob_name=None, protocol=None, sas_token=None)

ContainerClient.generate_shared_access_signature(
    blob_name=None, resource_types, permission, expiry, start=None, ip=None, protocol=None)


# Returns dict of account information (SKU and account type)
ContainerClient.get_account_infomation(timeout=None)

# Returns BlobProperties (or dict?)
ContainerClient.get_blob_properties(
    blob_name, snapshot=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.set_blob_properties(
    blob_name, content_settings=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a dict of metadata
ContainerClient.get_blob_metadata(
    blob_name, snapshot=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.set_blob_metadata(
    blob_name, metadata=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a iterable (auto-paging) response of BlobProperties
ContainerClient.list_blobs(
    prefix=None, num_results=None, include=None, delimiter=None, marker=None, timeout=None)


# Blob type enum
azure.storage.blob.BlobType.BlockBlob
azure.storage.blob.BlobType.PageBlob
azure.storage.blob.BlobType.AppendBlob

# By default, uploads as a BlockBlob, unless alternative blob_type_settings are specified.
ContainerClient.upload(
    blob_name,
    data=None,
    length=None,
    blob_type=BlobType.BlockBlob,
    metadata=None,
    content_settings=None,
    validate_content=False,
    lease_id=None,
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
    blob_name, snapshot=None, start_range=None, end_range=None, validate_content=False, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a pollable object to check operation status and abort
ContainerClient.copy_blob(
    blob_name, copy_source,
    metadata=None,
    source_if_modified_since=None,
    source_if_unmodified_since=None,
    source_if_match=None,
    source_if_none_match=None,
    destination_if_modified_since=None,
    destination_if_unmodified_since=None,
    destination_if_match=None,
    destination_if_none_match=None,
    destination_lease_id=None,
    source_lease_id=None,
    timeout=None,
    premium_page_blob_tier=None,  # Page only
    requires_sync=None)  # Block only

# Returns None
ContainerClient.delete_blob(
    blob_name, snapshot=None, lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns None
ContainerClient.undelete_blob(blob_name, timeout=None)

# Returns snapshot properties
ContainerClient.snapshot_blob(
    blob_name, metadata=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, lease=None, timeout=None)

# Returns None
ContainerClient.set_blob_tier(blob_name, blob_tier, timeout=None)

# Returns a Lease object, that can be run in a context manager
ContainerClient.acquire_blob_lease(
    blob_name,
    lease_duration=-1,
    proposed_lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)


########## Block blob specific operations ##########

# Returns None
ContainerClient.blockblob_add_block(
    blob_name, data, block_id, validate_content=False, lease=None, timeout=None)

# Returns None
ContainerClient.blobblob_add_block_from_url(
    blob_name, copy_source_url, source_range_start, source_range_end, block_id, source_content_md5=None, lease_id=None, timeout=None)

# Returns a tuple of two sets - committed and uncommitted blocks
ContainerClient.blockblob_get_block_ids(
    blob_name, block_list_type=None, snapshot=None, lease=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.blockblob_set_block_ids(
    blob_name, block_list, lease=None, content_settings=None, metadata=None, validate_content=False, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)


########## Page blob specific operations ##########

# Returns a list of page ranges
ContainerClient.pageblob_get_page_ranges(
    blob_name, start_range=None, end_range=None, snapshot=None, lease=None, previous_snapshot_diff=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.pageblob_set_sequence_number(
    blob_name, sequence_number_action, sequence_number=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.pageblob_resize_blob(
    blob_name, content_length, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.pageblob_update_page(
    blob_name, page, start_range, end_range, lease=None, validate_content=False, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns blob-updated property dict (Etag and last modified)
ContainerClient.pageblob_clear_page(
    blob_name, start_range, end_range, lease=None, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns a pollable object to check operation status and abort
ContainerClient.pageblob_incremental_copy(
    blob_name, copy_source, metadata=None, destination_if_modified_since=None, destination_if_unmodified_since=None, destination_if_match=None, destination_if_none_match=None, destination_lease_id=None, source_lease_id=None, timeout=None):


########## Append blob specific operations #########

# Returns blob-updated property dict (Etag, last modified, append offset, committed block count)
ContainerClient.appendblob_append_block(
    blob_name, data, validate_content=False, maxsize_condition=None, appendpos_condition=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)
```

## Lease
```python
BlobStorageLease.renew(
    if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobStorageLease.release(if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobStorageLease.break(
    lease_break_period=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobStorageLease.change(
    proposed_lease_id, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

#### Samples

lease = client.aquire_lease('my_container'):
client.get_container_properties('my_container', lease=lease)

with client.aquire_lease('my_container') as lease:
    container = client.get_container('my_container')
    data = container.download('test_data')  # pass lease implicitly
    lease.renew()

```

## Module level operations
```python
azure.storage.blob.upload_blob(blob_url, data, credentials=None, configuration=None)

azure.storage.blob.download_blob(blob_url, credentials=None, configuration=None)

#### Samples

blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"


upload_blob(blob_url, upload_data)

handle = download_blob(blob_url)
with open(output_file, 'wb') as output_data:
    for data in handle:
        output_data.write(data)
```

## Scenarios

### Upload/download blob via ContainerClient
```python
from azure.storage.blob import ContainerClient

creds = SharedKeyCredentials(account_name, acocunt_key)
client = ContainerClient(account_name, container_name, credentials=creds)

# Upload block blob to container
container.upload("test-data", upload_data)

# Download blob from container
handle = container.download("test-data")

# Consume data and write to file
with open(output_file, 'wb') as output_data:
    for data in handle:
        output_data.write(data)
```

#### Upload/download blob via BlobStorageClient
```python
from azure.storage.blob import BlobStorageClient, BlobType

storage_url = "https://test.blob.core.windows.net/?sv=2018-03-28&ss=b&srt=sco&sp=rwdlac&se=2019-04-04T00:17:18Z&st=2019-04-03T16:17:18Z&spr=https&sig=uJnCwe2fGQpTuiCJMH%2F%2B4PT0rrhS9kkvCEU7c2Gmjs4%3D"

storage = BlobStorageClient.from_url(storage_url, credentials=None, configuration=None)
container = storage.get_container("my-container")

# Upload block blob to container
container.upload("test-data", upload_data)

# Upload page blob to container
container.upload("test-data", upload_data, blob_type=BlobType.PageBlob)

# Upload append blob to container
container.upload("test-data", upload_data, blob_type=BlobType.AppendBlob)

# Download blob from container
handle = container.download("test-data")

# Consume data and write to file
with open(output_file, 'wb') as output_data:
    for data in handle:
        output_data.write(data)
```

### Enumerate blobs in a container
```python
from azure.storage.blob import BlobStorageClient, SharedKeyCredentials

creds = SharedKeyCredentials(account_name, acocunt_key)
client = BlobStorageCient(account_name, credentials=creds)

container = client.get_container('my-container')

for blob in container.list_blobs(prefix='/test'):
    print(blob.metadata)
```

### Manage containers
```python
from azure.storage.blob import BlobStorageClient

creds = SharedKeyCredentials(account_name, acocunt_key)
client = BlobStorageCient(account_name, credentials=creds)

try:
    container = client.get_container('my-container')
except ResourceNotFound:
    client.create_container('my-container')
    container = client.get_container('my-container')

if not client.exists('my-container'):
    client.create_container('my-container')

for container in client.list_containers():
    client.delete_container(container)
```

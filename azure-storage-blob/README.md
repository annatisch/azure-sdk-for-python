# Azure Storage Python SDK


## BlobStorageClient API
```python
azure.storage.blob.BlobStorageClient(
    account_name, credentials, configuration=None, protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)

azure.storage.blob.BlobStorageClient.from_connection_string(
    conn_str, configuration=None)

azure.storage.blob.BlobStorageClient.from_url(
    account_url, configuration=None)

BlobStorageClient.get_account_information(timeout=None)

BlobStorageClient.get_service_stats(timeout=None)

BlobStorageClient.get_service_properties(timeout=None)

BlobStorageClient.set_service_properties(
    logging=None, hour_metrics=None, minute_metrics=None, cors=None, target_version=None, timeout=None, delete_retention_policy=None, static_website=None)

BlobStorageClient.make_url(container=None, protocol=None, sas_token=None)

BlobStorageClient.generate_shared_access_signature(
    container_name=None, resource_types, permission, expiry, start=None, ip=None, protocol=None)

# Returns a generator of container objects - with names, properties, etc
BlobStorageClient.list_containers(
    prefix=None, num_results=None, include_metadata=False, marker=None, timeout=None)

BlobStorageClient.create_container(
    container_name, metadata=None, public_access=None, timeout=None)

BlobStorageClient.get_container_properties(container, lease=None, timeout=None)

BlobStorageClient.get_container_metadata(container, lease=None, timeout=None)

BlobStorageClient.set_container_metadata(container, metadata=None, lease=None, if_modified_since=None, timeout=None)

BlobStorageClient.get_container_acl(container, lease=None, timeout=None)

BlobStorageClient.set_container_acl(
    container, signed_identifiers=None, public_access=None lease=None, if_modified_since=None, if_unmodified_since=None, timeout=None)

BlobStorageClient.exists(
    container_name, blob_name=None, snapshot=None, timeout=None)

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

```

## ContainerClient API
```python
azure.storage.blob.ContainerClient(
    account_name, credentials, container_name, configuration=None,
    protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)

azure.storage.blob.ContainerClient.from_url(
    url, credentials=None, configuration=None)

azure.storage.blob.ContainerClient.from_connection_string(
    conn_str, container_name, configuration=None)


ContainerClient.make_url(blob_name=None, protocol=None, sas_token=None)

ContainerClient.generate_shared_access_signature(
    blob_name=None, resource_types, permission, expiry, start=None, ip=None, protocol=None)

ContainerClient.get_account_infomation(timeout=None)

ContainerClient.get_blob_properties(
    blob_name, snapshot=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

ContainerClient.set_blob_properties(
    blob_name, content_settings=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

ContainerClient.get_blob_metadata(
    blob_name, snapshot=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

ContainerClient.set_blob_metadata(
    blob_name, metadata=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

ContainerClient.list_blobs(
    prefix=None, num_results=None, include=None, delimiter=None, marker=None, timeout=None)

# By default, uploads as a BlockBlob, unless alternative blob_type_settings are specified.
# Returns a blob client according to type.
ContainerClient.upload(
    blob_name,
    data=None,
    length=None,
    blob_type=None,
    metadata=None,
    content_settings=None,
    validate_content=False,
    lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None,
    timeout=None)

# Returns a data generator.
ContainerClient.download(
    blob_name, snapshot=None, start_range=None, end_range=None, validate_content=False, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

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
    incremental=False,  # Page only
    premium_page_blob_tier=None,  # Page only
    requires_sync=None)  # Block blob only

BlobStorageAccount.delete_blob(
    blob_name, snapshot=None, lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

ContainerClient.snapshot_blob(
    blob_name, metadata=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, lease=None, timeout=None)

ContainerClient.set_blob_tier(blob_name, blob_tier, timeout=None)

# Returns a Lease object, that can be run in a context manager
ContainerClient.acquire_lease(
    blob_name,
    lease_duration=-1,
    proposed_lease_id=None,
    if_modified_since=None,
    if_unmodified_since=None,
    if_match=None,
    if_none_match=None, timeout=None)



## Blob type settings

azure.storage.blob.BlobType.BlockBlob
azure.storage.blob.BlobType.PageBlob
azure.storage.blob.BlobType.AppendBlob

azure.storage.blob.BlockOption(block_id)
azure.storage.blob.AppendBlobOptions(maxsize_condition=None, appendpos_condition=None)
azure.storage.blob.PageBlobOptions(premium_page_blob_tier=None, sequence_number=None)

## Blob type clients

### Common
azure.storage.blob.BlobClient(
    account_name, credentials, container_name, blob_name, snapshot=None, lease=None, configuration=None,
    protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)

azure.storage.blob.BlobClient.from_url(
    url, credentials=None, configuration=None)

azure.storage.blob.BlobClient.from_connection_string(
    conn_str, container_name, blob_name, configuration=None)

BlobClient.download(
    start_range=None, end_range=None, validate_content=False, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobClient.get_properties(
    blob_name, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobClient.set_properties(
    blob_name, content_settings=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobClient.get_metadata(
    blob_name, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

BlobClient.set_metadata(
    blob_name, metadata=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

### BlockBlobClient
BlockBlobClient.add_block(
    data, block_id, validate_content=False, timeout=None)

BlockBlobClient.get_block_ids(
    block_list_type=None, timeout=None)

BlockBlobClient.set_block_ids(
    block_list, content_settings=None, metadata=None, validate_content=False, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)


### PageBlobClient
PageBlobClient.get_page_ranges(start_range=None, end_range=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

PageBlobClient.get_page_ranges_diff(
    previous_snapshot, start_range=None, end_range=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

PageBlobClient.set_sequence_number(
    sequence_number_action, sequence_number=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

PageBlobClient.resize_blob(content_length, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

PageBlobClient.update_page(
    page, start_range, end_range, validate_content=False, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

PageBlobClient.clear_page(
    start_range, end_range, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

### AppendBlobClient
AppendBlobClient.append_block(
    data, validate_content=False, maxsize_condition=None, appendpos_condition=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)


## Lease

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
from azure.storage.blob import BlobStorageClient

storage_url = "https://test.blob.core.windows.net/?sv=2018-03-28&ss=b&srt=sco&sp=rwdlac&se=2019-04-04T00:17:18Z&st=2019-04-03T16:17:18Z&spr=https&sig=uJnCwe2fGQpTuiCJMH%2F%2B4PT0rrhS9kkvCEU7c2Gmjs4%3D"

storage = BlobStorageClient.from_url(storage_url, credentials=None, configuration=None)
container = storage.get_container("my-container")

# Upload block blob to container
container.upload("test-data", upload_data)

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
client = BlobStorageCient(account_name, account_key, credentials=creds)

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

### Upload/download directly with a blob SAS URL with write permissions (no client required).
```python
from azure.storage.blob import upload_blob, download_blob

blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"


upload_blob(blob_url, upload_data, credentials=None, configuration=None)

handle = download_blob(blob_url, credentials=None, configuration=None)

with open(output_file, 'wb') as output_data:
    for data in handle:
        output_data.write(data)
```
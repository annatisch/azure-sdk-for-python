# Azure Storage Python SDK

## Design

The Blob storage API is spread across three clients; each corresponding to the conceptual scope with which a user might wish to engage with the Storage service.
- The service account
- A container
- An individual blob.

It is intended that a user can either navigate the client hierarchy as needed, or instantiate their desired client directly. In addition to this, the basic operations of upload and download can be found at the module level, whereby no client is needed.

The 3-tiered design is intended to separate out the functionality according to common user scenarios. For example, we anticipate the majority of users only using a ContainerClient, to navigate the contents of a container, download blobs and upload new ones. A ContainerClient represents a single container, although its existence is not confirmed until one attempts to run operations on that container.

Account-level operations - including listing the containers within the account - exist on the BlobServiceClient, including creating new containers and deleting them. Creating containers with the BlobServiceClient also provides a simple means of getting a ContainerClient for that container to begin operating within that scope.

Navigating the client hierarchy in this way means that the configured pipeline is shared between clients to accommodate sharing an open connection pool.

Lastly, the BlobClient provides a means of accessing and modifying the particulars of a specific blob. This includes constructing that blob in its type-appropraite steps (e.g. `add_block` with `set_block_ids` for a block blob). A BlobClient is type-aware, and as such this client is intended for people literate in Azure Storage terminology and know exactly what blob types they are working with and how to do so.

While a user may have limited permissions to access the service according to one of these tiers - the operations performed by each client are not exclusively correlated to permissions.


## Module level operations
```python
# Returns a BlobClient
azure.storage.blob.upload_blob(blob_url, data, block_size=2046, concurrent_threads=1, credentials=None, configuration=None, **kwargs)

# Returns a streamable content iterator
azure.storage.blob.download_blob(blob_url, block_size=2046, concurrent_threads=1, credentials=None, configuration=None, **kwargs)
```

## BlobServiceClient API
```python
azure.storage.blob.BlobServiceClient(uri, credentials=None, configuration=None)

BlobServiceClient.make_url(protocol=None, sas_token=None)

BlobServiceClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)


# Returns dict of account information (SKU and account type)
BlobServiceClient.get_account_information(timeout=None)

# Returns ServiceStats 
BlobServiceClient.get_service_stats(timeout=None)

# Returns ServiceProperties (or dict?)
BlobServiceClient.get_service_properties(timeout=None)

# Returns None
BlobServiceClient.set_service_properties(
    logging=None, hour_metrics=None, minute_metrics=None, cors=None, target_version=None, timeout=None, delete_retention_policy=None, static_website=None)

# Returns a generator of container objects - with names, properties, etc
BlobServiceClient.list_container_properties(
    prefix=None, num_results=None, include_metadata=False, marker=None, timeout=None)

# Returns a ContainerClient
BlobServiceClient.create_container(
    container, metadata=None, public_access=None, timeout=None)

# Returns a ContainerClient
BlobServiceClient.get_container_client(container, snaphot=None)
```

## ContainerClient API
```python
azure.storage.blob.ContainerClient(
    uri, credentials=None, container_name=None, configuration=None,
    protocol=DEFAULT_PROTOCOL, endpoint_suffix=SERVICE_HOST_BASE, custom_domain=None)


ContainerClient.make_url(protocol=None, sas_token=None)

ContainerClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)

# Returns None
ContainerClient.create_container(
    metadata=None, public_access=None, timeout=None)

# Returns None
ContainerClient.delete_container(
    lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

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


# Returns a BlobClient
ContainerClient.get_blob_client(blob, blob_type, snapshot=None)
```

## BlobClient API
```python
azure.storage.blob.BlobClient(
    uri, blob_type=BlobType.BlockBlob, credentials=None, container_name=None, blob_name=None, snapshot=None, configuration=None)


BlobClient.make_url(protocol=None, sas_token=None)

BlobClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)

# By default, uploads as a BlockBlob, unless alternative blob_type is specified.
# Returns a BlobClient
BlobClient.upload_blob(
    data,
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
BlobClient.download_blob(
    offset=None, length=None, validate_content=False, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns None
BlobClient.delete_blob(
    lease=None, delete_snapshots=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Returns None
BlobClient.undelete_blob(timeout=None)

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

# Returns a pollable object to check operation status and abort
BlobClient.copy_from_source(
    copy_source,
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

# Only works where type is BlockBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.set_standard_blob_tier(standard_blob_tier, timeout=None)

# Only works where type is BlockBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.add_block(
    data, block_id, validate_content=False, lease=None, timeout=None)

# Only works where type is BlockBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.add_block_from_url(
    copy_source_url, source_range_start, source_range_end, block_id, source_content_md5=None, lease=None, timeout=None)

# Only works where type is BlockBlob, otherwise raises InvalidOperation
# Returns a tuple of two sets - committed and uncommitted blocks
BlobClient.get_block_ids(
    block_list_type=None, snapshot=None, lease=None, timeout=None)

# Only works where type is BlockBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_block_ids(
    block_list, lease=None, content_settings=None, metadata=None, validate_content=False, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns None
BlobClient.set_premium_page_blob_tier(premium_page_blob_tier, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.create_pageblob(
    content_length, content_settings=None, sequence_number=None, metadata=None, lease_id=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None, premium_page_blob_tier=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns a list of page ranges
BlobClient.get_page_ranges(
    start_range=None, end_range=None, snapshot=None, lease=None, previous_snapshot_diff=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.set_sequence_number(
    sequence_number_action, sequence_number=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.resize_blob(
    content_length, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.update_page(
    page, start_range, end_range, lease=None, validate_content=False, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.clear_page(
    start_range, end_range, lease=None, if_sequence_number_lte=None, if_sequence_number_lt=None, if_sequence_number_eq=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is PageBlob, otherwise raises InvalidOperation
# Returns a pollable object to check operation status and abort
BlobClient.incremental_copy(
    copy_source, metadata=None, destination_if_modified_since=None, destination_if_unmodified_since=None, destination_if_match=None, destination_if_none_match=None, destination_lease=None, source_lease=None, timeout=None):

# Only works where type is AppendBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag and last modified)
BlobClient.create_appendblob(
    content_settings=None, metadata=None, lease=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)

# Only works where type is AppendBlob, otherwise raises InvalidOperation
# Returns blob-updated property dict (Etag, last modified, append offset, committed block count)
BlobClient.append_block(
    data, validate_content=False, maxsize_condition=None, appendpos_condition=None, if_modified_since=None, if_unmodified_since=None, if_match=None, if_none_match=None, timeout=None)
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

### 1. Given a blob URL, upload data to it.
```python
import azure.storage.blob

blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

with open(upload_file, 'rb') as data:
    azure.storage.blob.upload_blob(blob_url, data, concurrent_threads=10)
```

### 2. Given a blob URL, download data from it.
```python
import azure.storage.blob

blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

with open(download_file, 'wb') as output:
    stream = azure.storage.blob.download_blob(blob_url, concurrent_threads=10)
    for data in stream:
        output.write(data)
```

### 3. Given a blob URL, upload data to the blob with metadata then inspect the properties.
```python
from azure.storage.blob import BlobClient

client = BlobClient(blob_url)

with open(upload_file, 'rb') as data:
    client.upload_blob(data, metadata={"Foo":"Bar"})

properties = client.get_blob_properties()
```

### 4. Given a blob URL, delete it.
```python
from azure.storage.blob import BlobClient

client = BlobClient(blob_url)
client.delete_blob()
```

### 5. Given a storage account, credentials and a container name, create the container and set metadata.
```python
from azure.storage.blob import ContainerClient, SharedKeyCredentials

account_url = "https://test.blob.core.windows.net"
creds = SharedKeyCredentials(...)

client = ContainerClient(account_url, container="my-container", credentials=creds)
container = client.create_container(metadata={"Foo": "Bar"})
```

### 6. Given a container URL, enumerate the blobs in the container.
```python
from azure.storage.blob import ContainerClient

container_url = "https://test.blob.core.windows.net/my-container?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

container_client = ContainerClient(container_url)

for blob in container_client.list_blob_properties(prefix='/test'):
    print(blob.metadata)
```

### 7. Given a storage account, credentials and a container name, list and download all blobs.
```python
from azure.storage.blob import ContainerClient, SharedKeyCredentials

account_url = "https://test.blob.core.windows.net"
creds = SharedKeyCredentials(...)

client = ContainerClient(account_url, container="my-container", credentials=creds)

test_blobs = container_client.list_blob_properties()
for blob in test_blobs:
    blob = container_client.get_blob_client(blob)
    stream = blob.download()
```

### 8. Given a storage account URL, list containers and delete them all.
```python
from azure.storage.blob import BlobSerivceClient

storage_url = "https://test.blob.core.windows.net?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

client = BlobServiceClient(storage_url)

all_containers = client.list_container_properties()
for container in all_containers:
    container_client = client.get_container_client(container)
    container_client.delete_container()
```

### 9. Given a storage account and credentials, create a container then upload data to it.
```python
from azure.storage.blob import BlobServiceClient, SharedKeyCredentials

account_url = "https://test.blob.core.windows.net"
creds = SharedKeyCredentials(...)

client = ContainerClient(account_url, credentials=creds)
container = client.create_container("my-container")

for input_file in list_of_file_paths:
    new_blob = client.get_blob_client(input_file)

    with open(input_file, 'rb') as data:
        new_blob.upload_blob(data)
```

### 10. Given a blob URL, take a snapshot and check its properties.
```python
from azure.storage.blob import BlobClient

blob_client = BlobClient(blob_url)
new_snapshot = blob_client.create_snapshot()

snapshot_client = BlobClient(new_snapshot)
snapshot_properties = snapshot_client.get_properties()
```

### 11. Given a block blob URL, replace a block in the blob.
```python
from base64 import b64encode
from urllib.parse import quote

from azure.storage.blob import BlobClient

blob_client = BlobClient(blob_url)
block_id = quote(b64encode(b"NewBlockID"))
blob_client.add_block(b"some data", block_id)
committed, uncommitted = blob_client.get_block_ids(block_type='all')

# Take last uncommitted block and replace the first committed block.
committed[0] = uncommitted[-1]
blob_client.set_block_ids(committed)
```


### 12. Given a blob URL, create a page blob and update its pages
```python
from azure.storage.blob import BlobClient, BlobType

client = BlobClient(blob_url, blob_type=BlobType.PageBlob)
client.create_pageblob(length=20000000)

pages = client.get_page_ranges()
for page in pages:
    client.update_page(upload_data, **page)
```

## Scenarios with alternative flat API

### 1. Given a blob URL, upload data to it.
```python
from azure.storage.blob import BlobServiceClient

blob_url = "https://test.blob.core.windows.net/my-container/my-data?sp=rcwd&st=2019-04-03T16:09:33Z&se=2019-04-04T00:09:33Z&spr=https&sv=2018-03-28&sig=N1pX45xdn1jf8K3upPmxIAGCMx9SceAgfNf8X%2B16aBU%3D&sr=b"

client = BlobServiceclient()
with open(upload_file, 'rb') as data:
    client.upload_blob(blob_url, data)
```

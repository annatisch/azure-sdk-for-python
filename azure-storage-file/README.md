# Azure Storage File Python SDK

## FileServiceClient
```python
azure.storage.file.FileServiceClient(account_url, credentials=None, configuration=None)

azure.storage.file.FileServiceClient.from_connection_string(conn_str, configuration=None)

FileServiceClient.make_url(protocol=None, sas_token=None)

FileServiceClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)

FileServiceClient.get_service_stats(timeout=None)

# Returns dict-like ServiceProperties
FileServiceClient.get_service_properties(timeout=None)

# Returns None
FileServiceClient.set_service_properties(
    logging=None, hour_metrics=None, minute_metrics=None, cors=None, timeout=None)

# Returns auto-paging iterable of dict-like ShareProperties
FileServiceClient.list_shares(
    prefix=None, include_metadata=False, include_snapshots=False, timeout=None)

FileServiceClient.get_share_client(share_name, snapshot=None)
```

## ShareClient
```python
azure.storage.file.ShareClient(share_url, share_name=None, snaphot=None, credentials=None, configuration=None)

azure.storage.file.ShareClient.from_connection_string(conn_str, share_name, configuration=None)

ShareClient.make_url(protocol=None, sas_token=None)

ShareClient.generate_shared_access_signature(
    permission=None, expiry=None, start=None, id=None, ip=None, protocol=None, cache_control=None,
    content_disposition=None, content_encoding=None, content_language=None, content_type=None)

ShareClient.create_share(metadata=None, quota=None, timeout=None)

ShareClient.create_snapshot(metadata=None, quota=None, timeout=None)

ShareClient.get_share_properties(timeout=None)

ShareClient.set_share_quota(quota, timeout=None)

ShareClient.get_share_metadata(timeout=None)

Shareclient.set_share_metadata(metadata=None, timeout=None)

ShareClient.get_share_acl(timeout=None)

ShareClient.set_share_acl(signed_identifiers=None, timeout=None)

ShareClient.get_share_stats(timeout=None)

# Returns auto-paging iterable of dict-like DirectoryProperties and FileProperties
ShareClient.list_directies_and_files(prefix=None, timeout=None)

ShareClient.delete_share(delete_snapshots=False, timeout=None)

SharedClient.get_directory_client(directory_name, snapshot=None)

SharedClient.get_file_client(file_name, snapshot=None)
```

## DirectoryClient
```python
azure.storage.file.DirectoryClient(
    directory_url, share_name=None, directory_path=None, snaphot=None, credentials=None, configuration=None)

azure.storage.file.DirectoryClient.from_connection_string(
    conn_str, share_name, directory_path, configuration=None)

DirectoryClient.make_url(protocol=None, sas_token=None)

DirectoryClient.generate_shared_access_signature(
    permission=None, expiry=None, start=None, id=None, ip=None, protocol=None, cache_control=None,
    content_disposition=None, content_encoding=None, content_language=None, content_type=None)

DirectoryClient.create_directory(metadata=None, timeout=None)

DirectoryClient.get_directory_properties(timeout=None)

DirectoryClient.get_directory_metadata(timeout=None)

DirectoryClient.set_directory_metadata(metadata=None, timeout=None)

DirectoryClient.list_directies_and_files(prefix=None, timeout=None)

DirectoryClient.delete_directory(timeout=None)

DirectoryClient.get_directory_cient(directory_name, snapshot=None)

DirectoryClient.get_file_cient(file_name, snapshot=None)
```

## FileClient
```python
azure.storage.file.FileClient(
    directory_url, share_name=None, directory_path=None, snaphot=None, credentials=None, configuration=None)

azure.storage.file.FileClient.from_connection_string(
    conn_str, share_name, directory_path, file_name, configuration=None)

FileClient.make_url(protocol=None, sas_token=None)

FileClient.generate_shared_access_signature(
    permission=None, expiry=None, start=None, id=None, ip=None, protocol=None, cache_control=None,
    content_disposition=None, content_encoding=None, content_language=None, content_type=None)

FileClient.get_file_properties(timeout=None)

FileClient.set_http_headers(content_settings, timeout=None)

FileClient.get_file_metadata(timeout=None)

FileClient.set_file_metadata(metadata=None, timeout=None)

FileClient.resize_file(size, timeout=None)

# Returns polling object in order to wait on or abort the operation.
FileClient.copy_from_source(source_url, metadata=None, timeout=None)

FileClient.delete_file(timeout=None)

FileClient.create_file(size, content_settings=None, metadata=None, timeout=None)

FileClient.upload_file(
    data, size=None, content_settings=None, metadata=None, validate_content=False, max_connections=1, timeout=None)

FileClient.download_file(
    start_range=None, end_range=None, validate_content=False, max_connections=1, timeout=None)

FileClient.list_ranges(start_range=None, end_range=None, timeout=None)

FileClient.clear_range(start_range, end_range, timeout=None)

FileClient.update_range(
    data, start_range, end_range, validate_content=False, timeout=None)
```
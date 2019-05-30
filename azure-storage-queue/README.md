# Azure Storage Queue Python SDK

## QueueServiceClient
```python
azure.storage.queue.QueueServiceClient(account_url, credentials=None, configuration=None)

azure.storage.queue.QueueServiceClient.from_connection_string(conn_str, configuration=None)

QueueServiceClient.make_url(protocol=None, sas_token=None)

QueueServiceClient.generate_shared_access_signature(
    resource_types, permission, expiry, start=None, ip=None, protocol=None)

QueueServiceClient.get_service_stats(timeout=None)

# Returns dict-like ServiceProperties
QueueServiceClient.get_service_properties(timeout=None)

# Returns None
QueueServiceClient.set_service_properties(
    logging=None, hour_metrics=None, minute_metrics=None, cors=None, timeout=None)

# Returns an auto-paging iterable of dict-like QueueProperties
QueueServiceClient.list_queues(prefix=None, include_metadata=False, timeout=None)

# Returns QueueClient
QueueServiceClient.get_queue_client(queue_name)
```

## QueueClient
```python
azure.storage.queue.QueueClient(queue_url, queue_name=None, credentials=None, configuration=None)

azure.storage.queue.QueueClient.from_connection_string(conn_str, queue_name, configuration=None)

QueueClient.create_queue(metadata=None, timeout=None)

QueueClient.delete_queue(timeout=None)

# Returns dict of metadata
QueueClient.get_queue_metadata(timeout=None)

QueueClient.set_queue_metadata(metadata=None, timeout=None)

QueueClient.get_queue_acl(timeout=None)

QueueClient.set_queue_acl(signed_identifiers=None, timeout=None)

QueueClient.enqueue_message(
    content, visibility_timeout=None, time_to_live=None, timeout=None)

# Returns message iterator of dict-like Message objects
QueueClient.dequeue_messages(visibility_timeout=None, timeout=None)

# Accepts either a Message object or a message ID.
QueueClient.update_message(message, visibility_timeout, pop_receipt=None, timeout=None)

# Returns message iterator
QueueClient.peek_messages(timeout=None)

QueueClient.clear_messages(timeout=None)

# Accepts either a Message object or a message ID.
QueueClient.delete_message(message, pop_receipt=None, timeout=None)
```


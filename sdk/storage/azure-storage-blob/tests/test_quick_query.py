# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from _shared.testcase import StorageTestCase, GlobalStorageAccountPreparer
from azure.storage.blob import (
    BlobServiceClient,
    CSVDialect,
    JSONEncoder
)

# ------------------------------------------------------------------------------
CSV_DATA = b'Service,Package,Version,RepoPath,MissingDocs\r\nApp Configuration,' \
           b'azure-data-appconfiguration,1,appconfiguration,FALSE\r\nEvent Hubs' \
           b'\r\nEvent Hubs - Azure Storage CheckpointStore,' \
           b'azure-messaging-eventhubs-checkpointstore-blob,1.0.1,eventhubs,FALSE\r\nIdentity,azure-identity,' \
           b'1.1.0-beta.1,identity,FALSE\r\nKey Vault - Certificates,azure-security-keyvault-certificates,' \
           b'4.0.0,keyvault,FALSE\r\nKey Vault - Keys,azure-security-keyvault-keys,4.2.0-beta.1,keyvault,' \
           b'FALSE\r\nKey Vault - Secrets,azure-security-keyvault-secrets,4.1.0,keyvault,FALSE\r\n' \
           b'Storage - Blobs,azure-storage-blob,12.4.0,storage,FALSE\r\nStorage - Blobs Batch,' \
           b'azure-storage-blob-batch,12.4.0-beta.1,storage,FALSE\r\nStorage - Blobs Cryptography,' \
           b'azure-storage-blob-cryptography,12.4.0,storage,FALSE\r\nStorage - File Shares,' \
           b'azure-storage-file-share,12.2.0,storage,FALSE\r\nStorage - Queues,' \
           b'azure-storage-queue,12.3.0,storage,FALSE\r\nText Analytics,' \
           b'azure-ai-textanalytics,1.0.0-beta.2,textanalytics,FALSE\r\nTracing,' \
           b'azure-core-tracing-opentelemetry,1.0.0-beta.2,core,FALSE\r\nService,Package,Version,RepoPath,' \
           b'MissingDocs\r\nApp Configuration,azure-data-appconfiguration,1.0.1,appconfiguration,FALSE\r\n' \
           b'Event Hubs,azure-messaging-eventhubs,5.0.1,eventhubs,FALSE\r\n' \
           b'Event Hubs - Azure Storage CheckpointStore,azure-messaging-eventhubs-checkpointstore-blob,' \
           b'1.0.1,eventhubs,FALSE\r\nIdentity,azure-identity,1.1.0-beta.1,identity,FALSE\r\n' \
           b'Key Vault - Certificates,azure-security-keyvault-certificates,4.0.0,keyvault,FALSE\r\n' \
           b'Key Vault - Keys,azure-security-keyvault-keys,4.2.0-beta.1,keyvault,FALSE\r\n' \
           b'Key Vault - Secrets,azure-security-keyvault-secrets,4.1.0,keyvault,FALSE\r\n' \
           b'Storage - Blobs,azure-storage-blob,12.4.0,storage,FALSE\r\n' \
           b'Storage - Blobs Batch,azure-storage-blob-batch,12.4.0-beta.1,storage,FALSE\r\n' \
           b'Storage - Blobs Cryptography,azure-storage-blob-cryptography,12.4.0,storage,FALSE\r\n' \
           b'Storage - File Shares,azure-storage-file-share,12.2.0,storage,FALSE\r\n' \
           b'Storage - Queues,azure-storage-queue,12.3.0,storage,FALSE\r\n' \
           b'Text Analytics,azure-ai-textanalytics,1.0.0-beta.2,textanalytics,FALSE\r\n' \
           b'Tracing,azure-core-tracing-opentelemetry,1.0.0-beta.2,core,FALSE\r\n' \
           b'Service,Package,Version,RepoPath,MissingDocs\r\n' \
           b'App Configuration,azure-data-appconfiguration,1.0.1,appconfiguration,FALSE\r\n' \
           b'Event Hubs,azure-messaging-eventhubs,5.0.1,eventhubs,FALSE'
CONVERTED_CSV_DATA = b"Service;Package;Version;RepoPath;MissingDocs.App Configuration;azure-data-appconfiguration;" \
                     b"'1.0.1';appconfiguration;FALSE.Event Hubs;azure-messaging-eventhubs;'5.0.1';eventhubs;" \
                     b"FALSE.Event Hubs - Azure Storage CheckpointStore;azure-messaging-eventhubs-checkpointstore-blob;" \
                     b"'1.0.1';eventhubs;FALSE.Identity;azure-identity;'1.1.0-beta.1';identity;FALSE.Key Vault - Certificates;" \
                     b"azure-security-keyvault-certificates;'4.0.0';keyvault;FALSE.Key Vault - Keys;azure-security-keyvault-keys;" \
                     b"'4.2.0-beta.1';keyvault;FALSE.Key Vault - Secrets;azure-security-keyvault-secrets;'4.1.0';keyvault;" \
                     b"FALSE.Storage - Blobs;azure-storage-blob;'12.4.0';storage;FALSE.Storage - Blobs Batch;" \
                     b"azure-storage-blob-batch;'12.4.0-beta.1';storage;FALSE.Storage - Blobs Cryptography;" \
                     b"azure-storage-blob-cryptography;'12.4.0';storage;FALSE.Storage - File Shares;azure-storage-file-share;" \
                     b"'12.2.0';storage;FALSE.Storage - Queues;azure-storage-queue;'12.3.0';storage;FALSE.Text Analytics;" \
                     b"azure-ai-textanalytics;'1.0.0-beta.2';textanalytics;FALSE.Tracing;azure-core-tracing-opentelemetry;" \
                     b"'1.0.0-beta.2';core;FALSE.Service;Package;Version;RepoPath;MissingDocs.App Configuration;" \
                     b"azure-data-appconfiguration;'1.0.1';appconfiguration;FALSE.Event Hubs;azure-messaging-eventhubs;" \
                     b"'5.0.1';eventhubs;FALSE.Event Hubs - Azure Storage CheckpointStore;azure-messaging-eventhubs-checkpointstore-blob;" \
                     b"'1.0.1';eventhubs;FALSE.Identity;azure-identity;'1.1.0-beta.1';identity;" \
                     b"FALSE.Key Vault - Certificates;azure-security-keyvault-certificates;'4.0.0';" \
                     b"keyvault;FALSE.Key Vault - Keys;azure-security-keyvault-keys;'4.2.0-beta.1';keyvault;FALSE.Key Vault - Secrets;" \
                     b"azure-security-keyvault-secrets;'4.1.0';keyvault;FALSE.Storage - Blobs;azure-storage-blob;'12.4.0';" \
                     b"storage;FALSE.Storage - Blobs Batch;azure-storage-blob-batch;'12.4.0-beta.1';storage;FALSE.Storage - Blobs Cryptography;" \
                     b"azure-storage-blob-cryptography;'12.4.0';storage;FALSE.Storage - File Shares;azure-storage-file-share;" \
                     b"'12.2.0';storage;FALSE.Storage - Queues;azure-storage-queue;'12.3.0';storage;FALSE.Text Analytics;" \
                     b"azure-ai-textanalytics;'1.0.0-beta.2';textanalytics;FALSE.Tracing;azure-core-tracing-opentelemetry;" \
                     b"'1.0.0-beta.2';core;FALSE.Service;Package;Version;RepoPath;MissingDocs.App Configuration;" \
                     b"azure-data-appconfiguration;'1.0.1';appconfiguration;FALSE.Event Hubs;azure-messaging-eventhubs;" \
                     b"'5.0.1';eventhubs;FALSE."

ERROR_CSV_DATA = b'Service,Package,Version,RepoPath,MissingDocs\r\nApp Configuration,' \
                 b'azure-data-appconfiguration,1.0.1,appconfiguration,FALSE\r\nEvent Hubs,' \
                 b'azure-messaging-eventhubs,5.0.1,eventhubs,FALSE\r\nEvent Hubs - Azure Storage CheckpointStore,' \
                 b'azure-messaging-eventhubs-checkpointstore-blob,1.0.1,eventhubs,FALSE\r\nIdentity,azure-identity,' \
                 b'1.1.0-beta.1,identity,FALSE\r\nKey Vault - Certificates,azure-security-keyvault-certificates,' \
                 b'4.0.0,keyvault,FALSE\r\nKey Vault - Keys,azure-security-keyvault-keys,4.2.0-beta.1,keyvault,' \
                 b'FALSE\r\nKey Vault - Secrets,azure-security-keyvault-secrets,4.1.0,keyvault,FALSE\r\n' \
                 b'Storage - Blobs,azure-storage-blob,12.4.0,storage,FALSE\r\nStorage - Blobs Batch,' \
                 b'azure-storage-blob-batch,12.4.0-beta.1,storage,FALSE\r\nStorage - Blobs Cryptography,' \
                 b'azure-storage-blob-cryptography,12.4.0,storage,FALSE\r\nStorage - File Shares,' \
                 b'azure-storage-file-share,12.2.0,storage,FALSE\r\nStorage - Queues,' \
                 b'azure-storage-queue,12.3.0,storage,FALSE\r\nText Analytics,' \
                 b'azure-ai-textanalytics,1.0.0-beta.2,textanalytics,FALSE\r\nTracing,' \
                 b'azure-core-tracing-opentelemetry,1.0.0-beta.2,core,FALSE\r\nService,Package,Version,RepoPath,' \
                 b'MissingDocs\r\nApp Configuration,azure-data-appconfiguration,1.0.1,appconfiguration,FALSE\r\n' \
                 b'Event Hubs,azure-messaging-eventhubs,5.0.1,eventhubs,FALSE'


# ------------------------------------------------------------------------------


class StorageQuickQueryTest(StorageTestCase):
    def _setup(self, bsc):
        self.config = bsc._config
        self.container_name = self.get_resource_name('utqqcontainer')

        if self.is_live:
            try:
                bsc.create_container(self.container_name)
            except:
                pass

    def _teardown(self, bsc):
        if self.is_live:
            try:
                bsc.delete_container(self.container_name)
            except:
                pass

        return super(StorageQuickQueryTest, self).tearDown()

    # --Helpers-----------------------------------------------------------------

    def _get_blob_reference(self):
        return self.get_resource_name("csvfile")

    # -- Test cases for APIs supporting CPK ----------------------------------------------

    @GlobalStorageAccountPreparer()
    def test_quick_query_readall(self, resource_group, location, storage_account, storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        # upload the csv file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(CSV_DATA, overwrite=True)

        errors = []

        def on_error(error):
            errors.append(error)

        reader = blob_client.query_blob("SELECT * from BlobStorage", errors=on_error)
        data = reader.readall()

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(reader), len(CSV_DATA))
        self.assertEqual(reader.size, reader.tell())
        #self.assertEqual(data, CSV_DATA)

    @GlobalStorageAccountPreparer()
    def test_quick_query_readall_with_error(self, resource_group, location, storage_account, storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        # upload the csv file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(ERROR_CSV_DATA, overwrite=True)

        errors = []

        def on_error(error):
            errors.append(error)

        reader = blob_client.query_blob("SELECT * from BlobStorage", errors=on_error)
        data = reader.readall()

        self.assertEqual(len(errors), 0)
        self.assertEqual(len(reader), len(CSV_DATA))
        self.assertEqual(reader.size, reader.tell())
        self.assertEqual(data, CSV_DATA)

    @GlobalStorageAccountPreparer()
    def test_quick_query_readall_with_serialization_setting(self, resource_group, location, storage_account,
                                                    storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        # upload the csv file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(CSV_DATA, overwrite=True)

        errors = []

        def on_error(error):
            errors.append(error)

        input_format = CSVDialect(
            delimiter=',',
            quotechar='"',
            lineterminator='\n',
            escapechar=''
        )
        output_format = CSVDialect(
            delimiter=';',
            quotechar="'",
            lineterminator='.',
            escapechar='\\'
        )
        resp = blob_client.query_blob(
            "SELECT * from BlobStorage",
            errors=on_error,
            blob_format=input_format,
            output_format=output_format,
            has_header=False)
        query_result = resp.readall()

        self.assertEqual(len(errors), 0)
        self.assertEqual(resp.size, len(CSV_DATA))
        self.assertEqual(query_result, CONVERTED_CSV_DATA)

    @GlobalStorageAccountPreparer()
    def test_quick_query_readall_with_fatal_error(self, resource_group, location, storage_account,
                                                    storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        data1 = b'{name: owner}'
        data2 = b'{name2: owner2}'
        data3 = b'{version:0,begin:1601-01-01T00:00:00.000Z,intervalSecs:3600,status:Finalized,config:' \
                b'{version:0,configVersionEtag:0x8d75ef460eb1a12,numShards:1,recordsFormat:avro,formatSchemaVersion:3,' \
                b'shardDistFnVersion:1},chunkFilePaths:[$blobchangefeed/log/00/1601/01/01/0000/],storageDiagnostics:' \
                b'{version:0,lastModifiedTime:2019-11-01T17:53:18.861Z,' \
                b'data:{aid:d305317d-a006-0042-00dd-902bbb06fc56}}}'
        data = data1 + b'\n' + data2 + b'\n' + data1

        # upload the json file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(data, overwrite=True)

        errors = []

        def on_error(error):
            errors.append(error)

        input_format = JSONEncoder()
        output_format = CSVDialect(
            delimiter=';',
            quotechar="'",
            lineterminator='.',
            escapechar='\\'
        )
        resp = blob_client.query_blob(
            "SELECT * from BlobStorage",
            errors=on_error,
            blob_format=input_format,
            output_format=output_format)
        query_result = resp.readall()

        self.assertEqual(len(errors), 0)
        self.assertEqual(resp.size, len(CSV_DATA))
        self.assertEqual(query_result, CONVERTED_CSV_DATA)

    @GlobalStorageAccountPreparer()
    def test_quick_query_with_serialization_setting_throws_error(self, resource_group, location, storage_account,
                                                                 storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        # upload the csv file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(CSV_DATA, overwrite=True)

        errors = []

        def progress_callback(error, bytes_processed, total_bytes):
            if error:
                errors.append(error)
            if not bytes_processed:
                print("All bytes have been processed")
                print("Total Bytes should be {}".format(total_bytes))
            else:
                print(bytes_processed)

        input_seri = DelimitedTextConfiguration(column_separator=',', field_quote='"', record_separator='\n',
                                                escape_char='', headers_present=True
                                                )
        output_seri = DelimitedTextConfiguration(column_separator=';', field_quote="'", record_separator='.',
                                                 escape_char='\\', headers_present=True
                                                 )
        resp = blob_client.query("SELECT RepoPath from BlobStorage", progress_callback=progress_callback,
                                 input_serialization=input_seri, output_serialization=output_seri)
        query_result = resp.readall()

        # the error is because that line only has one column
        self.assertEqual(len(errors), 1)
        self.assertEqual(resp.total_bytes, len(CSV_DATA))
        self.assertTrue(len(query_result) > 0)

    @GlobalStorageAccountPreparer()
    def test_quick_query_with_serialization_json_setting(self, resource_group, location, storage_account,
                                                         storage_account_key):
        # Arrange
        bsc = BlobServiceClient(
            self.account_url(storage_account, "blob"),
            credential=storage_account_key)
        self._setup(bsc)

        data1 = b'{\"name\": \"owner\", \"id\": 1}'
        data2 = b'{\"name2\": \"owner2\"}'
        data = data1 + b'\n' + data2 + b'\n' + data1

        # upload the json file
        blob_name = self._get_blob_reference()
        blob_client = bsc.get_blob_client(self.container_name, blob_name)
        blob_client.upload_blob(data, overwrite=True)

        errors = []

        def progress_callback(error, bytes_processed, total_bytes):
            if error:
                errors.append(error)
            if not bytes_processed:
                print("All bytes have been processed")
                print("Total Bytes should be {}".format(total_bytes))
            else:
                print(bytes_processed)

        input_seri = '\n'
        output_seri = ';'

        resp = blob_client.query("SELECT name from BlobStorage", progress_callback=progress_callback,
                                 input_serialization=input_seri, output_serialization=output_seri)
        query_result = resp.readall()

        self.assertEqual(len(errors), 0)
        self.assertEqual(resp.total_bytes, len(data))
        self.assertTrue(len(query_result) > 0)
        blob_client.delete_blob()
# ------------------------------------------------------------------------------

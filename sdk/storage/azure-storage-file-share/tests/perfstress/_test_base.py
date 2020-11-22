# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import uuid

from azure_devtools.perfstress_tests import PerfStressTest

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.fileshare import ShareServiceClient as SyncShareServiceClient
from azure.storage.fileshare.aio import ShareServiceClient as AsyncShareServiceClient


class _ServiceTest(PerfStressTest):
    service_client = None
    async_service_client = None

    def __init__(self, arguments):
        super().__init__(arguments)

        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            raise Exception("Undefined environment variable AZURE_STORAGE_CONNECTION_STRING")

        if not _ServiceTest.service_client or self.args.service_client_per_instance:
            if self.args.max_range_size:
                _ServiceTest.service_client = SyncShareServiceClient.from_connection_string(conn_str=connection_string, max_range_size=self.args.max_range_size)
                _ServiceTest.async_service_client = AsyncShareServiceClient.from_connection_string(conn_str=connection_string, max_range_size=self.args.max_range_size)
            else:
                _ServiceTest.service_client = SyncShareServiceClient.from_connection_string(conn_str=connection_string)
                _ServiceTest.async_service_client = AsyncShareServiceClient.from_connection_string(conn_str=connection_string)

        self.service_client = _ServiceTest.service_client
        self.async_service_client =_ServiceTest.async_service_client

    async def close(self):
        await self.async_service_client.close()
        await super().close()

    @staticmethod
    def add_arguments(parser):
        super(_ServiceTest, _ServiceTest).add_arguments(parser)
        parser.add_argument('--max-range-size', nargs='?', type=int, help='Maximum size of file uploading in single HTTP PUT. Defaults to 4*1024*1024', default=4*1024*1024)
        parser.add_argument('--service-client-per-instance', action='store_true', help='Create one ServiceClient per test instance.  Default is to share a single ServiceClient.', default=False)


class _ShareTest(_ServiceTest):
    share_name = "perfstress-" + str(uuid.uuid4())

    def __init__(self, arguments):
        super().__init__(arguments)
        self.share_client = self.service_client.get_share_client(self.share_name)
        self.async_share_client = self.async_service_client.get_share_client(self.share_name)

    async def global_setup(self):
        await super().global_setup()
        self.share_client.create_share()

    async def global_cleanup(self):
        self.share_client.delete_share()
        await super().global_cleanup()

    async def close(self):
        await self.async_share_client.close()
        await super().close()


class _FileTest(_ShareTest):
    def __init__(self, arguments):
        super().__init__(arguments)
        file_name = "sharefiletest-" + str(uuid.uuid4())
        self.sharefile_client = self.share_client.get_file_client(file_name)
        self.async_sharefile_client = self.async_share_client.get_file_client(file_name)

    async def global_setup(self):
        await super().global_setup()
        try:
            self.sharefile_client.delete_file()
        except ResourceNotFoundError:
            pass

    async def global_cleanup(self):
        try:
            self.sharefile_client.delete_file()
        except ResourceNotFoundError:
            pass
        await super().global_cleanup()

    async def close(self):
        await self.async_sharefile_client.close()
        await super().close()

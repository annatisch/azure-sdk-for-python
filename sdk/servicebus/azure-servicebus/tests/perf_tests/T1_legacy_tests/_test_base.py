# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import uuid

from azure_devtools.perfstress_tests import PerfStressTest

from azure.servicebus import ServiceBusClient, ReceiveMode, ServiceBusMessage
from azure.servicebus.aio import ServiceBusClient as AsyncServiceBusClient
from azure.servicebus.aio.management import ServiceBusAdministrationClient


class _ServiceTest(PerfStressTest):
    service_client = None
    async_service_client = None

    def __init__(self, arguments):
        super().__init__(arguments)

        connection_string = self.get_from_env("AZURE_SERVICEBUS_CONNECTION_STRING")
        if not _ServiceTest.service_client or self.args.service_client_per_instance:
            _ServiceTest.service_client = ServiceBusClient.from_connection_string(connection_string)
            _ServiceTest.async_service_client = AsyncServiceBusClient.from_connection_string(connection_string)

        self.service_client = _ServiceTest.service_client
        self.async_service_client =_ServiceTest.async_service_client

    async def close(self):
        await self.async_service_client.close()
        await super().close()

    @staticmethod
    def add_arguments(parser):
        super(_ServiceTest, _ServiceTest).add_arguments(parser)
        parser.add_argument('--message-size', nargs='?', type=int, help='Maximum size of a single message. Defaults to 1024', default=1024)
        parser.add_argument('--service-client-per-instance', action='store_true', help='Create one ServiceClient per test instance.  Default is to share a single ServiceClient.', default=False)


class _QueueTest(_ServiceTest):
    queue_name = "perfstress-" + str(uuid.uuid4())

    def __init__(self, arguments):
        super().__init__(arguments)
        connection_string = self.get_from_env("AZURE_SERVICEBUS_CONNECTION_STRING")
        self.async_mgmt_client = ServiceBusAdministrationClient.from_connection_string(connection_string)
        self.queue_client = self.service_client.get_queue(self.queue_name)
        self.async_queue_client = self.service_client.get_queue(self.queue_name)

    async def global_setup(self):
        await super().global_setup()
        await self.async_mgmt_client.create_queue(self.queue_name)

    async def global_cleanup(self):
        await self.async_mgmt_client.delete_queue(self.queue_name)
        await super().global_cleanup()

    async def close(self):
        await self.async_mgmt_client.close()
        await super().close()


class _SendTest(_QueueTest):

    def __init__(self, arguments):
        super().__init__(arguments)
        self.sender = self.service_client.get_queue_sender(self.queue_name)
        self.async_sender = self.async_service_client.get_queue_sender(self.queue_name)

    async def global_setup(self):
        await super().global_setup()
        self.sender.open()
        await self.async_sender.open()
    
    async def global_cleanup(self):
        self.sender.close()
        await self.async_sender.close()
        await super().global_cleanup()


class _ReceiveTest(_QueueTest):

    def __init__(self, arguments):
        super().__init__(arguments)
        mode = ReceiveMode.PeekLock if self.args.peeklock else ReceiveMode.ReceiveAndDelete
        self.receiver = self.service_client.get_queue_receiver(
            queue_name=self.queue_name,
            receive_mode=mode,
            prefetch_count=self.args.prefetch,
            max_wait_time=self.args.max_wait_time)
        self.async_receiver = self.service_client.get_queue_receiver(
            queue_name=self.queue_name,
            receive_mode=mode,
            prefetch_count=self.args.prefetch,
            max_wait_time=self.args.max_wait_time)
    
    async def _preload_queue(self):
        data = b'a' * self.args.message_size
        async with self.async_service_client.get_queue_sender(self.queue_name) as sender:
            batch = await sender.create_message_batch()
            for i in range(self.args.preload):
                try:
                    message = ServiceBusMessage(data)
                    batch.add_message(message)
                except ValueError:
                    # Batch full
                    await sender.send_messages(batch)
                    batch = await sender.create_message_batch()

    async def global_setup(self):
        await super().global_setup()
        await self._preload_queue()
        self.receiver.open()
        await self.async_receiver.open()
    
    async def global_cleanup(self):
        self.receiver.close()
        await self.async_receiver.close()
        await super().global_cleanup()

    @staticmethod
    def add_arguments(parser):
        super(_ReceiveTest, _ReceiveTest).add_arguments(parser)
        parser.add_argument('--preload', nargs='?', type=int, help='Number of messages to pre-load in the queue. Defaults to 1000.', default=1000)
        parser.add_argument('--peeklock', action='store_true', help='Receive using PeekLock mode and message settlement.', default=False)
        parser.add_argument('--prefetch', nargs='?', type=int, help='Max number of messages fetched on the connection. Defaults to 0.', default=0)
        parser.add_argument('--max-wait-time', nargs='?', type=int, help='Max time to wait for messages before closing. Defaults to 0.', default=0)
        parser.add_argument('--num-messages', nargs='?', type=int, help='Maximum number of messages to receive. Defaults to 100', default=100)

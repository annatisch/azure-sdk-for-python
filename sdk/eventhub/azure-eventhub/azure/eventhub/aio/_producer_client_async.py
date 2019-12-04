# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
import asyncio
import logging

from typing import Any, Union, TYPE_CHECKING, List, Optional, Dict, cast
from uamqp import constants  # type: ignore

from ..exceptions import ConnectError, EventHubError
from ._client_base_async import ClientBaseAsync
from ._producer_async import EventHubProducer
from .._constants import ALL_PARTITIONS
from .._common import EventData, EventDataBatch

if TYPE_CHECKING:
    from uamqp.constants import TransportType
    from azure.core.credentials import TokenCredential  # type: ignore

_LOGGER = logging.getLogger(__name__)


class EventHubProducerClient(ClientBaseAsync):
    """
    The EventHubProducerClient class defines a high level interface for
    sending events to the Azure Event Hubs service.

    :param str fully_qualified_namespace: The fully qualified host name for the Event Hubs namespace.
     This is likely to be similar to <yournamespace>.servicebus.windows.net
    :param str eventhub_name: The path of the specific Event Hub to connect the client to.
    :param ~azure.core.credentials.TokenCredential credential: The credential object used for authentication which
     implements a particular interface for getting tokens. It accepts
     :class:`EventHubSharedKeyCredential<azure.eventhub.aio.EventHubSharedKeyCredential>`, or credential objects
     generated by the azure-identity library and objects that implement the `get_token(self, *scopes)` method.
    :keyword bool logging_enable: Whether to output network trace logs to the logger. Default is `False`.
    :keyword float auth_timeout: The time in seconds to wait for a token to be authorized by the service.
     The default value is 60 seconds. If set to 0, no timeout will be enforced from the client.
    :keyword str user_agent: The user agent that should be appended to the built-in user agent string.
    :keyword int retry_total: The total number of attempts to redo a failed operation when an error occurs. Default
     value is 3.
    :keyword float idle_timeout: Timeout, in seconds, after which the underlying connection will close
     if there is no further activity. By default the value is None, meaning that the service determines when to
     close an idle connection.
    :keyword transport_type: The type of transport protocol that will be used for communicating with
     the Event Hubs service. Default is `TransportType.Amqp`.
    :paramtype transport_type: ~azure.eventhub.TransportType
    :keyword dict http_proxy: HTTP proxy settings. This must be a dictionary with the following
     keys: `'proxy_hostname'` (str value) and `'proxy_port'` (int value).
     Additionally the following keys may also be present: `'username', 'password'`.

    .. admonition:: Example:

        .. literalinclude:: ../samples/async_samples/sample_code_eventhub_async.py
            :start-after: [START create_eventhub_producer_client_async]
            :end-before: [END create_eventhub_producer_client_async]
            :language: python
            :dedent: 4
            :caption: Create a new instance of the EventHubProducerClient.
    """

    def __init__(self,
                 fully_qualified_namespace: str,
                 eventhub_name: str,
                 credential: 'TokenCredential',
                 **kwargs) -> None:
        super(EventHubProducerClient, self).__init__(
            fully_qualified_namespace=fully_qualified_namespace,
            eventhub_name=eventhub_name,
            credential=credential,
            network_tracing=kwargs.pop("logging_enable", False),
            **kwargs
        )
        self._producers = {ALL_PARTITIONS: self._create_producer()}  # type: Dict[str, Optional[EventHubProducer]]
        self._lock = asyncio.Lock(loop=self._loop)  # sync the creation of self._producers
        self._max_message_size_on_link = 0
        self._partition_ids = None  # Optional[List[str]]

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.close()

    async def _get_partitions(self) -> None:
        if not self._partition_ids:
            self._partition_ids = await self.get_partition_ids()  # type: ignore
            for p_id in cast(List[str], self._partition_ids):
                self._producers[p_id] = None

    async def _get_max_mesage_size(self) -> None:
        # pylint: disable=protected-access,line-too-long
        async with self._lock:
            if not self._max_message_size_on_link:
                await cast(EventHubProducer, self._producers[ALL_PARTITIONS])._open_with_retry()
                self._max_message_size_on_link = \
                    cast(EventHubProducer, self._producers[ALL_PARTITIONS])._handler.message_handler._link.peer_max_message_size \
                    or constants.MAX_MESSAGE_LENGTH_BYTES

    async def _start_producer(self, partition_id: str, send_timeout: Optional[Union[int, float]]) -> None:
        async with self._lock:
            await self._get_partitions()
            if partition_id not in cast(List[str], self._partition_ids) and partition_id != ALL_PARTITIONS:
                raise ConnectError("Invalid partition {} for the event hub {}".format(partition_id, self.eventhub_name))

            if not self._producers[partition_id] or cast(EventHubProducer, self._producers[partition_id]).closed:
                self._producers[partition_id] = self._create_producer(
                    partition_id=partition_id,
                    send_timeout=send_timeout
                )

    def _create_producer(
            self, *,
            partition_id: Optional[str] = None,
            send_timeout: Optional[Union[int, float]] = None
    ) -> EventHubProducer:
        target = "amqps://{}{}".format(self._address.hostname, self._address.path)
        send_timeout = self._config.send_timeout if send_timeout is None else send_timeout

        handler = EventHubProducer(
            self,
            target,
            partition=partition_id,
            send_timeout=send_timeout,
            idle_timeout=self._idle_timeout,
            loop=self._loop
        )
        return handler

    @classmethod
    def from_connection_string(
            cls, conn_str: str,
            *,
            eventhub_name: Optional[str] = None,
            logging_enable: bool = False,
            http_proxy: Optional[Dict[str, Union[str, int]]] = None,
            auth_timeout: float = 60,
            user_agent: Optional[str] = None,
            retry_total: int = 3,
            transport_type: Optional['TransportType'] = None,
            **kwargs: Any
            ) -> 'EventHubProducerClient':
        """Create an EventHubProducerClient from a connection string.

        :param str conn_str: The connection string of an Event Hub.
        :keyword str eventhub_name: The path of the specific Event Hub to connect the client to.
        :keyword bool logging_enable: Whether to output network trace logs to the logger. Default is `False`.
        :keyword dict http_proxy: HTTP proxy settings. This must be a dictionary with the following
         keys: `'proxy_hostname'` (str value) and `'proxy_port'` (int value).
         Additionally the following keys may also be present: `'username', 'password'`.
        :keyword float auth_timeout: The time in seconds to wait for a token to be authorized by the service.
         The default value is 60 seconds. If set to 0, no timeout will be enforced from the client.
        :keyword str user_agent: The user agent that should be appended to the built-in user agent string.
        :keyword int retry_total: The total number of attempts to redo a failed operation when an error occurs.
         Default value is 3.
        :keyword float idle_timeout: Timeout, in seconds, after which the underlying connection will close
         if there is no further activity. By default the value is None, meaning that the service determines when to
         close an idle connection.
        :keyword transport_type: The type of transport protocol that will be used for communicating with
         the Event Hubs service. Default is `TransportType.Amqp`.
        :paramtype transport_type: ~azure.eventhub.TransportType
        :rtype: ~azure.eventhub.aio.EventHubProducerClient

        .. admonition:: Example:

            .. literalinclude:: ../samples/async_samples/sample_code_eventhub_async.py
                :start-after: [START create_eventhub_producer_client_from_conn_str_async]
                :end-before: [END create_eventhub_producer_client_from_conn_str_async]
                :language: python
                :dedent: 4
                :caption: Create a new instance of the EventHubProducerClient from connection string.
        """
        constructor_args = cls._from_connection_string(
            conn_str,
            eventhub_name=eventhub_name,
            logging_enable=logging_enable,
            http_proxy=http_proxy,
            auth_timeout=auth_timeout,
            user_agent=user_agent,
            retry_total=retry_total,
            transport_type=transport_type,
            **kwargs
        )
        return cls(**constructor_args)

    async def send_batch(
            self,
            event_data_batch: EventDataBatch,
            *,
            timeout: Optional[Union[int, float]] = None) -> None:
        """Sends event data and blocks until acknowledgement is received or operation times out.

        :param event_data_batch: The EventDataBatch object to be sent.
        :type event_data_batch: ~azure.eventhub.EventDataBatch
        :param float timeout: The maximum wait time to send the event data.
         If not specified, the default wait time specified when the producer was created will be used.
        :rtype: None
        :raises: :class:`AuthenticationError<azure.eventhub.exceptions.AuthenticationError>`
         :class:`ConnectError<azure.eventhub.exceptions.ConnectError>`
         :class:`ConnectionLostError<azure.eventhub.exceptions.ConnectionLostError>`
         :class:`EventDataError<azure.eventhub.exceptions.EventDataError>`
         :class:`EventDataSendError<azure.eventhub.exceptions.EventDataSendError>`
         :class:`EventHubError<azure.eventhub.exceptions.EventHubError>`

        .. admonition:: Example:

            .. literalinclude:: ../samples/async_samples/sample_code_eventhub_async.py
                :start-after: [START eventhub_producer_client_send_async]
                :end-before: [END eventhub_producer_client_send_async]
                :language: python
                :dedent: 4
                :caption: Asynchronously sends event data

        """
        partition_id = event_data_batch._partition_id or ALL_PARTITIONS  # pylint:disable=protected-access
        try:
            await cast(EventHubProducer, self._producers[partition_id]).send(event_data_batch, timeout=timeout)
        except (KeyError, AttributeError, EventHubError):
            await self._start_producer(partition_id, timeout)
            await cast(EventHubProducer, self._producers[partition_id]).send(event_data_batch, timeout=timeout)

    async def create_batch(
            self,
            *,
            partition_id: Optional[str] = None,
            partition_key: Optional[str] = None,
            max_size_in_bytes: Optional[int] = None) -> EventDataBatch:
        """Create an EventDataBatch object with the max size of all content being constrained by max_size_in_bytes.

        The max_size should be no greater than the max allowed message size defined by the service.

        :param str partition_id: The specific partition ID to send to. Default is None, in which case the service
         will assign to all partitions using round-robin.
        :param str partition_key: With the given partition_key, event data will be sent to
         a particular partition of the Event Hub decided by the service.
        :param int max_size_in_bytes: The maximum size of bytes data that an EventDataBatch object can hold.
        :rtype: ~azure.eventhub.EventDataBatch

        .. admonition:: Example:

            .. literalinclude:: ../samples/async_samples/sample_code_eventhub_async.py
                :start-after: [START eventhub_producer_client_create_batch_async]
                :end-before: [END eventhub_producer_client_create_batch_async]
                :language: python
                :dedent: 4
                :caption: Create EventDataBatch object within limited size

        """
        if not self._max_message_size_on_link:
            await self._get_max_mesage_size()

        if max_size_in_bytes and max_size_in_bytes > self._max_message_size_on_link:
            raise ValueError('Max message size: {} is too large, acceptable max batch size is: {} bytes.'
                             .format(max_size_in_bytes, self._max_message_size_on_link))

        event_data_batch = EventDataBatch(
            max_size_in_bytes=(max_size_in_bytes or self._max_message_size_on_link),
            partition_id=partition_id,
            partition_key=partition_key
        )

        return event_data_batch

    async def get_eventhub_properties(self) -> Dict[str, Any]:
        """Get properties of the Event Hub.

        Keys in the returned dictionary include:

            - `eventhub_name` (str)
            - `created_at` (UTC datetime.datetime)
            - `partition_ids` (list[str])

        :rtype: dict
        :raises: :class:`EventHubError<azure.eventhub.exceptions.EventHubError>`
        """
        return await super(EventHubProducerClient, self)._get_eventhub_properties_async()

    async def get_partition_ids(self) -> List[str]:
        """Get partition IDs of the Event Hub.

        :rtype: list[str]
        :raises: :class:`EventHubError<azure.eventhub.exceptions.EventHubError>`
        """
        return await super(EventHubProducerClient, self)._get_partition_ids_async()

    async def get_partition_properties(self, partition_id: str) -> Dict[str, Any]:
        """Get properties of the specified partition.

        Keys in the properties dictionary include:

            - `eventhub_name` (str)
            - `id` (str)
            - `beginning_sequence_number` (int)
            - `last_enqueued_sequence_number` (int)
            - `last_enqueued_offset` (str)
            - `last_enqueued_time_utc` (UTC datetime.datetime)
            - `is_empty` (bool)

        :param partition_id: The target partition ID.
        :type partition_id: str
        :rtype: dict
        :raises: :class:`EventHubError<azure.eventhub.exceptions.EventHubError>`
        """
        return await super(EventHubProducerClient, self)._get_partition_properties_async(partition_id)

    async def close(self) -> None:
        """Close the Producer client underlying AMQP connection and links.

        :rtype: None

        .. admonition:: Example:

            .. literalinclude:: ../samples/async_samples/sample_code_eventhub_async.py
                :start-after: [START eventhub_producer_client_close_async]
                :end-before: [END eventhub_producer_client_close_async]
                :language: python
                :dedent: 4
                :caption: Close down the handler.

        """
        async with self._lock:
            for producer in self._producers.values():
                if producer:
                    await producer.close()
        await super(EventHubProducerClient, self)._close_async()

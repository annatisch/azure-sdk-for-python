#!/usr/bin/env python

# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

"""
Example to show managing subscription entities under a ServiceBus namespace, including
    - Create a subscription
    - Get subscription properties and runtime information
    - Update a subscription
    - Delete a subscription
    - List subscriptions under the given ServiceBus Namespace
"""

# pylint: disable=C0111

import os
import asyncio
from azure.servicebus.aio.management import ServiceBusAdministrationClient

CONNECTION_STR = os.environ['SERVICE_BUS_CONNECTION_STR']
TOPIC_NAME = "sb_mgmt_demo_topic"
SUBSCRIPTION_NAME = "sb_mgmt_demo_subscription"


async def create_subscription(servicebus_mgmt_client):
    print("-- Create Subscription")
    await servicebus_mgmt_client.create_subscription(TOPIC_NAME, SUBSCRIPTION_NAME)
    print("Subscription {} is created.".format(SUBSCRIPTION_NAME))
    print("")


async def delete_subscription(servicebus_mgmt_client):
    print("-- Delete Subscription")
    await servicebus_mgmt_client.delete_subscription(TOPIC_NAME, SUBSCRIPTION_NAME)
    print("Subscription {} is deleted.".format(SUBSCRIPTION_NAME))
    print("")


async def list_subscriptions(servicebus_mgmt_client):
    print("-- List Subscriptions")
    async for subscription_properties in servicebus_mgmt_client.list_subscriptions(TOPIC_NAME):
        print("Subscription Name:", subscription_properties.name)
    print("")


async def get_and_update_subscription(servicebus_mgmt_client):
    print("-- Get and Update Subscription")
    subscription_properties = await servicebus_mgmt_client.get_subscription(TOPIC_NAME, SUBSCRIPTION_NAME)
    print("Subscription Name:", subscription_properties.name)
    print("Please refer to SubscriptionDescription for complete available settings.")
    print("")
    subscription_properties.max_delivery_count = 5
    await servicebus_mgmt_client.update_subscription(TOPIC_NAME, subscription_properties)


async def get_subscription_runtime_properties(servicebus_mgmt_client):
    print("-- Get Subscription Runtime Properties")
    get_subscription_runtime_properties = await servicebus_mgmt_client.get_subscription_runtime_properties(TOPIC_NAME, SUBSCRIPTION_NAME)
    print("Subscription Name:", get_subscription_runtime_properties.name)
    print("Please refer to SubscriptionRuntimeProperties from complete available runtime properties.")
    print("")

async def main():
    async with ServiceBusAdministrationClient.from_connection_string(CONNECTION_STR) as servicebus_mgmt_client:
        await create_subscription(servicebus_mgmt_client)
        await list_subscriptions(servicebus_mgmt_client)
        await get_and_update_subscription(servicebus_mgmt_client)
        await get_subscription_runtime_properties(servicebus_mgmt_client)
        await delete_subscription(servicebus_mgmt_client)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

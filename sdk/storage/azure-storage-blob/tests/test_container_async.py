# coding: utf-8

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import pytest
import unittest
import asyncio
from dateutil.tz import tzutc

import requests
from datetime import datetime, timedelta

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError, ResourceExistsError
from azure.core.pipeline.transport import AioHttpTransport
from multidict import CIMultiDict, CIMultiDictProxy

from azure.storage.blob.aio import (
    BlobServiceClient,
    ContainerClient,
    BlobClient,
    PublicAccess,
    LeaseClient,
    AccessPolicy,
    StorageErrorCode,
    BlobBlock,
    BlobType,
    ContentSettings,
    BlobProperties,
    ContainerPermissions
)

from testcase import StorageTestCase, TestMode, record, LogCaptured

#------------------------------------------------------------------------------
TEST_CONTAINER_PREFIX = 'container'
#------------------------------------------------------------------------------

class AiohttpTestTransport(AioHttpTransport):
    """Workaround to vcrpy bug: https://github.com/kevin1024/vcrpy/pull/461
    """
    async def send(self, request, **config):
        response = await super(AiohttpTestTransport, self).send(request, **config)
        if not isinstance(response.headers, CIMultiDictProxy):
            response.headers = CIMultiDictProxy(CIMultiDict(response.internal_response.headers))
            response.content_type = response.headers.get("content-type")
        return response


class StorageContainerTestAsync(StorageTestCase):

    def setUp(self):
        super(StorageContainerTestAsync, self).setUp()
        url = self._get_account_url()
        credential = self._get_shared_key_credential()
        self.bsc = BlobServiceClient(url, credential=credential, transport=AiohttpTestTransport())
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.bsc.__aenter__())
        self.test_containers = []

    def tearDown(self):
        if not self.is_playback():
            loop = asyncio.get_event_loop()
            for container_name in self.test_containers:
                try:
                    container = self.bsc.get_container_client(container_name)
                    loop.run_until_complete(container.delete_container())
                except HttpResponseError:
                    try:
                        lease = LeaseClient(container)
                        loop.run_until_complete(lease.break_lease(0))
                        loop.run_until_complete(container.delete_container())
                    except:
                        pass
                except:
                    pass
            loop.run_until_complete(self.bsc.__aexit__())
        return super(StorageContainerTestAsync, self).tearDown()

    #--Helpers-----------------------------------------------------------------
    def _get_container_reference(self, prefix=TEST_CONTAINER_PREFIX):
        container_name = self.get_resource_name(prefix)
        self.test_containers.append(container_name)
        return container_name

    async def _create_container(self, prefix=TEST_CONTAINER_PREFIX):
        container_name = self._get_container_reference(prefix)
        container = self.bsc.get_container_client(container_name)
        try:
            await container.create_container()
        except ResourceExistsError:
            pass
        return container

    #--Test cases for containers -----------------------------------------
    
    async def _test_create_container(self):
        # Arrange
        container_name = self._get_container_reference()

        # Act
        container = self.bsc.get_container_client(container_name)
        created = await container.create_container()

        # Assert
        self.assertTrue(created)

    @record
    def test_create_container(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_container())

    async def _test_create_container_with_already_existing_container_fail_on_exist(self):
        # Arrange
        container_name = self._get_container_reference()

        # Act
        container = self.bsc.get_container_client(container_name)
        created = await container.create_container()
        with self.assertRaises(HttpResponseError):
            await container.create_container()

        # Assert
        self.assertTrue(created)

    @record
    def test_create_container_with_already_existing_container_fail_on_exist(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_container_with_already_existing_container_fail_on_exist())

    async def _test_create_container_with_public_access_container(self):
        # Arrange
        container_name = self._get_container_reference()

        # Act
        container = self.bsc.get_container_client(container_name)
        created = await container.create_container(public_access='container')

        # Assert
        self.assertTrue(created)

    @record
    def test_create_container_with_public_access_container(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_container_with_public_access_container())

    async def _test_create_container_with_public_access_blob(self):
        # Arrange
        container_name = self._get_container_reference()

        # Act
        container = self.bsc.get_container_client(container_name)
        created = await container.create_container(public_access='blob')

        blob = container.get_blob_client("blob1")
        await blob.upload_blob(u'xyz')

        anonymous_service = BlobClient(
            self._get_account_url(),
            container=container_name,
            blob="blob1")

        # Assert
        self.assertTrue(created)
        await anonymous_service.download_blob()

    @record
    def test_create_container_with_public_access_blob(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_container_with_public_access_blob())

    async def _test_create_container_with_metadata(self):
        # Arrange
        container_name = self._get_container_reference()
        metadata = {'hello': 'world', 'number': '42'}

        # Act
        container = self.bsc.get_container_client(container_name)
        created = await container.create_container(metadata)

        # Assert
        self.assertTrue(created)
        md_cr = await container.get_container_properties()
        md = md_cr.metadata
        self.assertDictEqual(md, metadata)

    @record
    def test_create_container_with_metadata(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_create_container_with_metadata())

    async def _test_container_exists_with_lease(self):
        # Arrange
        container = await self._create_container()
        await container.acquire_lease()

        # Act
        exists = await container.get_container_properties()

        # Assert
        self.assertTrue(exists)

    @record
    def test_container_exists_with_lease(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_container_exists_with_lease())

    async def _test_unicode_create_container_unicode_name(self):
        # Arrange
        container_name = u'啊齄丂狛狜'

        container = self.bsc.get_container_client(container_name)
        # Act
        with self.assertRaises(HttpResponseError):
            # not supported - container name must be alphanumeric, lowercase
            await container.create_container()

        # Assert

    @record
    def test_unicode_create_container_unicode_name(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_unicode_create_container_unicode_name())

    async def _test_list_containers(self):
        # Arrange
        container = await self._create_container()

        # Act
        containers = []
        async for c in self.bsc.list_containers():
            containers.append(c)


        # Assert
        self.assertIsNotNone(containers)
        self.assertGreaterEqual(len(containers), 1)
        self.assertIsNotNone(containers[0])
        self.assertNamedItemInContainer(containers, container.container_name)
        self.assertIsNotNone(containers[0].has_immutability_policy)
        self.assertIsNotNone(containers[0].has_legal_hold)

    @record
    def test_list_containers(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_containers())

    async def _test_list_containers_with_prefix(self):
        # Arrange
        container = await self._create_container()

        # Act
        containers = []
        async for c in self.bsc.list_containers(name_starts_with=container.container_name):
            containers.append(c)

        # Assert
        self.assertIsNotNone(containers)
        self.assertEqual(len(containers), 1)
        self.assertIsNotNone(containers[0])
        self.assertEqual(containers[0].name, container.container_name)
        self.assertIsNone(containers[0].metadata)

    @record
    def test_list_containers_with_prefix(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_containers_with_prefix())

    async def _test_list_containers_with_include_metadata(self):
        # Arrange
        container = await self._create_container()
        metadata = {'hello': 'world', 'number': '42'}
        resp = await container.set_container_metadata(metadata)

        # Act
        containers = []
        async for c in self.bsc.list_containers(
            name_starts_with=container.container_name,
            include_metadata=True):
            containers.append(c)

        # Assert
        self.assertIsNotNone(containers)
        self.assertGreaterEqual(len(containers), 1)
        self.assertIsNotNone(containers[0])
        self.assertNamedItemInContainer(containers, container.container_name)
        self.assertDictEqual(containers[0].metadata, metadata)

    @record
    def test_list_containers_with_include_metadata(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_containers_with_include_metadata())

    async def _test_list_containers_with_public_access(self):
        # Arrange
        container = await self._create_container()
        resp = await container.set_container_access_policy(public_access=PublicAccess.Blob)

        # Act
        containers = []
        async for c in self.bsc.list_containers(name_starts_with=container.container_name):
            containers.append(c)

        # Assert
        self.assertIsNotNone(containers)
        self.assertGreaterEqual(len(containers), 1)
        self.assertIsNotNone(containers[0])
        self.assertNamedItemInContainer(containers, container.container_name)
        self.assertEqual(containers[0].public_access, PublicAccess.Blob)

    @record
    def test_list_containers_with_public_access(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_containers_with_public_access())

    async def _test_list_containers_with_num_results_and_marker(self):
        # Arrange
        prefix = 'listcontainer'
        container_names = []
        for i in range(0, 4):
            cr = await self._create_container(prefix + str(i))
            container_names.append(cr.container_name)

        container_names.sort()

        # Act
        generator1 = self.bsc.list_containers(name_starts_with=prefix, results_per_page=2).by_page()
        containers1 = []
        async for c in await generator1.__anext__():
            containers1.append(c)

        generator2 = self.bsc.list_containers(
            name_starts_with=prefix, results_per_page=2).by_page(generator1.continuation_token)
        containers2 = []
        async for c in await generator2.__anext__():
            containers2.append(c)

        # Assert
        self.assertIsNotNone(containers1)
        self.assertEqual(len(containers1), 2)
        self.assertNamedItemInContainer(containers1, container_names[0])
        self.assertNamedItemInContainer(containers1, container_names[1])
        self.assertIsNotNone(containers2)
        self.assertEqual(len(containers2), 2)
        self.assertNamedItemInContainer(containers2, container_names[2])
        self.assertNamedItemInContainer(containers2, container_names[3])

    @record
    def test_list_containers_with_num_results_and_marker(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_containers_with_num_results_and_marker())

    async def _test_set_container_metadata(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '43'}
        container = await self._create_container()

        # Act
        await container.set_container_metadata(metadata)
        md = await container.get_container_properties()
        metadata_from_response = md.metadata
        # Assert
        self.assertDictEqual(metadata_from_response, metadata)

    @record
    def test_set_container_metadata(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_metadata())

    async def _test_set_container_metadata_with_lease_id(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '43'}
        container = await self._create_container()
        lease_id = await container.acquire_lease()

        # Act
        await container.set_container_metadata(metadata, lease_id)

        # Assert
        md = await container.get_container_properties()
        md = md.metadata
        self.assertDictEqual(md, metadata)

    @record
    def test_set_container_metadata_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_metadata_with_lease_id())

    async def _test_set_container_metadata_with_non_existing_container(self):
        # Arrange
        container_name = self._get_container_reference()
        container = self.bsc.get_container_client(container_name)

        # Act
        with self.assertRaises(ResourceNotFoundError):
            await container.set_container_metadata({'hello': 'world', 'number': '43'})

        # Assert

    @record
    def test_set_container_metadata_with_non_existing_container(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_metadata_with_non_existing_container())

    async def _test_get_container_metadata(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '42'}
        container = await self._create_container()
        await container.set_container_metadata(metadata)

        # Act
        md_cr = await container.get_container_properties()
        md = md_cr.metadata

        # Assert
        self.assertDictEqual(md, metadata)

    @record
    def test_get_container_metadata(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_metadata())

    async def _test_get_container_metadata_with_lease_id(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '42'}
        container = await self._create_container()
        await container.set_container_metadata(metadata)
        lease_id = await container.acquire_lease()

        # Act
        md = await container.get_container_properties(lease_id)
        md = md.metadata

        # Assert
        self.assertDictEqual(md, metadata)

    @record
    def test_get_container_metadata_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_metadata_with_lease_id())

    async def _test_get_container_properties(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '42'}
        container = await self._create_container()
        await container.set_container_metadata(metadata)

        # Act
        props = await container.get_container_properties()

        # Assert
        self.assertIsNotNone(props)
        self.assertDictEqual(props.metadata, metadata)
        # self.assertEqual(props.lease.duration, 'infinite')
        # self.assertEqual(props.lease.state, 'leased')
        # self.assertEqual(props.lease.status, 'locked')
        # self.assertEqual(props.public_access, 'container')
        self.assertIsNotNone(props.has_immutability_policy)
        self.assertIsNotNone(props.has_legal_hold)

    @record
    def test_get_container_properties(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_properties())

    async def _test_get_container_properties_with_lease_id(self):
        # Arrange
        metadata = {'hello': 'world', 'number': '42'}
        container = await self._create_container()
        await container.set_container_metadata(metadata)
        lease_id = await container.acquire_lease()

        # Act
        props = await container.get_container_properties(lease_id)
        await lease_id.break_lease()

        # Assert
        self.assertIsNotNone(props)
        self.assertDictEqual(props.metadata, metadata)
        self.assertEqual(props.lease.duration, 'infinite')
        self.assertEqual(props.lease.state, 'leased')
        self.assertEqual(props.lease.status, 'locked')

    @record
    def test_get_container_properties_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_properties_with_lease_id())

    async def _test_get_container_acl(self):
        # Arrange
        container = await self._create_container()

        # Act
        acl = await container.get_container_access_policy()

        # Assert
        self.assertIsNotNone(acl)
        self.assertIsNone(acl.get('public_access'))
        self.assertEqual(len(acl.get('signed_identifiers')), 0)

    @record
    def test_get_container_acl(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_acl())

    async def _test_get_container_acl_with_lease_id(self):
        # Arrange
        container = await self._create_container()
        lease_id = await container.acquire_lease()

        # Act
        acl = await container.get_container_access_policy(lease_id)

        # Assert
        self.assertIsNotNone(acl)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_get_container_acl_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_get_container_acl_with_lease_id())

    async def _test_set_container_acl(self):
        # Arrange
        container = await self._create_container()

        # Act
        response = await container.set_container_access_policy()

        self.assertIsNotNone(response.get('etag'))
        self.assertIsNotNone(response.get('last_modified'))

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertEqual(len(acl.get('signed_identifiers')), 0)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_set_container_acl(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl())

    async def _test_set_container_acl_with_one_signed_identifier(self):
        # Arrange
        from dateutil.tz import tzutc
        container = await self._create_container()

        # Act
        access_policy = AccessPolicy(permission=ContainerPermissions.READ,
                                     expiry=datetime.utcnow() + timedelta(hours=1),
                                     start=datetime.utcnow())
        signed_identifier = {'testid': access_policy}

        response = await container.set_container_access_policy(signed_identifier)

        # Assert
        self.assertIsNotNone(response.get('etag'))
        self.assertIsNotNone(response.get('last_modified'))

    @record
    def test_set_container_acl_with_one_signed_identifier(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_one_signed_identifier())

    async def _test_set_container_acl_with_lease_id(self):
        # Arrange
        container = await self._create_container()
        lease_id = await container.acquire_lease()

        # Act
        await container.set_container_access_policy(lease=lease_id)

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_set_container_acl_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_lease_id())

    async def _test_set_container_acl_with_public_access(self):
        # Arrange
        container = await self._create_container()

        # Act
        await container.set_container_access_policy(public_access='container')

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertEqual('container', acl.get('public_access'))

    @record
    def test_set_container_acl_with_public_access(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_public_access())

    async def _test_set_container_acl_with_empty_signed_identifiers(self):
        # Arrange
        container = await self._create_container()

        # Act
        await container.set_container_access_policy(signed_identifiers=dict())

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertEqual(len(acl.get('signed_identifiers')), 0)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_set_container_acl_with_empty_signed_identifiers(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_empty_signed_identifiers())

    async def _test_set_container_acl_with_signed_identifiers(self):
        # Arrange
        container = await self._create_container()

        # Act
        access_policy = AccessPolicy(permission=ContainerPermissions.READ,
                                     expiry=datetime.utcnow() + timedelta(hours=1),
                                     start=datetime.utcnow() - timedelta(minutes=1))
        identifiers = {'testid': access_policy}
        await container.set_container_access_policy(identifiers)

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertEqual('testid', acl.get('signed_identifiers')[0].id)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_set_container_acl_with_signed_identifiers(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_signed_identifiers())

    async def _test_set_container_acl_with_three_identifiers(self):
        # Arrange
        container = await self._create_container()
        access_policy = AccessPolicy(permission=ContainerPermissions.READ,
                                     expiry=datetime.utcnow() + timedelta(hours=1),
                                     start=datetime.utcnow() - timedelta(minutes=1))
        identifiers = {i: access_policy for i in range(2)}

        # Act
        await container.set_container_access_policy(identifiers)

        # Assert
        acl = await container.get_container_access_policy()
        self.assertIsNotNone(acl)
        self.assertEqual(len(acl.get('signed_identifiers')), 2)
        self.assertEqual('0', acl.get('signed_identifiers')[0].id)
        self.assertIsNotNone(acl.get('signed_identifiers')[0].access_policy)
        self.assertIsNone(acl.get('public_access'))

    @record
    def test_set_container_acl_with_three_identifiers(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_with_three_identifiers())

    async def _test_set_container_acl_too_many_ids(self):
        # Arrange
        container_name = await self._create_container()

        # Act
        identifiers = dict()
        for i in range(0, 6):
            identifiers['id{}'.format(i)] = AccessPolicy()

        # Assert
        with self.assertRaises(ValueError) as e:
            await container_name.set_container_access_policy(identifiers)
        self.assertEqual(
            str(e.exception),
            'Too many access policies provided. The server does not support setting more than 5 access policies on a single resource.'
        )

    @record
    def test_set_container_acl_too_many_ids(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_set_container_acl_too_many_ids())

    async def _test_lease_container_acquire_and_release(self):
        # Arrange
        container = await self._create_container()

        # Act
        lease = await container.acquire_lease()
        await lease.release()

        # Assert

    @record
    def test_lease_container_acquire_and_release(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_acquire_and_release())

    async def _test_lease_container_renew(self):
        # Arrange
        container = await self._create_container()
        lease = await container.acquire_lease(lease_duration=15)
        self.sleep(10)
        lease_id_start = lease.id

        # Act
        await lease.renew()

        # Assert
        self.assertEqual(lease.id, lease_id_start)
        self.sleep(5)
        with self.assertRaises(HttpResponseError):
            await container.delete_container()
        self.sleep(10)
        await container.delete_container()

    @record
    def test_lease_container_renew(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_renew())

    async def _test_lease_container_break_period(self):
        # Arrange
        container = await self._create_container()

        # Act
        lease = await container.acquire_lease(lease_duration=15)

        # Assert
        await lease.break_lease(lease_break_period=5)
        self.sleep(6)
        with self.assertRaises(HttpResponseError):
            await container.delete_container(lease=lease)

    @record
    def test_lease_container_break_period(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_break_period())

    async def _test_lease_container_break_released_lease_fails(self):
        # Arrange
        container = await self._create_container()
        lease = await container.acquire_lease()
        await lease.release()

        # Act
        with self.assertRaises(HttpResponseError):
            await lease.break_lease()

        # Assert

    @record
    def test_lease_container_break_released_lease_fails(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_break_released_lease_fails())

    async def _test_lease_container_with_duration(self):
        # Arrange
        container = await self._create_container()

        # Act
        lease = await container.acquire_lease(lease_duration=15)

        # Assert
        with self.assertRaises(HttpResponseError):
            await container.acquire_lease()
        self.sleep(15)
        await container.acquire_lease()

    @record
    def test_lease_container_with_duration(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_with_duration())

    async def _test_lease_container_twice(self):
        # Arrange
        container = await self._create_container()

        # Act
        lease = await container.acquire_lease(lease_duration=15)

        # Assert
        lease2 = await container.acquire_lease(lease_id=lease.id)
        self.assertEqual(lease.id, lease2.id)

    @record
    def test_lease_container_twice(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_twice())

    async def _test_lease_container_with_proposed_lease_id(self):
        # Arrange
        container = await self._create_container()

        # Act
        proposed_lease_id = '55e97f64-73e8-4390-838d-d9e84a374321'
        lease = await container.acquire_lease(lease_id=proposed_lease_id)

        # Assert
        self.assertEqual(proposed_lease_id, lease.id)

    @record
    def test_lease_container_with_proposed_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_with_proposed_lease_id())

    async def _test_lease_container_change_lease_id(self):
        # Arrange
        container = await self._create_container()

        # Act
        lease_id = '29e0b239-ecda-4f69-bfa3-95f6af91464c'
        lease = await container.acquire_lease()
        lease_id1 = lease.id
        await lease.change(proposed_lease_id=lease_id)
        await lease.renew()
        lease_id2 = lease.id

        # Assert
        self.assertIsNotNone(lease_id1)
        self.assertIsNotNone(lease_id2)
        self.assertNotEqual(lease_id1, lease_id)
        self.assertEqual(lease_id2, lease_id)

    @record
    def test_lease_container_change_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_lease_container_change_lease_id())

    async def _test_delete_container_with_existing_container(self):
        # Arrange
        container = await self._create_container()

        # Act
        deleted = await container.delete_container()

        # Assert
        self.assertIsNone(deleted)

    @record
    def test_delete_container_with_existing_container(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_container_with_existing_container())

    async def _test_delete_container_with_non_existing_container_fail_not_exist(self):
        # Arrange
        container_name = self._get_container_reference()
        container = self.bsc.get_container_client(container_name)

        # Act
        with LogCaptured(self) as log_captured:
            with self.assertRaises(ResourceNotFoundError):
                await container.delete_container()

            log_as_str = log_captured.getvalue()
            #self.assertTrue('ERROR' in log_as_str)

    @record
    def test_delete_container_with_non_existing_container_fail_not_exist(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_container_with_non_existing_container_fail_not_exist())

    async def _test_delete_container_with_lease_id(self):
        # Arrange
        container = await self._create_container()
        lease = await container.acquire_lease(lease_duration=15)

        # Act
        deleted = await container.delete_container(lease=lease)

        # Assert
        self.assertIsNone(deleted)
        with self.assertRaises(ResourceNotFoundError):
            await container.get_container_properties()

    @record
    def test_delete_container_with_lease_id(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_delete_container_with_lease_id())

    async def _test_list_names(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'

        await (container.get_blob_client('blob1')).upload_blob(data)
        await (container.get_blob_client('blob2')).upload_blob(data)


        # Act
        blobs = []
        async for b in container.list_blobs():
            blobs.append(b.name)

        self.assertEqual(blobs, ['blob1', 'blob2'])

    @record
    def test_list_names(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_names())

    async def _test_list_blobs(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        cr0 = container.get_blob_client('blob1')
        await cr0.upload_blob(data)
        cr1 = container.get_blob_client('blob2')
        await cr1.upload_blob(data)

        # Act
        blobs = []
        async for b in container.list_blobs():
            blobs.append(b)

        # Assert
        self.assertIsNotNone(blobs)
        self.assertGreaterEqual(len(blobs), 2)
        self.assertIsNotNone(blobs[0])
        self.assertNamedItemInContainer(blobs, 'blob1')
        self.assertNamedItemInContainer(blobs, 'blob2')
        self.assertEqual(blobs[0].size, 11)
        self.assertEqual(blobs[1].content_settings.content_type,
                         'application/octet-stream')
        self.assertIsNotNone(blobs[0].creation_time)

    @record
    def test_list_blobs(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs())

    async def _test_list_blobs_leased_blob(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        blob1 = container.get_blob_client('blob1')
        await blob1.upload_blob(data)
        lease = await blob1.acquire_lease()

        # Act
        resp = []
        async for b in container.list_blobs():
            resp.append(b)
        # Assert
        self.assertIsNotNone(resp)
        self.assertGreaterEqual(len(resp), 1)
        self.assertIsNotNone(resp[0])
        self.assertNamedItemInContainer(resp, 'blob1')
        self.assertEqual(resp[0].size, 11)
        self.assertEqual(resp[0].lease.duration, 'infinite')
        self.assertEqual(resp[0].lease.status, 'locked')
        self.assertEqual(resp[0].lease.state, 'leased')

    @record
    def test_list_blobs_leased_blob(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_leased_blob())

    async def _test_list_blobs_with_prefix(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        c0 = container.get_blob_client('blob_a1')
        await c0.upload_blob(data)
        c1 = container.get_blob_client('blob_a2')
        await c1.upload_blob(data)
        c2 = container.get_blob_client('blob_b1')
        await c2.upload_blob(data)

        # Act
        resp = []
        async for b in container.list_blobs(name_starts_with='blob_a'):
            resp.append(b)

        # Assert
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp), 2)
        self.assertNamedItemInContainer(resp, 'blob_a1')
        self.assertNamedItemInContainer(resp, 'blob_a2')

    @record
    def test_list_blobs_with_prefix(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_prefix())

    async def _test_list_blobs_with_num_results(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        c0 = container.get_blob_client('blob_a1')
        await c0.upload_blob(data)
        c1 = container.get_blob_client('blob_a2')
        await c1.upload_blob(data)
        c2 = container.get_blob_client('blob_a3')
        await c2.upload_blob(data)
        c3 = container.get_blob_client('blob_b1')
        await c3.upload_blob(data)

        # Act
        generator = container.list_blobs(results_per_page=2).by_page()
        blobs = []
        async for b in await generator.__anext__():
            blobs.append(b)

        # Assert
        self.assertIsNotNone(blobs)
        self.assertEqual(len(blobs), 2)
        self.assertNamedItemInContainer(generator.current_page, 'blob_a1')
        self.assertNamedItemInContainer(generator.current_page, 'blob_a2')

    @record
    def test_list_blobs_with_num_results(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_num_results())

    async def _test_list_blobs_with_include_snapshots(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        blob1 = container.get_blob_client('blob1')
        await blob1.upload_blob(data)
        await blob1.create_snapshot()
        await (container.get_blob_client('blob2')).upload_blob(data)

        # Act
        blobs = []
        async for b in container.list_blobs(include="snapshots"):
            blobs.append(b)

        # Assert
        self.assertEqual(len(blobs), 3)
        self.assertEqual(blobs[0].name, 'blob1')
        self.assertIsNotNone(blobs[0].snapshot)
        self.assertEqual(blobs[1].name, 'blob1')
        self.assertIsNone(blobs[1].snapshot)
        self.assertEqual(blobs[2].name, 'blob2')
        self.assertIsNone(blobs[2].snapshot)

    @record
    def test_list_blobs_with_include_snapshots(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_include_snapshots())

    async def _test_list_blobs_with_include_metadata(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        blob1 = container.get_blob_client('blob1')
        await blob1.upload_blob(data, metadata={'number': '1', 'name': 'bob'})
        await blob1.create_snapshot()
        cr = container.get_blob_client('blob2')
        await cr.upload_blob(data, metadata={'number': '2', 'name': 'car'})

        # Act
        blobs = []
        async for b in container.list_blobs(include="metadata"):
            blobs.append(b)

        # Assert
        self.assertEqual(len(blobs), 2)
        self.assertEqual(blobs[0].name, 'blob1')
        self.assertEqual(blobs[0].metadata['number'], '1')
        self.assertEqual(blobs[0].metadata['name'], 'bob')
        self.assertEqual(blobs[1].name, 'blob2')
        self.assertEqual(blobs[1].metadata['number'], '2')
        self.assertEqual(blobs[1].metadata['name'], 'car')

    @record
    def test_list_blobs_with_include_metadata(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_include_metadata())

    async def _test_list_blobs_with_include_uncommittedblobs(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        blob1 = container.get_blob_client('blob1')
        await blob1.stage_block('1', b'AAA')
        await blob1.stage_block('2', b'BBB')
        await blob1.stage_block('3', b'CCC')

        blob2 = container.get_blob_client('blob2')
        await blob2.upload_blob(data, metadata={'number': '2', 'name': 'car'})

        # Act
        blobs = []
        async for b in container.list_blobs(include="uncommittedblobs"):
            blobs.append(b)

        # Assert
        self.assertEqual(len(blobs), 2)
        self.assertEqual(blobs[0].name, 'blob1')
        self.assertEqual(blobs[1].name, 'blob2')

    @record
    def test_list_blobs_with_include_uncommittedblobs(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_include_uncommittedblobs())

    async def _test_list_blobs_with_include_copy(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        await (container.get_blob_client('blob1')).upload_blob(data, metadata={'status': 'original'})
        sourceblob = 'https://{0}.blob.core.windows.net/{1}/blob1'.format(
            self.settings.STORAGE_ACCOUNT_NAME,
            container.container_name)

        blobcopy = container.get_blob_client('blob1copy')
        await blobcopy.start_copy_from_url(sourceblob, metadata={'status': 'copy'})

        # Act
        blobs = []
        async for b in container.list_blobs(include="copy"):
            blobs.append(b)

        # Assert
        self.assertEqual(len(blobs), 2)
        self.assertEqual(blobs[0].name, 'blob1')
        self.assertEqual(blobs[1].name, 'blob1copy')
        self.assertEqual(blobs[1].blob_type, blobs[0].blob_type)
        self.assertEqual(blobs[1].size, 11)
        self.assertEqual(blobs[1].content_settings.content_type,
                         'application/octet-stream')
        self.assertEqual(blobs[1].content_settings.cache_control, None)
        self.assertEqual(blobs[1].content_settings.content_encoding, None)
        self.assertEqual(blobs[1].content_settings.content_language, None)
        self.assertEqual(blobs[1].content_settings.content_disposition, None)
        self.assertNotEqual(blobs[1].content_settings.content_md5, None)
        self.assertEqual(blobs[1].lease.status, 'unlocked')
        self.assertEqual(blobs[1].lease.state, 'available')
        self.assertNotEqual(blobs[1].copy.id, None)
        self.assertEqual(blobs[1].copy.source, sourceblob)
        self.assertEqual(blobs[1].copy.status, 'success')
        self.assertEqual(blobs[1].copy.progress, '11/11')
        self.assertNotEqual(blobs[1].copy.completion_time, None)

    @record
    def test_list_blobs_with_include_copy(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_include_copy())

    async def _test_list_blobs_with_delimiter(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'

        cr0 = container.get_blob_client('a/blob1')
        await cr0.upload_blob(data)
        cr1 = container.get_blob_client('a/blob2')
        await cr1.upload_blob(data)
        cr2 = container.get_blob_client('b/blob3')
        await cr2.upload_blob(data)
        cr4 = container.get_blob_client('blob4')
        await cr4.upload_blob(data)

        # Act
        resp = []
        async for w in container.walk_blobs():
            resp.append(w)

        # Assert
        self.assertIsNotNone(resp)
        self.assertEqual(len(resp), 3)
        self.assertNamedItemInContainer(resp, 'a/')
        self.assertNamedItemInContainer(resp, 'b/')
        self.assertNamedItemInContainer(resp, 'blob4')

    @record
    def test_list_blobs_with_delimiter(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_delimiter())

    async def _test_walk_blobs_with_delimiter(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'

        cr0 = container.get_blob_client('a/blob1')
        await cr0.upload_blob(data)
        cr1 = container.get_blob_client('a/blob2')
        await cr1.upload_blob(data)
        cr2 = container.get_blob_client('b/c/blob3')
        await cr2.upload_blob(data)
        cr3 = container.get_blob_client('blob4')
        await cr3.upload_blob(data)

        blob_list = []
        def recursive_walk(prefix):
            for b in prefix:
                if b.get('prefix'):
                    recursive_walk(b)
                else:
                    blob_list.append(b.name)

        # Act
        recursive_walk(container.walk_blobs())

        # Assert
        self.assertEqual(len(blob_list), 4)
        self.assertEqual(blob_list, ['a/blob1', 'a/blob2', 'b/c/blob3', 'blob4'])

    @pytest.mark.skip
    def test_walk_blobs_with_delimiter(self):
        if TestMode.need_recording_file(self.test_mode):
            return
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_walk_blobs_with_delimiter())

    async def _test_list_blobs_with_include_multiple(self):
        # Arrange
        container = await self._create_container()
        data = b'hello world'
        blob1 = container.get_blob_client('blob1')
        await blob1.upload_blob(data, metadata={'number': '1', 'name': 'bob'})
        await blob1.create_snapshot()

        client = container.get_blob_client('blob2')
        await client.upload_blob(data, metadata={'number': '2', 'name': 'car'})

        # Act
        blobs = []
        async for b in container.list_blobs(include=["snapshots", "metadata"]):
            blobs.append(b)

        # Assert
        self.assertEqual(len(blobs), 3)
        self.assertEqual(blobs[0].name, 'blob1')
        self.assertIsNotNone(blobs[0].snapshot)
        self.assertEqual(blobs[0].metadata['number'], '1')
        self.assertEqual(blobs[0].metadata['name'], 'bob')
        self.assertEqual(blobs[1].name, 'blob1')
        self.assertIsNone(blobs[1].snapshot)
        self.assertEqual(blobs[1].metadata['number'], '1')
        self.assertEqual(blobs[1].metadata['name'], 'bob')
        self.assertEqual(blobs[2].name, 'blob2')
        self.assertIsNone(blobs[2].snapshot)
        self.assertEqual(blobs[2].metadata['number'], '2')
        self.assertEqual(blobs[2].metadata['name'], 'car')

    @record
    def test_list_blobs_with_include_multiple(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_list_blobs_with_include_multiple())

    async def _test_shared_access_container(self):
        # SAS URL is calculated from storage key, so this test runs live only
        if TestMode.need_recording_file(self.test_mode):
            return

        # Arrange
        container = await self._create_container()
        blob_name  = 'blob1'
        data = b'hello world'

        blob = container.get_blob_client(blob_name)
        await blob.upload_blob(data)

        token = container.generate_shared_access_signature(
            expiry=datetime.utcnow() + timedelta(hours=1),
            permission=ContainerPermissions.READ,
        )
        blob = BlobClient(blob.url, credential=token)

        # Act
        response = requests.get(blob.url)

        # Assert
        self.assertTrue(response.ok)
        self.assertEqual(data, response.content)

    @record
    def test_shared_access_container(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_shared_access_container())

    async def _test_web_container_normal_operations_working(self):
        web_container = "web"

        # create the web container in case it does not exist yet
        container = self.bsc.get_container_client(web_container)
        try:
            try:
                created = await container.create_container()
                self.assertIsNotNone(created)
            except ResourceExistsError:
                pass

            # test if web container exists
            exist = await container.get_container_properties()
            self.assertTrue(exist)

            # create a blob
            blob_name = self.get_resource_name("blob")
            blob_content = self.get_random_text_data(1024)
            blob = container.get_blob_client(blob_name)
            await blob.upload_blob(blob_content)

            # get a blob
            blob_data = await (await blob.download_blob()).content_as_bytes()
            self.assertIsNotNone(blob)
            self.assertEqual(blob_data.decode('utf-8'), blob_content)

        finally:
            # delete container
            await container.delete_container()

    @record
    def test_web_container_normal_operations_working(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._test_web_container_normal_operations_working())


#------------------------------------------------------------------------------
if __name__ == '__main__':
    unittest.main()

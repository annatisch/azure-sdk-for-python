# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import tempfile

from azure_devtools.perfstress_tests import get_random_bytes

from ._test_base import _FileTest


class UploadFromFileTest(_FileTest):
    temp_file = None

    async def global_setup(self):
        await super().global_setup()
        data = get_random_bytes(self.args.size)
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            UploadFromFileTest.temp_file = temp_file.name
            temp_file.write(data)

    async def global_cleanup(self):
        os.remove(UploadFromFileTest.temp_file)
        await super().global_cleanup()

    def run_sync(self):
        with open(UploadFromFileTest.temp_file, 'rb') as fp:
            self.file_client.upload_data(
                fp,
                overwrite=True,
                max_concurrency=self.args.max_concurrency)

    async def run_async(self):
        with open(UploadFromFileTest.temp_file, 'rb') as fp:
            await self.async_file_client.upload_data(
                fp,
                overwrite=True,
                max_concurrency=self.args.max_concurrency)

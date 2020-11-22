# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import tempfile
import uuid

from ._test_base_legacy import _LegacyShareTest


class LegacyDownloadToFileTest(_LegacyShareTest):
    file_name = "downloadtest"

    async def global_setup(self):
        await super().global_setup()
        data = b'a' * self.args.size
        self.service_client.create_file_from_bytes(
            share_name=self.share_name,
            directory_name=None,
            file_name=self.file_name,
            file=data)

    async def setup(self):
        await super().setup()
        self.temp_file = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

    async def cleanup(self):
        os.remove(self.temp_file)
        await super().cleanup()

    def run_sync(self):
        self.service_client.get_file_to_path(
            share_name=self.share_name,
            directory_name=None,
            file_name=self.file_name,
            file_path=self.temp_file)

    async def run_async(self):
        raise NotImplementedError("Async not supported for legacy tests.")

    @staticmethod
    def add_arguments(parser):
        super(LegacyDownloadToFileTest, LegacyDownloadToFileTest).add_arguments(parser)
        parser.add_argument('-s', '--size', nargs='?', type=int, help='Size of files to download.  Default is 10240.', default=10240)

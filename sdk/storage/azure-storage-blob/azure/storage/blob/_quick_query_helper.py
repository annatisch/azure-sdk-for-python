# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from io import BytesIO

from ._shared.avro.datafile import DataFileReader
from ._shared.avro.avro_io import DatumReader

from ._models import BlobQueryError


class BlobQueryReader(object):  # pylint: disable=too-many-instance-attributes
    """A streaming object to read quick query result.

    :ivar str name:
        The name of the blob for the quick query request.
    :ivar str container:
        The name of the container where the blob is.
    :ivar dict response_headers:
        The response_headers of the quick query request.
    :ivar int total_bytes:
        The size of the total data in the stream.
    """

    def __init__(
        self,
        name=None,
        container=None,
        errors='strict',
        record_delimiter='\n',
        encoding=None,
        headers=None,
        response=None
    ):
        self.name = name
        self.container = container
        self.response_headers = headers
        self.size = 0
        self.bytes_processed = 0
        self.record_delimiter = record_delimiter.encode('utf-8')
        self._errors = errors
        self._encoding = encoding
        self._parsed_results = DataFileReader(QuickQueryStreamer(response), DatumReader())
        self._first_result = self._process_record(next(self._parsed_results))

    def __len__(self):
        return self.size

    def _process_record(self, result):
        self.size = result.get('totalBytes', self.size)
        self.bytes_processed = result.get('bytesScanned', self.bytes_processed)
        if 'data' in result:
            return result.get('data')
        if 'fatal' in result:
            error = BlobQueryError(
                error=result['name'],
                is_fatal=result['fatal'],
                description=result['description'],
                position=result['position']
            )
            if (self._errors == 'ignore' and result['fatal']) or self._errors == 'strict':
                raise error
            if self._errors == 'ignore':
                return None
            else:
                if not self._errors(error):
                    raise error
        return None

    def _iter_records(self):
        if self._first_result is not None:
            yield self._first_result
        for next_result in self._parsed_results:
            processed_result = self._process_record(next_result)
            if processed_result is not None:
                yield processed_result

    def readall(self):
        """Return all quick query results.

        This operation is blocking until all data is downloaded.
        :rtype: bytes
        """
        stream = BytesIO()
        self.readinto(stream)
        data = stream.getvalue()
        if self._encoding:
            return data.decode(self._encoding)
        return data

    def readinto(self, stream):
        """Download the quick query result to a stream.

        :param stream:
            The stream to download to. This can be an open file-handle,
            or any writable stream.
        :returns: None
        """
        for record in self._iter_records():
            stream.write(record)

    def records(self):
        """Returns a record generator for the query result.

        :rtype: Iterable[bytes]
        """
        for record_chunk in self._iter_records():
            for record in record_chunk.split(self.record_delimiter):
                if self._encoding:
                    yield record.decode(self._encoding)
                else:
                    yield record



class QuickQueryStreamer(object):
    """
    File-like streaming iterator.
    """

    def __init__(self, generator):
        self.generator = generator
        self.iterator = iter(generator)
        self._buf = b""
        self._point = 0
        self._download_offset = 0
        self._buf_start = 0
        self.file_length = None

    def __len__(self):
        return self.file_length

    def __iter__(self):
        return self.iterator

    @staticmethod
    def seekable():
        return True

    def next(self):
        next_part = next(self.iterator)
        self._download_offset += len(next_part)
        return next_part

    def tell(self):
        return self._point

    def seek(self, offset, whence=0):
        if whence == 0:
            self._point = offset
        elif whence == 1:
            self._point += offset
        else:
            raise ValueError("whence must be 0, or 1")
        if self._point < 0:
            self._point = 0  # XXX is this right?

    def read(self, size):
        try:
            # keep reading from the generator until the buffer of this stream has enough data to read
            while self._point + size > self._download_offset:
                self._buf += self.next()
        except StopIteration:
            self.file_length = self._download_offset

        start_point = self._point

        # EOF
        self._point = min(self._point + size, self._download_offset)

        relative_start = start_point - self._buf_start
        if relative_start < 0:
            raise ValueError("Buffer has dumped too much data")
        relative_end = relative_start + size
        data = self._buf[relative_start: relative_end]

        # dump the extra data in buffer
        # buffer start--------------------16bytes----current read position
        dumped_size = max(relative_end - 16 - relative_start, 0)
        self._buf_start += dumped_size
        self._buf = self._buf[dumped_size:]

        return data
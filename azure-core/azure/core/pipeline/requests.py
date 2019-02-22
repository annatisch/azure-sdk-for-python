# --------------------------------------------------------------------------
#
# Copyright (c) Microsoft Corporation. All rights reserved.
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the ""Software""), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED *AS IS*, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
# --------------------------------------------------------------------------
"""
This module is the requests implementation of Pipeline ABC
"""
from __future__ import absolute_import  # we have a "requests" module that conflicts with "requests" on Py2.7
import contextlib
import logging
import threading
from typing import TYPE_CHECKING, List, Callable, Iterator, Any, Union, Dict, Optional  # pylint: disable=unused-import
import warnings

from oauthlib import oauth2
import requests
from requests.models import CONTENT_CHUNK_SIZE

from urllib3 import Retry  # Needs requests 2.16 at least to be safe

from ..exceptions import (
    TokenExpiredError,
    ClientRequestError,
    raise_with_traceback
)
from ..pipeline import ClientRequest
from . import ClientResponse, HTTPSender, HTTPSenderConfiguration, HTTPPolicy, Response, Request, StreamableClientResponse

_LOGGER = logging.getLogger(__name__)


class RequestsCredentialsPolicy(HTTPPolicy):
    # TODO: Should this be a mandatory policy?
    # Does it rely on deprecated auth constructs?
    """Implementation of request-oauthlib except and retry logic.
    """
    def __init__(self, credentials):
        super(RequestsCredentialsPolicy, self).__init__()
        self._creds = credentials

    def send(self, request, **kwargs):
        session = request.context.session
        try:
            self._creds.signed_session(session)
        except TypeError: # Credentials does not support session injection
            _LOGGER.warning("Your credentials class does not support session injection. Performance will not be at the maximum.")
            request.context.session = session = self._creds.signed_session()

        try:
            try:
                return self.next.send(request, **kwargs)
            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                error = "Token expired or is invalid. Attempting to refresh."
                _LOGGER.warning(error)

            try:
                try:
                    self._creds.refresh_session(session)
                except TypeError: # Credentials does not support session injection
                    _LOGGER.warning("Your credentials class does not support session injection. Performance will not be at the maximum.")
                    request.context.session = session = self._creds.refresh_session()

                return self.next.send(request, **kwargs)
            except (oauth2.rfc6749.errors.InvalidGrantError,
                    oauth2.rfc6749.errors.TokenExpiredError) as err:
                msg = "Token expired or is invalid."
                raise_with_traceback(TokenExpiredError, msg, err)

        except (requests.RequestException,
                oauth2.rfc6749.errors.OAuth2Error) as err:
            msg = "Error occurred in request."
            raise_with_traceback(ClientRequestError, msg, err)


class RequestsContext(object):
    def __init__(self, session):
        self.session = session


class PipelineRequestsHTTPSender(HTTPSender):  # TODO: I think this can be deleted.
    """Implements a basic Pipeline, that supports universal HTTP lib "requests" driver.
    """

    def __init__(self, universal_http_requests_driver=None):
        # type: (Optional[BasicRequestsHTTPSender]) -> None
        self.driver = universal_http_requests_driver or BasicRequestsHTTPSender()

    def __enter__(self):
        # type: () -> PipelineRequestsHTTPSender
        self.driver.__enter__()
        return self

    def __exit__(self, *exc_details):  # pylint: disable=arguments-differ
        self.driver.__exit__(*exc_details)

    def close(self):
        self.__exit__()

    def build_context(self):
        # type: () -> RequestsContext
        return RequestsContext(
            session=self.driver.session,
        )

    def send(self, request, **kwargs):
        # type: (Request[ClientRequest], Any) -> Response
        """Send request object according to configuration.

        :param Request request: The request object to be sent.
        """
        if request.context is None:  # Should not happen, but make mypy happy and does not hurt
            request.context = self.build_context()

        if request.context.session is not self.driver.session:
            kwargs['session'] = request.context.session

        return Response(
            request,
            self.driver.send(request.http_request, **kwargs)
        )


class RequestsClientResponse(ClientResponse):

    def __init__(self, request, requests_response):
        super(RequestsClientResponse, self).__init__(request, requests_response)
        self.status_code = requests_response.status_code
        self.headers = requests_response.headers
        self.reason = requests_response.reason

    def body(self):
        return self.internal_response.content

    def text(self, encoding=None):
        if encoding:
            self.internal_response.encoding = encoding
        return self.internal_response.text

    def raise_for_status(self):
        self.internal_response.raise_for_status()


class StreamableRequestsClientResponse(RequestsClientResponse, StreamableClientResponse):

    def stream_download(self, chunk_size=None, callback=None):
        # type: (Optional[int], Optional[Callable]) -> Iterator[bytes]
        """Generator for streaming request body data.

        :param callback: Custom callback for monitoring progress.
        :param int chunk_size:
        """
        chunk_size = chunk_size or CONTENT_CHUNK_SIZE
        with contextlib.closing(self.internal_response) as response:
            # https://github.com/PyCQA/pylint/issues/1437
            for chunk in response.iter_content(chunk_size):  # pylint: disable=no-member
                if not chunk:
                    break
                if callback and callable(callback):
                    callback(chunk, response=response)
                yield chunk


class BasicRequestsHTTPSender(HTTPSender):
    """Implements a basic requests HTTP sender.

    Since requests team recommends to use one session per requests, you should
    not consider this class as thread-safe, since it will use one Session
    per instance.

    In this simple implementation:
    - You provide the configured session if you want to, or a basic session is created.
    - All kwargs received by "send" are sent to session.request directly
    """

    def __init__(self, session=None):
        # type: (Optional[requests.Session]) -> None
        self.session = session or requests.Session()

    def __enter__(self):
        # type: () -> BasicRequestsHTTPSender
        return self

    def __exit__(self, *exc_details):  # pylint: disable=arguments-differ
        self.close()

    def close(self):
        self.session.close()

    def send(self, request, **kwargs):
        # type: (ClientRequest, Any) -> ClientResponse
        """Send request object according to configuration.

        Allowed kwargs are:
        - session : will override the driver session and use yours. Should NOT be done unless really required.
        - anything else is sent straight to requests.

        :param ClientRequest request: The request object to be sent.
        """
        # It's not recommended to provide its own session, and is mostly
        # to enable some legacy code to plug correctly
        session = kwargs.pop('session', self.session)
        try:
            response = session.request(
                request.method,
                request.url,
                **kwargs)
        except requests.RequestException as err:
            msg = "Error occurred in request."
            raise_with_traceback(ClientRequestError, msg, err)

        return RequestsClientResponse(request, response)


def _patch_redirect(session):
    # type: (requests.Session) -> None
    """Whether redirect policy should be applied based on status code.

    HTTP spec says that on 301/302 not HEAD/GET, should NOT redirect.
    But requests does, to follow browser more than spec
    https://github.com/requests/requests/blob/f6e13ccfc4b50dc458ee374e5dba347205b9a2da/requests/sessions.py#L305-L314

    This patches "requests" to be more HTTP compliant.

    Note that this is super dangerous, since technically this is not public API.
    """
    def enforce_http_spec(resp, request):
        if resp.status_code in (301, 302) and \
                request.method not in ['GET', 'HEAD']:
            return False
        return True

    redirect_logic = session.resolve_redirects

    def wrapped_redirect(resp, req, **kwargs):
        attempt = enforce_http_spec(resp, req)
        return redirect_logic(resp, req, **kwargs) if attempt else []
    wrapped_redirect.is_msrest_patched = True  # type: ignore

    session.resolve_redirects = wrapped_redirect  # type: ignore


class RequestsHTTPSender(BasicRequestsHTTPSender):
    # TODO: Consolidate with BasicRequestsSender above, remove all references to old
    # configuration implementation.
    """A requests HTTP sender that can consume a msrest.Configuration object.

    This instance will consume the following configuration attributes:
    - connection
    - proxies
    - retry_policy
    - redirect_policy
    - enable_http_logger
    - hooks
    - session_configuration_callback
    """

    _protocols = ['http://', 'https://']

    # Set of authorized kwargs at the operation level
    _REQUESTS_KWARGS = [
        'cookies',
        'verify',
        'timeout',
        'allow_redirects',
        'proxies',
        'verify',
        'cert'
    ]

    def __init__(self, config=None):
        # type: (Optional[RequestHTTPSenderConfiguration]) -> None
        self._session_mapping = threading.local()
        self.config = config or RequestHTTPSenderConfiguration()
        super(RequestsHTTPSender, self).__init__()

    @property  # type: ignore
    def session(self):
        try:
            return self._session_mapping.session
        except AttributeError:
            self._session_mapping.session = requests.Session()
            self._init_session(self._session_mapping.session)
            return self._session_mapping.session

    @session.setter
    def session(self, value):
        self._init_session(value)
        self._session_mapping.session = value

    def _init_session(self, session):
        # type: (requests.Session) -> None
        """Init session level configuration of requests.

        This is initialization I want to do once only on a session.
        """
        _patch_redirect(session)

        # Change max_retries in current all installed adapters
        max_retries = self.config.retry_policy()
        for protocol in self._protocols:
            session.adapters[protocol].max_retries = max_retries

    def _configure_send(self, request, **kwargs):
        # type: (ClientRequest, Any) -> Dict[str, str]
        """Configure the kwargs to use with requests.

        See "send" for kwargs details.

        :param ClientRequest request: The request object to be sent.
        :returns: The requests.Session.request kwargs
        :rtype: dict[str,str]
        """
        requests_kwargs = {}  # type: Any
        session = kwargs.pop('session', self.session)

        # If custom session was not create here
        if session is not self.session:
            self._init_session(session)

        session.max_redirects = int(self.config.redirect_policy())
        session.trust_env = bool(self.config.proxies.use_env_settings)

        # Initialize requests_kwargs with "config" value
        requests_kwargs.update(self.config.connection())
        requests_kwargs['allow_redirects'] = bool(self.config.redirect_policy)
        requests_kwargs['headers'] = self.config.headers.copy()

        proxies = self.config.proxies()
        if proxies:
            requests_kwargs['proxies'] = proxies

        # Replace by operation level kwargs
        # We allow some of them, since some like stream or json are controled by msrest
        for key in kwargs:
            if key in self._REQUESTS_KWARGS:
                requests_kwargs[key] = kwargs[key]

        # Hooks. Deprecated, should be a policy
        def make_user_hook_cb(user_hook, session):
            def user_hook_cb(r, *args, **kwargs):
                kwargs.setdefault("msrest", {})['session'] = session
                return user_hook(r, *args, **kwargs)
            return user_hook_cb

        hooks = []
        for user_hook in self.config.hooks:
            hooks.append(make_user_hook_cb(user_hook, self.session))

        if hooks:
            requests_kwargs['hooks'] = {'response': hooks}

        # Configuration callback. Deprecated, should be a policy
        output_kwargs = self.config.session_configuration_callback(
            session,
            self.config,
            kwargs,
            **requests_kwargs
        )
        if output_kwargs is not None:
            requests_kwargs = output_kwargs

        # If custom session was not create here
        if session is not self.session:
            requests_kwargs['session'] = session

        ### Autorest forced kwargs now ###

        # If Autorest needs this response to be streamable. True for compat.
        requests_kwargs['stream'] = kwargs.get('stream', True)

        if request.files:
            requests_kwargs['files'] = request.files
        elif request.data:
            requests_kwargs['data'] = request.data
        requests_kwargs['headers'].update(request.headers)

        return requests_kwargs

    def send(self, request, **kwargs):
        # type: (ClientRequest, Any) -> ClientResponse
        """Send request object according to configuration.

        Available kwargs:
        - session : will override the driver session and use yours. Should NOT be done unless really required.
        - A subset of what requests.Session.request can receive:

            - cookies
            - verify
            - timeout
            - allow_redirects
            - proxies
            - verify
            - cert

        Everything else will be silently ignored.

        :param ClientRequest request: The request object to be sent.
        """
        requests_kwargs = self._configure_send(request, **kwargs)
        return super(RequestsHTTPSender, self).send(request, **requests_kwargs)


class RequestHTTPSenderConfiguration(HTTPSenderConfiguration):  # TODO: Remove
    """Requests specific HTTP sender configuration.

    :param str filepath: Path to existing config file (optional).
    """

    def __init__(self, filepath=None):
        # type: (Optional[str]) -> None

        super(RequestHTTPSenderConfiguration, self).__init__()

        # Retry configuration
        self.retry_policy = ClientRetryPolicy()

        # Requests hooks. Must respect requests hook callback signature
        # Note that we will inject the following parameters:
        # - kwargs['msrest']['session'] with the current session
        self.hooks = []  # type: List[Callable[[requests.Response, str, str], None]]
"""
Provides Mixins and TestCases for snapshot testing outgoing HTTP requests
with VCR_.

Depends on vcrpy_ and requests_, but is also usable with `other HTTP
libraries`_ than requests.

.. _VCR: https://vcrpy.readthedocs.io
.. _vcrpy: https://pypi.org/project/vcrpy/
.. _requests: https://pypi.org/project/requests/
.. _other HTTP libraries: https://vcrpy.readthedocs.io/en/latest/installation.html#compatibility

License:

Copyright 2025 Maykin Media

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all copies
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Taken from https://github.com/maykinmedia/django-common/blob/c5f8985bcb2628139d6da7252947523299aba2e1/maykin_common/vcr.py
"""

import inspect
import os
from collections.abc import Callable, Collection
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any, ClassVar, Protocol, override

from django.test import SimpleTestCase, TestCase, TransactionTestCase, tag

import requests.exceptions
from vcr.cassette import Cassette
from vcr.config import RecordMode
from vcr.request import Request
from vcr.unittest import VCR, VCRMixin as _VCRMixin

__all__ = [
    "SimpleVCRTestCase",
    "TransactionVCRTestCase",
    "VCRMixin",
    "VCRTestCase",
]
type _VCRBRRHook = Callable[[Request], Request | None]
"""VCR before_record_request hook
May mutate Request and return it, or cancel recording by returning None"""


class _VCRTestCase(Protocol):
    "The interface VCRMixin depends on"

    _testMethodName: str

    def _get_cassette_name(self) -> str: ...
    def _get_vcr(self, **kwargs) -> VCR: ...
    # TypedDict is almost as cursed as Protocol :(
    def _get_vcr_kwargs(self, **kwargs) -> dict[str, Any]: ...


class VCRMixin(_VCRMixin):
    """
    Mixin to use VCR cassettes to record HTTP requests/responses.
    """

    vcr_enabled: bool
    """
    Easy toggle to temporarily turn vcr *off* during development or debugging.
    So `True` does *not* enable recording "episodes" that would otherwise not
    be recorded.
    """

    VCR_RECORD_MODE: RecordMode = RecordMode(
        os.environ.get("VCR_RECORD_MODE", RecordMode.NONE)
    )
    """
    Defaults to `VCR_RECORD_MODE` env variable or `RecordMode.NONE`.
    To (re-)record throw away the cassettes and set to `RecordMode.ONCE`
    """

    VCR_TEST_FILES: Path | None = None
    """
    Cassettes will be stored in

      ``VCR_TEST_FILES``/vcr_cassettes/`{test class name}`/`{test method name}.yaml`

    If left `None`, a ``files`` directory at the same level as the test class file
    will be used.
    """

    VCR_FILTER_HEADERS: ClassVar[Collection[str]] = frozenset(
        ("Authorization", "x-api-key")
    )
    """
    Default set of request headers to filter out.

    Passed to the ``filter_headers`` kwarg of VCR by default.
    """

    @override
    def _get_cassette_library_dir(self):
        test_files = self.VCR_TEST_FILES or Path(inspect.getfile(self.__class__)).parent
        test_files.mkdir(exist_ok=True)
        return str(test_files / "vcr_cassettes" / self.__class__.__qualname__)

    @override
    def _get_cassette_name(self: _VCRTestCase):
        """Return the filename for cassette

        Default VCR behaviour puts class name in the cassettename
        we put them in a directory.
        """
        return f"{self._testMethodName}.yaml"

    @override
    def _get_vcr_kwargs(self, **kwargs):
        return {
            "record_mode": self.VCR_RECORD_MODE,
            # Decompress for human readable cassette diffs when re-recoding
            "decode_compressed_response": True,
            "filter_headers": self.VCR_FILTER_HEADERS,
        } | super()._get_vcr_kwargs(**kwargs)

    def vcr_raises(
        self: _VCRTestCase,
        exception: Callable[[], Exception] = requests.exceptions.RequestException,
    ) -> AbstractContextManager[Cassette]:
        """Simulate occurrence of an error during HTTP request.

        Example:

        .. code-block::

            from requests.exceptions import SSLError, Timeout

            # sometimes people let certificates expire
            with self.vcr_raises(SSLError):
                response = function_under_test_that_uses_requests()

            # or services/connections are down
            with self.vcr_raises(Timeout):
                response = function_under_test_that_uses_requests()

        .. note::
           Instead of performing and recording a request, this raises an exception.
           So there will be no request nor cassette!

        """
        # TODO: decouple exception from requests with generic Timeout/SSLError/etc that
        # inherit from all semantically equal exceptions thrown by better libraries
        # than requests. A client can then change its implementation without a need to
        # change the tests (iff it doesn't do anything with the Error arguments).

        kwargs = self._get_vcr_kwargs()
        hook: _VCRBRRHook = kwargs.get("before_record_request") or (lambda _: None)

        def raise_exception(request):
            # perform configured hook first
            hook(request)
            raise exception()

        clean_vcr = self._get_vcr(**kwargs | {"before_record_request": raise_exception})
        return clean_vcr.use_cassette(self._get_cassette_name())  # pyright: ignore[reportReturnType] upstream inferred type is wrong


@tag("vcr")
class SimpleVCRTestCase(VCRMixin, SimpleTestCase):
    """A Django ``SimpleTestCase`` with the ``VCRMixin`` and a ``vcr`` tag.

    Use this for testing "client code".
    """


@tag("vcr")
class VCRTestCase(VCRMixin, TestCase):
    """A Django ``TestCase`` with the ``VCRMixin`` and a ``vcr`` tag.

    Use this if your `Model` may do HTTP requests.
    """


@tag("vcr")
class TransactionVCRTestCase(VCRMixin, TransactionTestCase):
    """A Django ``TestCase`` with the ``VCRMixin`` and a ``vcr`` tag.

    Use this only if you really need it. i.e when you're actually testing the
    transactional behaviour of your app.
    """

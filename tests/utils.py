"""
Utilities for test cases
"""
from functools import partial
from http import HTTPStatus
from typing import cast

from requests import Response


class MockResponse(object):

    def __init__(self, status_code: int, content: bytes):
        self._status_code = status_code
        self._content = content

    @property
    def status_code(self):
        return self._status_code

    @property
    def content(self):
        return self._content


def get_mocked_response(status_code: int, content: bytes) -> Response:
    mock_resp = cast(Response, MockResponse(status_code, content))
    return mock_resp


get_mocked_error_response = partial(
    get_mocked_response,
    status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
    content=b'error happened'
)

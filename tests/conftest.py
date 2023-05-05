import pytest
import requests_mock

@pytest.fixture
def requests_mocker() -> requests_mock.Mocker:
    with requests_mock.Mocker() as mocker:
        yield mocker

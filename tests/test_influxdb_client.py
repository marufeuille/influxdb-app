import datetime
import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.influxdb_client import InfluxDbClient

DIR_PATH = os.path.dirname(__file__)


def mocked_requests_get(*args, **kwargs): # type: ignore
    class MockResponse:
        def __init__(self, response_text: str, status_code: int):
            self.text = response_text
            self.status_code = status_code

    return MockResponse(kwargs["response_text"], kwargs["status_code"])


def test_influxdb_client(mocker): # type: ignore
    with open(os.path.join(DIR_PATH, "data/test.json")) as f:
        response_text = f.read()
    mocker.patch(
        "requests.get",
        return_value=mocked_requests_get(response_text=response_text, status_code=200),
    )
    client = InfluxDbClient("http://localhost:8086/query", "token")
    data = client.get_data("temperature", "test_db", "test_rp", "medaka")

    assert data == response_text.strip()


query_test_parameters = [
    (
        "temperature",
        "test_db",
        "test_rp",
        "test_ms",
        None,
        None,
        """
        SELECT
            temperature
        FROM
            test_db.test_rp.test_ms
        WHERE
            1 = 1""",
    ),
    (
        "temperature",
        "test_db",
        "test_rp",
        "test_ms",
        datetime.datetime(2021, 10, 1),
        None,
        """
        SELECT
            temperature
        FROM
            test_db.test_rp.test_ms
        WHERE
            1 = 1
            AND '2021-10-01T00:00:00Z' <= time""",
    ),
    (
        "temperature",
        "test_db",
        "test_rp",
        "test_ms",
        None,
        datetime.datetime(2021, 10, 1),
        """
        SELECT
            temperature
        FROM
            test_db.test_rp.test_ms
        WHERE
            1 = 1
            AND time < '2021-10-01T00:00:00Z'""",
    ),
    (
        "temperature",
        "test_db",
        "test_rp",
        "test_ms",
        datetime.datetime(2021, 10, 1),
        datetime.datetime(2021, 10, 2),
        """
        SELECT
            temperature
        FROM
            test_db.test_rp.test_ms
        WHERE
            1 = 1
            AND '2021-10-01T00:00:00Z' <= time
            AND time < '2021-10-02T00:00:00Z'""",
    ),
]


@pytest.mark.parametrize(
    "key_name, db_name, rp_name, ms_name, begin_datetime, end_datetime, expected",
    query_test_parameters,
)
def test__gen_query_minimum(
    key_name, db_name, rp_name, ms_name, begin_datetime, end_datetime, expected
    ): # type: ignore
    client = InfluxDbClient("http://localhost:8086/query", "token")
    result_query = client._gen_query(
        key_name, db_name, rp_name, ms_name, begin_datetime, end_datetime
    )
    assert result_query == expected

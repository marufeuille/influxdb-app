import os
import sys
import datetime
import json

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from sensor_data import SensorData
from sensor_status import SensorStatus


@pytest.mark.parametrize(
    "sensor_data, expected_dict",
    [
        (
            SensorData(
                status=SensorStatus.SUCCESS,
                name="test",
                humidity=50,
                temperature=10,
                observed_timestamp=int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp()),
            ),
            {
                "status": "success",
                "name": "test",
                "temperature": 10,
                "humidity": 50,
                "observed_timestamp": int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp())
            }
        ),
        (
            SensorData(
                status=SensorStatus.SUCCESS,
                name="test",
                temperature=10,
                observed_timestamp=int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp()),
            ),
            {
                "status": "success",
                "name": "test",
                "temperature": 10,
                "observed_timestamp": int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp())
            }
        ),
        (
            SensorData(
                status=SensorStatus.SUCCESS,
                name="test",
                humidity=50,
                observed_timestamp=int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp()),
            ),
            {
                "status": "success",
                "name": "test",
                "humidity": 50,
                "observed_timestamp": int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp())
            }
        ),
        (
            SensorData(
                status=SensorStatus.SUCCESS,
                name="test",
                observed_timestamp=int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp()),
            ),
            {
                "status": "success",
                "name": "test",
                "observed_timestamp": int(datetime.datetime(2021, 10, 1, 10, 0, 0).timestamp())
            }
        ),
    ]
)
def test_to_dict_json(sensor_data, expected_dict):
    result = sensor_data.to_dict()
    assert result == expected_dict
    json_result = sensor_data.to_json()
    assert json.loads(json_result) == expected_dict


import os
import sys


import pytest
from bluepy import btle

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
import engbird
from engbird import EngbirdIBSTH1Sensor
from sensor_status import SensorStatus


def mock_peripheral(return_value):
    class MockPeripheral:
        def __init__(self, *params, **kwargs):
            pass
        def readCharacteristic(self, *params, **kwargs):
            return return_value

    return MockPeripheral

@pytest.mark.parametrize(
    "characteristic_value, expected_temperature, expected_humidity",
    [
        (
            b'\x95\x07\xcd\x1d\x01p\x06',
            19.41,
            76.29
        ),
    ]
)
def test_get_sensor_data(characteristic_value, expected_temperature, expected_humidity, mocker):
    mocked_peripheral = mock_peripheral(characteristic_value)
    mocker.patch('engbird.btle.Peripheral', mocked_peripheral)

    sensor = EngbirdIBSTH1Sensor("test", "XX:XX:XX:XX:XX:XX")
    data = sensor.get_sensor_data()

    assert data.temperature == expected_temperature
    assert data.humidity == expected_humidity
    assert data.status == SensorStatus.SUCCESS


class ErrorMockPeripheral:
    def __init__(self, *params, **kwargs):
        pass
    def readCharacteristic(self, *params, **kwargs):
        raise btle.BTLEDisconnectError("test")



def test_get_sensor_data_error(mocker):
    mocker.patch('engbird.btle.Peripheral', ErrorMockPeripheral)

    sensor = EngbirdIBSTH1Sensor("test", "XX:XX:XX:XX:XX:XX")
    data = sensor.get_sensor_data()

    assert data.status == SensorStatus.FAILURE



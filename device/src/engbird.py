import argparse
import logging
from datetime import datetime
from time import sleep

from bluepy import btle
from sensor_data import SensorData
from sensor_status import SensorStatus

logging.basicConfig(level=logging.INFO)


class EngbirdIBSTH1Sensor:
    def __init__(self, name: str, macaddr: str, characteristic_code: int = 0x0028):
        self._name = name
        self._macaddr = macaddr
        self._characteristic_code = characteristic_code

    def get_sensor_data(self) -> SensorData:
        now = int(datetime.now().timestamp())
        try:
            if "_peripheral" not in self.__dict__.keys():
                self._peripheral = btle.Peripheral(self._macaddr)
            characteristic = self._peripheral.readCharacteristic(
                self._characteristic_code
            )
        except btle.BTLEDisconnectError:
            logging.error("could not connect sensor device.")

            return SensorData(
                status=SensorStatus.FAILURE,
                name=self._name,
                humidity=None,
                temperature=None,
                observed_timestamp=now,
            )
        else:
            temperature = int.from_bytes(characteristic[0:2], "little") / 100
            humidity = int.from_bytes(characteristic[2:4], "little") / 100
            return SensorData(
                status=SensorStatus.SUCCESS,
                name=self._name,
                humidity=humidity,
                temperature=temperature,
                observed_timestamp=now,
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--macaddr", type=str, required=True)
    parser.add_argument("--max_retry", type=int, required=False, default=5)
    parser.add_argument("--interval", type=int, required=False, default=5)
    args = parser.parse_args()
    max_retry: int = args.max_retry
    interval: int = args.interval
    engbird = EngbirdIBSTH1Sensor("medaka", args.macaddr)
    for _ in range(max_retry):
        data = engbird.get_sensor_data()
        if data.status == SensorStatus.SUCCESS:
            json = data.to_json()
            logging.info(json)
            print(json)
            break
        sleep(interval)

    else:
        logging.error(f"Error: Exceeded Max Retry{max_retry}")
        json = data.to_json()
        print(json)
        logging.error(json)

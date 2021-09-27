from dataclasses import dataclass
from typing import Optional
import json

from sensor_status import SensorStatus

@dataclass
class SensorData:
    status: SensorStatus
    name: str
    humidity: Optional[float]
    temperature: Optional[float]
    observed_timestamp: int


    def to_dict(self):
        dic: Dict[str, str] = {
            "status": self.status.value,
            "name": self.name,
            "observed_timestamp": int(self.observed_timestamp.timestamp())
        }
        if self.humidity is not None:
            dic["humidity"] = self.humidity
        if self.temperature is not None:
            dic["temperature"] = self.temperature
        return dic

    def to_json(self):
        return json.dumps(self.to_dict())

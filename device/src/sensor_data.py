import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from sensor_status import SensorStatus


@dataclass
class SensorData:
    status: SensorStatus
    name: str
    observed_timestamp: int
    humidity: Optional[float]=None
    temperature: Optional[float]=None

    def to_dict(self) -> Dict[str, Any]:
        dic: Dict[str, Any] = {
            "status": self.status.value,
            "name": self.name,
            "observed_timestamp": self.observed_timestamp
        }
        if self.humidity is not None:
            dic["humidity"] = self.humidity
        if self.temperature is not None:
            dic["temperature"] = self.temperature
        return dic

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

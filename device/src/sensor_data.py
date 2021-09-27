import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

from sensor_status import SensorStatus


@dataclass
class SensorData:
    status: SensorStatus
    name: str
    humidity: Optional[float]
    temperature: Optional[float]
    observed_timestamp: int

    def to_dict(self) -> Dict[str, Any]:
        dic: Dict[str, Any] = {
            "status": self.status.value,
            "name": self.name,
            "observed_timestamp": int(self.observed_timestamp.timestamp()),  # type: ignore
        }
        if self.humidity is not None:
            dic["humidity"] = self.humidity
        if self.temperature is not None:
            dic["temperature"] = self.temperature
        return dic

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

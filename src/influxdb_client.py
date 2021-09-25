import json
from datetime import datetime
from typing import Any, Dict, Optional

import requests


class InfluxDbClient:
    def __init__(self, url: str, token: str):
        self._url = url
        self._token = token

    def _gen_query(
        self,
        key_name: str,
        db: str,
        rp: str,
        measurement: str,
        begin_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
    ) -> str:
        query = f"""
        SELECT
            {key_name}
        FROM
            {db}.{rp}.{measurement}
        WHERE
            1 = 1"""
        if begin_datetime is not None:
            query = "\n".join(
                [query, f"            AND '{begin_datetime.isoformat()}Z' <= time"]
            )
        if end_datetime is not None:
            query = "\n".join(
                [query, f"            AND time < '{end_datetime.isoformat()}Z'"]
            )
        return query

    def get_data(
        self,
        key_name: str,
        db: str,
        rp: str,
        measurement: str,
        begin_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        query = self._gen_query(
            key_name, db, rp, measurement, begin_datetime, end_datetime
        )

        headers = {"Authorization": f"Token {self._token}"}
        payloads = {"db": db, "q": query}

        response = requests.get(self._url, headers=headers, params=payloads)
        return json.loads(response.text.strip())  # type: ignore

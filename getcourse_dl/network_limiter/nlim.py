"""
Network limiter staff. Limit ops/s not to get banned.
Follows requests api.
"""
from typing import Any
import requests


class NLim:
    def get(self, *args: Any, **kwargs: Any) -> requests.Response:
        return requests.get(*args, **kwargs)  # by far dummy


nlim = NLim()

from datetime import datetime
from src.additel_sdk.coerce import coerce
from src.additel_sdk.time import TimeTick


def test_timetick():
    data = {
        "$type": "TAU.Module.Channels.DI.TimeTick",
        "TickTime": "2025-03-22 14:05:12 123456",
    }
    result = coerce(data)
    assert isinstance(result, TimeTick)
    assert result == datetime(2025, 3, 22, 14, 5, 12, 123456)

import json
from app.extensions import ma
from app.shared import BaseSchema

from ..models import (
    Model_EventLog,
)


class Schema_EventLog(BaseSchema):
    class Meta:
        model = Model_EventLog
        load_instance = True

    event_payload = ma.Method("get_event_payload", deserialize="load_event_payload")

    def get_event_payload(self, obj):
        return json.loads(obj.event_payload) if obj.event_payload is not None else None

    def load_event_payload(self, value):
        return json.dumps(value) if value is not None else None

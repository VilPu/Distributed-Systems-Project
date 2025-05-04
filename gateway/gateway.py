import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from google.protobuf import empty_pb2
from fastapi import HTTPException

import sensors_pb2

# REST for the client based on https://fastapi.tiangolo.com/#example-upgrade
# gRPC based on https://medium.com/@coderviewer/simple-usage-of-grpc-with-python-f714d9f69daa
app = FastAPI()

# REST output model
class SensorReadingOut(BaseModel):
    sensor_id: str
    reading_type: str
    reading_value: float
    timestamp: str

class SensorListOut(BaseModel):
    sensor_ids: List[str]

class AlertListOut(BaseModel):
    alerts: List[str]

class SensorHistoryOut(BaseModel):
    history: List[str]

# use real stubs or mock stubs
USE_MOCK = os.getenv("USE_MOCK", "false")
if USE_MOCK == "true":
    from mock_services import MockSensorsStub, MockStorageStub, MockAlertStub
    sensors_stub = MockSensorsStub()
    storage_stub = MockStorageStub()
    alerts_stub = MockAlertStub()
else:
    from grpc_clients import sensors_stub, storage_stub, alerts_stub


@app.get("/sensors/{sensor_id}", response_model=SensorReadingOut)
def get_sensor(sensor_id: str):
    request = sensors_pb2.SensorRequest(sensor_id=sensor_id)
    response = sensors_stub.GetSensorData(request)
    if not response.sensor_id:
        raise HTTPException(status_code=404, detail=f"Sensor with id: {sensor_id} not found")
    return {
        "sensor_id": response.sensor_id,
        "reading_type": response.reading_type,
        "reading_value": response.reading_value,
        "timestamp": response.timestamp
    }

@app.get("/sensors", response_model=SensorListOut)
def get_sensors():
    response = sensors_stub.ListSensors(empty_pb2.Empty())
    return {
        "sensor_ids": list(response.sensor_ids)
    }

@app.get("/alerts", response_model=AlertListOut)
def get_alerts():
    response = alerts_stub.GetAlerts(empty_pb2.Empty())
    return {
        "alerts": [
            f"{alert.alert_message} (triggered={alert.triggered}) at {alert.timestamp}"
            for alert in response.alerts
        ]
    }

@app.get("/history/{sensor_id}",response_model=SensorHistoryOut)
def get_history(sensor_id: str):
    request = sensors_pb2.SensorRequest(sensor_id=sensor_id)
    response = storage_stub.GetHistory(request)
    if not response.history:
        raise HTTPException(status_code=404, detail=f"Sensor with id: {sensor_id} not found")
    return {
        "history": [
            f"{history_entry.sensor_id}: {history_entry.reading_type}={history_entry.reading_value} at {history_entry.timestamp}"
            for history_entry in response.history
        ]
    }


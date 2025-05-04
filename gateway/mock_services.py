import sensors_pb2

# create mock stubs instead of real stubs for testing

class MockSensorsStub:
    def GetSensorData(self, request):
        print(f"MockSensorsStub called with sensor_id={request.sensor_id}")
        sensor_id = request.sensor_id
        if sensor_id == "s1-temp":
            return sensors_pb2.SensorReading(
                sensor_id=sensor_id,
                reading_type="temperature",
                reading_value=10.0,
                timestamp="2025-04-27T11:51:00Z"
            )
        elif sensor_id == "s2-humid":
            return sensors_pb2.SensorReading(
                sensor_id=sensor_id,
                reading_type="humidity",
                reading_value=40.0,
                timestamp="2025-04-27T11:51:00Z"
            )
        elif sensor_id == "s3-temp":
            return sensors_pb2.SensorReading(
                sensor_id=sensor_id,
                reading_type="temperature",
                reading_value=25.0,
                timestamp="2025-04-27T11:51:00Z"
            )
        else:
            return sensors_pb2.SensorReading()


    def ListSensors(self, request):
        return sensors_pb2.SensorsList(
            sensor_ids=['s1-temp', 's2-humid', 's3-temp']
        )

class MockStorageStub:
    def GetHistory(self, request):
        sensor_id = request.sensor_id
        print(f"MockStorageStub called with sensor_id={sensor_id}")
        if sensor_id == "s1-temp":
            history_entries = [
                sensors_pb2.SensorReading(
                    sensor_id=sensor_id,
                    reading_type="temperature",
                    reading_value=10.0,
                    timestamp="2025-04-27T11:51:00Z"
                ),
                sensors_pb2.SensorReading(
                    sensor_id=sensor_id,
                    reading_type="temperature",
                    reading_value=11.0,
                    timestamp="2025-04-27T11:51:00Z"
                ),
            ]
        elif sensor_id == "s2-humid":
            history_entries = [
                sensors_pb2.SensorReading(
                    sensor_id=sensor_id,
                    reading_type="humidity",
                    reading_value=40,
                    timestamp="2025-04-27T11:51:00Z"
                )
            ]
        elif sensor_id == "s3-temp":
            history_entries = [
                sensors_pb2.SensorReading(
                    sensor_id=sensor_id,
                    reading_type="temperature",
                    reading_value=22.0,
                    timestamp="2025-04-27T11:51:00Z"
                ),
                sensors_pb2.SensorReading(
                    sensor_id=sensor_id,
                    reading_type="temperature",
                    reading_value=0.0,
                    timestamp="2025-04-27T11:51:00Z"
                ),
            ]
        else:
            history_entries = []
        return sensors_pb2.SensorHistory(history=history_entries)

class MockAlertStub:
    def GetAlerts(self, request):
        return sensors_pb2.AlertList(
            alerts = [
                sensors_pb2.AlertStatus(
                    triggered=True,
                    alert_message= "s1-temp: temp too low",
                    timestamp="2025-04-27T10:30:00Z"
                ),
                sensors_pb2.AlertStatus(
                    triggered=True,
                    alert_message="s2-humid: humid too high",
                    timestamp="2025-04-27T10:30:00Z"
                ),
                sensors_pb2.AlertStatus(
                    triggered=True,
                    alert_message="s3-temp: temp too low",
                    timestamp="2025-04-27T10:30:00Z"
                )
            ]
        )

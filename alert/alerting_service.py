import grpc
from concurrent import futures
import time
import logging
import protos.sensors_pb2_grpc as sensors_pb2_grpc
import protos.sensors_pb2 as sensors_pb2

FORMAT = '%(asctime)s %(levelname)-5s: %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)

# Static thresholds for each sensor type
THRESHOLDS = {
    "temperature": 80.0,
    "humidity": 90.0,
    "pressure": 1200.0,
    "timeseries": 30.0  # testin vuoksi
}

# In-memory alert store
active_alerts = {}

class AlertService():
    def CheckAlert(self, request, context):
        sensor_id = request.sensor_id
        reading_type = request.reading_type
        value = request.reading_value
        timestamp = request.timestamp

        threshold = THRESHOLDS.get(reading_type)

        if threshold is not None and value > threshold:
            active_alerts[sensor_id] = {
                "triggered": True,
                "alert_message": "Threshold exceeded!",
                "timestamp": timestamp
            }
            logging.warning(f"ALERT: {sensor_id} sent {value} for {reading_type}, exceeds threshold {threshold}")
            return sensors_pb2.AlertStatus(
                triggered = True,
                alert_message = "Threshold exceeded!",
                timestamp = timestamp
            )

        # Remove alert if value goes back to normal
        if sensor_id in active_alerts:
            del active_alerts[sensor_id]

        return sensors_pb2.AlertStatus(
            triggered=False,
            alert_message = "Reading normal",
            timestamp = timestamp
        )

    def GetAlerts(self, request, context):
        alerts = sensors_pb2.AlertList()
        for sid, data in active_alerts.items():
            alerts.alerts.append(sensors_pb2.AlertStatus(
                triggered = data.triggered,
                alert_message = data.alert_message,
                timestamp = data.timestamp
            ))
        return alerts

def serve():
    port = "5052"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensors_pb2_grpc.add_AlertServiceServicer_to_server(AlertService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info(f"Alerting service started on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    serve()

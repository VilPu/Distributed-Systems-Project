from concurrent import futures
from Sensor import Sensor

import protos.sensors_pb2_grpc as sensors_pb2_grpc
import protos.sensors_pb2 as sensors_pb2
import threading
import logging
import grpc
import time
import os

FORMAT = '%(asctime)s %(levelname)-5s: %(message)s'
lock = threading.Lock()

def save_reading(storage_service_ip, sensor: Sensor):
    response = None
    try:
        with grpc.insecure_channel(storage_service_ip + ":5051") as channel:
            stub = sensors_pb2_grpc.StorageServiceStub(channel)

            SensorReading = sensors_pb2.SensorReading()
            SensorReading.sensor_id=sensor.sensor_id,
            SensorReading.reading_type=sensor.reading_type,
            SensorReading.reading_value=sensor.reading_value,
            SensorReading.timestamp=sensor.timestamp
            
            response = stub.SaveReading(SensorReading)
    except Exception as error:
        logging.error(f"{sensor.sensor_id}: failed to save reading ({type(error).__name__})")
    if response == None:
        return False
    return response.status == "200"


class SensorManager():
    
    storage_service_ip = os.environ.get("STORAGE_SERVICE_IP", "127.0.0.1")
    sensors: dict[str, Sensor] = {}

    def PushReading(self, request, context):
        received = Sensor(request.sensor_id, request.reading_type, request.reading_value, request.timestamp)
        logging.info(f"{received.sensor_id}: data received ({received.reading_type} {received.reading_value} @ {received.timestamp})")
        with lock:
            self.sensors.update({received.sensor_id: received})
        if save_reading(self.storage_service_ip, received): # if persisted
            return sensors_pb2.Response(status="200")
        return sensors_pb2.Response(status="202") # only in memory

    def GetSensorData(self, request, context):
        logging.info(f"Data requested from {request.sensor_id}")
        latest_reading = self.sensors.get(request.sensor_id)
        SensorReading = sensors_pb2.SensorReading()
        SensorReading.sensor_id=latest_reading.sensor_id
        SensorReading.reading_type=latest_reading.reading_type
        SensorReading.reading_value=latest_reading.reading_value
        SensorReading.timestamp=latest_reading.timestamp
        return SensorReading

    def ListSensors(self, request, context):
        sensors_list = sensors_pb2.SensorsList()
        inactive = []
        with lock:
            logging.info("Sensors:")
            for sensor in self.sensors.values():
                logging.info(f"{sensor}")
                current_ts = int(time.time())
                sensor_ts = int(sensor.timestamp)
                sensor_id = sensor.sensor_id
                if (current_ts -  sensor_ts > 20): # after 20 sec inactivity: remove sensor
                    inactive.append(sensor.sensor_id)
                    continue
                if (current_ts - sensor_ts > 5): # after 5 seconds sensor becomes inactive
                    sensor.active = False
                sensors_list.sensor_ids.append(sensor_id)
            for id in inactive:
                inactive = self.sensors.pop(id)
                logging.info(f"{inactive.sensor_id}: deleted")
        return sensors_list


def serve():
    port = "5050"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensors_pb2_grpc.add_SensorManagerServicer_to_server(SensorManager(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info(f"Sensor Manager started on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    serve()

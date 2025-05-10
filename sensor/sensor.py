import grpc
import protos.sensors_pb2_grpc as sensors_pb2_grpc
import protos.sensors_pb2 as sensors_pb2
import logging
import random
import time
import os

FORMAT = '%(asctime)s %(levelname)-5s: %(message)s'

# Very simple device that sends sensor data periodically
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    sensor_id = "SENSOR-" + str(int(random.random() * 100000))
    channel_ip = os.environ.get("SMIP", "127.0.0.1")
    channel = grpc.insecure_channel(channel_ip + ":5050")
    logging.info(f"{sensor_id} started")
    while True:
        try: 
            timestamp = str(int(time.time()))
            stub = sensors_pb2_grpc.SensorManagerStub(channel)
            response = stub.PushReading(sensors_pb2.SensorReading(sensor_id=f"{sensor_id}", reading_type="timeseries", reading_value=random.random() * 40, timestamp=timestamp))
            trimmed_status = str.replace(response.status, "\n", "")
            logging.info(f"Data sent [{trimmed_status}]")
            time.sleep(random.random() * 15) # random 15 sec interval between readings
        except Exception as error:
            logging.error(f"Connection failed ({type(error).__name__})") # {type(error).__name__}
            break
    channel.close()
    logging.info(f"{sensor_id} stopped")


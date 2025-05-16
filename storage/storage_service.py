from concurrent import futures
from pymongo import MongoClient
import logging
import grpc
import os

import sensors_pb2_grpc as sensors_pb2_grpc
import sensors_pb2 as sensors_pb2

FORMAT = '%(asctime)s %(levelname)-5s: %(message)s'

mongo_uri = os.environ.get("DB_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client["sensor_data"]
collection = db["readings"]

class StorageService():

    def SaveReading(self,request, context):
        reading = {
            "sensor_id": request.sensor_id,
            "reading_type": request.reading_type,
            "reading_value": request.reading_value,
            "timestamp": request.timestamp
        }
        try:
            collection.insert_one(reading)
            logging.info(f"Reading saved to db: {reading}")
            return sensors_pb2.Response(status="200")
        except Exception as e:
            logging.error(f"Failed to store reading. Error: {e}")
            return sensors_pb2.Response(status="500")

    def GetHistory(self, request, context):
        sensor_id = request.sensor_id
        history = []
        try:
            results = collection.find({"sensor_id": sensor_id})
            for result in results:
                reading = sensors_pb2.SensorReading(
                    sensor_id = result["sensor_id"],
                    reading_type = result["reading_type"],
                    reading_value = result["reading_value"],
                    timestamp = result["timestamp"]
                )
                history.append(reading)
        except Exception as e:
            logging.error(f"Failed to query database: {e}")

        return sensors_pb2.SensorHistory(history=history)

def serve():
    port = "5051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensors_pb2_grpc.add_StorageServiceServicer_to_server(StorageService(), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    logging.info(f"Storage service started on port {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format=FORMAT)
    serve()
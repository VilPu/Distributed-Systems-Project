import grpc
import sensors_pb2_grpc


# gRPC channels & stubs for communication to microservices
# sensor_manager
sensor_channel = grpc.insecure_channel('localhost:5050')
sensors_stub = sensors_pb2_grpc.SensorManagerStub(sensor_channel)
# storage service
storage_channel = grpc.insecure_channel('localhost:5051')
storage_stub = sensors_pb2_grpc.StorageServiceStub(storage_channel)
# alert service
alert_channel = grpc.insecure_channel('localhost:5052')
alerts_stub = sensors_pb2_grpc.AlertServiceStub(alert_channel)

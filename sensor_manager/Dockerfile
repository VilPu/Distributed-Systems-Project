FROM python:3.10

ADD . .

ENV STORAGE_SERVICE_IP="storage-service"

RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. protos/sensors.proto

CMD ["python", "sensor_manager.py"]

FROM python:3.10

ADD . .

ENV DB_URI="mongo-db"

RUN pip install -r requirements.txt

RUN python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. sensors.proto

EXPOSE 5051

CMD ["python", "storage_service.py"]

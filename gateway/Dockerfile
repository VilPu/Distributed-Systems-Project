# official python image
FROM python:3.10


ENV USE_MOCK='false'
# install build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libffi-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# copy all the files from /gateway folder
COPY . . /gateway/
WORKDIR /gateway

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m grpc_tools.protoc --proto_path=. --python_out=. --grpc_python_out=. sensors.proto
EXPOSE 9000

CMD ["uvicorn", "gateway:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
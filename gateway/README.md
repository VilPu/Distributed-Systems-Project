# Gateway

Gateway will route client requests to separate microservices: 
 * Alert service
   * Get alerts from sensors
* Storage service
  * Get history entries from sensors
* Sensor manager
  * Get sensor details that are retrieved from each sensor

Run separately gateway app with mock responses locally:
* Install requirements
* Set environment variable USE_MOCK='true', in Windows powershell $env:USE_MOCK="true"
* Run command: uvicorn gateway:app --reload --port 9000
* Test endpoints with:
  *  curl http://localhost:9000/history/s1-temp
  * curl http://localhost:9000/sensors/s2-humid
  * curl http://localhost:9000/sensors
  * curl http://localhost:9000/sensors/s1-temp
  * curl http://localhost:9000/alerts
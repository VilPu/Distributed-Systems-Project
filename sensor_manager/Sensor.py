import time        

class Sensor():

    def __init__(self, id, reading_type, reading_value, timestamp=str(int(time.time()))):
        self.sensor_id = id
        self.reading_type = reading_type
        self.reading_value = reading_value
        self.timestamp = timestamp
        self.active = True

    def __str__(self):
        state = "inactive"
        if self.active:
            state = "active"
        return f"[{state}] {self.sensor_id}"

    def __eq__(self, value):
        if type(value) != Sensor:
            return False
        return self.sensor_id == value.sensor_id

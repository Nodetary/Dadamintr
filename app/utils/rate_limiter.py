from time import sleep
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.request_times = []
    
    def wait_if_needed(self):
        now = datetime.now()
        self.request_times = [t for t in self.request_times 
                            if now - t < timedelta(minutes=1)]
        
        if len(self.request_times) >= self.requests_per_minute:
            sleep_time = (self.request_times[0] + timedelta(minutes=1) - now).total_seconds()
            if sleep_time > 0:
                sleep(sleep_time)
        
        self.request_times.append(now) 
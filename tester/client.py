import requests
import time

class HTTPClientWrapper:
    def __init__(self, base_url, timeout=3.0, max_retries=1):
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries

    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        
        for attempt in range(self.max_retries + 1):
            start_time = time.time()
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                # Ensure we handle 429 Rate Limit
                if response.status_code == 429:
                    if attempt < self.max_retries:
                        time.sleep(1.0)  # simple backoff
                        continue
                    else:
                        latency = (time.time() - start_time) * 1000
                        return {"status_code": 429, "data": None, "latency_ms": latency, "error": "Rate limit exceeded"}
                
                # Check for 5xx server errors
                if 500 <= response.status_code < 600:
                    if attempt < self.max_retries:
                        time.sleep(1.0)
                        continue
                        
                latency = (time.time() - start_time) * 1000
                try:
                    data = response.json()
                except ValueError:
                    data = None
                    
                return {
                    "status_code": response.status_code,
                    "data": data,
                    "latency_ms": latency,
                    "error": None,
                    "headers": response.headers
                }
                
            except requests.exceptions.Timeout:
                if attempt < self.max_retries:
                    time.sleep(1.0)
                    continue
                latency = (time.time() - start_time) * 1000
                return {"status_code": None, "data": None, "latency_ms": latency, "error": "Timeout"}
            except requests.exceptions.RequestException as e:
                # Other connection errors
                if attempt < self.max_retries:
                    time.sleep(1.0)
                    continue
                latency = (time.time() - start_time) * 1000
                return {"status_code": None, "data": None, "latency_ms": latency, "error": str(e)}
        
        return {"status_code": None, "data": None, "latency_ms": 0, "error": "Max retries exceeded"}

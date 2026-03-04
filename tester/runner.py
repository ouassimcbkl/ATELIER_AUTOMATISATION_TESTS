import statistics
import math
from datetime import datetime
from .client import HTTPClientWrapper
from .tests import TESTS

def run_all_tests():
    client = HTTPClientWrapper("https://api.frankfurter.app")
    
    results = []
    latencies = []
    passed = 0
    failed = 0
    
    for name, test_func in TESTS:
        try:
            latency = test_func(client)
            results.append({"name": name, "status": "PASS", "latency_ms": round(latency, 2), "details": ""})
            latencies.append(latency)
            passed += 1
        except AssertionError as ae:
            results.append({"name": name, "status": "FAIL", "latency_ms": 0, "details": str(ae)})
            failed += 1
        except Exception as e:
            results.append({"name": name, "status": "FAIL", "latency_ms": 0, "details": str(e)})
            failed += 1
            
    total = passed + failed
    error_rate = failed / total if total > 0 else 0
    
    latencies.sort()
    avg_latency = statistics.mean(latencies) if latencies else 0.0
    p95_index = math.ceil(0.95 * len(latencies)) - 1
    if p95_index < 0:
        p95_index = 0
    p95_latency = latencies[p95_index] if latencies else 0.0
    
    run_data = {
        "api": "Frankfurter",
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": round(error_rate, 3),
            "latency_ms_avg": round(avg_latency, 2),
            "latency_ms_p95": round(p95_latency, 2)
        },
        "tests": results
    }
    return run_data

if __name__ == "__main__":
    import json
    print(json.dumps(run_all_tests(), indent=2))

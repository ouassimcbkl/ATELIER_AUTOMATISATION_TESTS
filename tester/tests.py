from .client import HTTPClientWrapper

def test_status_200(client):
    res = client.get("/latest")
    assert res.get("status_code") == 200, f"Expected 200, got {res.get('status_code')}"
    return res.get("latency_ms")

def test_content_type_json(client):
    res = client.get("/latest")
    assert res.get("status_code") == 200
    ctype = res.get("headers", {}).get("Content-Type", "")
    assert "application/json" in ctype, f"Expected JSON, got {ctype}"
    return res.get("latency_ms")

def test_mandatory_fields(client):
    res = client.get("/latest")
    data = res.get("data")
    assert data is not None, "Response data is empty"
    for field in ["amount", "base", "date", "rates"]:
        assert field in data, f"Missing field: {field}"
    return res.get("latency_ms")

def test_data_types(client):
    res = client.get("/latest")
    data = res.get("data")
    assert isinstance(data.get("amount"), (int, float)), "amount should be numeric"
    assert isinstance(data.get("base"), str), "base should be string"
    assert isinstance(data.get("date"), str), "date should be string"
    assert isinstance(data.get("rates"), dict), "rates should be object"
    return res.get("latency_ms")

def test_invalid_input_404(client):
    res = client.get("/latest", params={"from": "INVALID_CURRENCY"})
    assert res.get("status_code") == 404, f"Expected 404 for invalid input, got {res.get('status_code')}"
    assert res.get("data") is not None, "Expected error JSON"
    return res.get("latency_ms")

def test_robustness_timeout_handled(client):
    res = client.get("/this_route_does_not_exist")
    assert res.get("status_code") == 404, "Expected 404 for non-existent route"
    return res.get("latency_ms")

TESTS = [
    ("HTTP 200 OK", test_status_200),
    ("Content-Type JSON", test_content_type_json),
    ("Mandatory Fields", test_mandatory_fields),
    ("Data Types", test_data_types),
    ("Invalid Input 404", test_invalid_input_404),
    ("Route Not Found 404", test_robustness_timeout_handled)
]

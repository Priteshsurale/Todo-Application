from fastapi.testclient import TestClient
from ..main import app
from fastapi import status

client = TestClient(app)

def test_return_health_check():
    res = client.get('/healthy')
    assert res.status_code == status.HTTP_200_OK
    assert res.json() ==  {'status':'Healthy'}
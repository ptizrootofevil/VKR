import pytest
from fastapi.testclient import TestClient
import clickhouse_connect
import sys
import os

# Корень проекта - на уровень выше tests
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from api.main import app, client

def test_example():
    assert 1 + 1 == 2

def test_db_connection():
    assert client.query("SELECT version()").result_rows[0][0] == "25.11.2.24"


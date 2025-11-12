import os
from fastapi import FastAPI, HTTPException
import clickhouse_connect

# Чтение переменных окружения
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 9000))
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

# Подключение к ClickHouse
client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    user=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD
)

app = FastAPI()

@app.get("/")
async def root():
    result = client.execute("SELECT version()")
    return {"clickhouse_version": result[0][0]}

@app.get("/test")
async def test_query():
    client.execute("CREATE TABLE IF NOT EXISTS my_database.test_table (id UInt32, name String) ENGINE = MergeTree() ORDER BY id")
    client.execute("INSERT INTO my_database.test_table (id, name) VALUES", [(1, "test")])
    result = client.execute("SELECT * FROM my_database.test_table")
    return {"data": result}
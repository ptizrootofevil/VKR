import os
from fastapi import FastAPI, HTTPException
import clickhouse_connect

app = FastAPI()

# Чтение переменных окружения
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))  # HTTP-порт для clickhouse-connect
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "9y6bH73d")

# Подключение к ClickHouse
client = clickhouse_connect.get_client( #host='localhost', port=8123, username='default', password='9y6bH73d')
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD
)

@app.get("/")
async def root():
    # Пример запроса к ClickHouse
    result = client.query("SELECT version()")
    version = result.result_rows[0][0]
    return {"message": "FastAPI connected to ClickHouse", "clickhouse_version": version}

@app.on_event("startup")
async def startup_event():
    # Создание тестовой таблицы при старте
    client.command("""
        CREATE TABLE IF NOT EXISTS test_table (
            id UInt32,
            name String
        ) ENGINE = MergeTree()
        ORDER BY id
    """)

@app.get("/insert")
async def insert_data():
    client.command("INSERT INTO test_table (id, name) VALUES (1, 'Test')")
    return {"message": "Data inserted"}

@app.get("/select")
async def select_data():
    result = client.query("SELECT * FROM test_table")
    return {"data": result.result_rows}
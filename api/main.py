import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import clickhouse_connect

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Чтение переменных окружения
CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))  # HTTP-порт для clickhouse-connect
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "9y6bH73d")

# Подключение к ClickHouse
client = clickhouse_connect.get_client(
    host=CLICKHOUSE_HOST,
    port=CLICKHOUSE_PORT,
    username=CLICKHOUSE_USER,
    password=CLICKHOUSE_PASSWORD
)

@app.get("/", response_class=HTMLResponse)
async def root(request:Request):
    result = client.query("SELECT version()")
    version = result.result_rows[0][0]
    return templates.TemplateResponse(request=request,
                                      name="login.html",
                                      context={"version": version})

@app.get("/insert", response_class=HTMLResponse)
async def insert_data(request:Request):
    return templates.TemplateResponse("insert.html", {"request" : request})

@app.post("/insert")
async def insert_data_post(
    id: Annotated[int, Form()],
    name: Annotated[str, Form()],
    request:Request
):
    ic = client.create_insert_context(table='test_table')
    ic.data = [[id, name]]
    client.insert(context=ic)

    return templates.TemplateResponse("insert_complete.html", {"request" : request, 
                                                                "id" : id, 
                                                                "name" : name})

@app.get("/select", response_class=HTMLResponse)
async def select_data(request:Request):
    rows = []

    with client.query_row_block_stream("SELECT id, name from test_table order by id") as stream:
        for block in stream:
            for rec in block:
                rows.append([rec[0], rec[1]])
    
    return templates.TemplateResponse("select.html", {"request" : request,
                                                      "records" : rows} )



@app.get("/debug/tables")
async def debug_tables():
    # Показывает все таблицы
    result = client.query("SHOW TABLES FROM default")
    return {"tables": result.result_rows}
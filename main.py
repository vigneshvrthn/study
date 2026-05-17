from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import sqlite3

app = FastAPI()

# CORS - REQUIRED for Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Item(BaseModel):
    item_name: str
    item_value: int
    case_content: int

@app.post("/save")
def save_item(item: Item):
    try:
        conn = sqlite3.connect("testdb.db")
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO items (item_name, item_value, case_content)
            VALUES (?, ?, ?)
            """,
            (item.item_name, item.item_value, item.case_content)
        )

        conn.commit()
        conn.close()

        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/getData")
def get_data():
    conn = sqlite3.connect("testdb.db")
    df = pd.read_sql("SELECT * FROM items", conn)
    conn.close()
    return {"status": "success", "data": df.to_dict(orient="records")}



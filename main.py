from fastapi import FastAPI, HTTPException
import sqlite3
import logging
from fastapi.middleware.cors import CORSMiddleware
import re

logging.basicConfig(
    filename="logs/api_logs.log",
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    encoding="utf8",
)

DATABASE = "file:database.db?mode=ro"

PATTERN = r'^[a-zA-Z]+-\d{2}-\d{1}$'

OPT_NAMES = {
    "web": "Web-программирование",
    "BI": "Инструментальные средства BI",
    "Low-code": "Low-Code",
    "Linux": "Системное программирование в Linux"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return sqlite3.connect(DATABASE, uri=True, check_same_thread=False)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/groups/{group}")
async def get_group(group: str):
    try:
        if not re.match(PATTERN, group):
            raise HTTPException(status_code=400, detail="Invalid table name")
        
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM [{group}]")
        lessons = []
        for i in cur.fetchall():
            lessons.append({
            'id': i[0],
            'name': i[1],
            'teacher': i[2],
            'location': i[3],
            'group': i[4],
            'start': i[5],
            'end': i[6],
            })
        conn.close()
        return lessons
    except sqlite3.Error as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/groups/{group}/{id}")
@app.get("/subgroups/{group}/{subgroup}/{id}")
async def get_lesson(group: str, id: int):
    try:
        if not group.isidentifier():
            raise HTTPException(status_code=400, detail="Invalid table name")

        conn = get_db_connection()
        cur = conn.cursor()
        query = f"SELECT * FROM [{group}] WHERE id = ?"
        cur.execute(query, (id,))
        lesson = cur.fetchone()
        conn.close()
        
        if lesson is None:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        return {
            'id': lesson[0],
            'name': lesson[1],
            'teacher': lesson[2],
            'location': lesson[3],
            'group': lesson[4],
            'start': lesson[5],
            'end': lesson[6],
            'link': lesson[7]
        }
    except sqlite3.Error as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/subgroups/{group}/{subgroup}")
async def get_subgroup(group: str, subgroup: str):
    try:
        if not re.match(PATTERN, group):
            raise HTTPException(status_code=400, detail="Invalid table name")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM [{group}] WHERE subgroup = ?", (subgroup,))
        lessons = []
        for i in cur.fetchall():
            lessons.append({
            'id': i[0],
            'name': i[1],
            'teacher': i[2],
            'location': i[3],
            'group': i[4],
            'start': i[5],
            'end': i[6],
            'link': i[7]
            })
        conn.close()
        return lessons
    except sqlite3.Error as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database error")

@app.get("/optional/{name}")
async def get_optional(name: str):
    try:
        if not name in OPT_NAMES:
            raise HTTPException(status_code=400, detail="Invalid table name")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM [{OPT_NAMES.get(name)}]")
        lessons = []
        for i in cur.fetchall():
            lessons.append({
            'id': i[0],
            'name': i[1],
            'teacher': i[2],
            'location': i[3],
            'group': i[4],
            'start': i[5],
            'end': i[6],
            'link': i[7]
            })
        conn.close()
        return lessons
    except sqlite3.Error as e:
        logging.error(e)
        raise HTTPException(status_code=500, detail="Database error")
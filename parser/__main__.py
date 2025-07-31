from config import *
from parser.parser_modules.Lessons import Lessons
from parser.parser_modules.Lessons import Lesson
from parser.parser_modules.Timetable import Timetable
import datetime
import logging
import sqlite3
from time import sleep

logging.basicConfig(
    filename="logs/parser_logs.log",
    level=logging.INFO,
    format=" %(asctime)s - %(levelname)s - %(message)s",
    encoding="utf8",
)

UPDATE_TIME = 7200

timetable = Timetable()

while True:
    try:
        logging.info("--START--")


        start_time = datetime.datetime.now()

        timetable.update_timetable()

        conn = sqlite3.connect("database.db")
        conn.execute("PRAGMA journal_mode=WAL;")
        cur = conn.cursor()

        for group in groups:
            cur.execute(
                f"""
                        CREATE TABLE IF NOT EXISTS [{group['id']}] (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT,
                            teacher TEXT,
                            location TEXT,
                            subgroup TEXT,
                            start TEXT,
                            end TEXT,
                            link TEXT
                            )
                """
            )
            start_time_gr = datetime.datetime.now()
            lessons = Lessons(group)
            for workbook in timetable.get_workbooks():
                if not f"{group.get('course')} курс" in workbook.sheetnames:
                    continue
                worksheet = workbook[f"{group.get('course')} курс"]
                lessons.add_lessons_from_sheet(worksheet)
                
            cur.execute(f"SELECT * FROM [{group['id']}]")
            prev_timetable = []
            tuple = cur.fetchall()
            
            if len(tuple) >=1:
                for ls_info in tuple:
                    ls = Lesson().from_tuple(ls_info)
                    prev_timetable.append(ls)

            sep_lessons = lessons.get_lessons_dict(prev_timetable)
            for ls in sep_lessons["to_add"]:
                cur.execute(f"INSERT INTO [{group['id']}] (name, teacher, location, subgroup, start, end, link) VALUES (?, ?, ?,?,?,?,?)", ls.get_tuple())


            for ls in sep_lessons["to_del"]:
                cur.execute(f"DELETE FROM [{group['id']}] WHERE id = ?", (ls.id,))
                
            conn.commit()

            logging.info(
                f"{group['name']} calendar updated({datetime.datetime.now() - start_time_gr})"
            )

        duration = datetime.datetime.now() - start_time
        logging.info(f"all groups updated({duration.total_seconds()} seconds)")
        conn.close()
        sleep(600)
    except Exception as e:
        logging.exception(e)
        sleep(30)



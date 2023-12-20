from db import db
from sqlalchemy import text


def new_message(content: str):
    try:
        sql = "INSERT INTO messages (content) VALUES (:content)"
        db.session.execute(sql, {"content":content})
        db.session.commit()
        return True
    except:
        return False
    
def get_all_messages():
    sql = text("SELECT id, content FROM messages")
    result = db.session.execute(sql)
    all_messages = result.fetchall()
    return all_messages

def get_messages():
    pass


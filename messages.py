from db import db
from sqlalchemy import text


def new_message(content: str, creator_id: int):
    try:
        sql = text("INSERT INTO messages (content, creator_id) VALUES (:content, :creator_id)")
        db.session.execute(sql, {"content":content, "creator_id":creator_id})
        db.session.commit()
        return True
    except:
        return False
    
def get_all_messages():
    sql = text("SELECT content FROM messages")
    result = db.session.execute(sql)
    all_messages = result.fetchall()
    return all_messages

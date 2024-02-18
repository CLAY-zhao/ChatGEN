import builtins

from chatglm_cpp_serve import chatglm_server
from db import SQLiteDatabase
from utils import cache

import openai

openai.api_key = ""
openai.api_base = "http://127.0.0.1:9000/v1"


class Sqlite3JSAPI(object):

  def __init__(self) -> None:
    self.db = builtins.__dict__.get("__sqlite__", SQLiteDatabase())

  def api_open_db(self):
    ok = self.db.initialize_database()
    return {"ok": ok}

  def api_db_exist(self):
    return {"db": self.db.is_exist()}

  def api_db_move(self, database_path):
    pass

  def api_db_query(self):
    if self.db.is_exist():
      self.db.open_connection()
      rows = self.db.select_configuration()
      return {row["key"].lower(): row["value"] for row in rows}
    else:
      return None

  def api_db_update(self, kwargs_dict):
    # personal_settings: str, imagination: float, top_p: float
    for key, value in kwargs_dict.items():
      self.db.update_configuration(key.upper(), value)
      cache[key.upper()] = value

    return {"ok": True}


class JSAPI(Sqlite3JSAPI):

  def api_chatglm_cpp(self):
    chatglm_server.chatglm_cpp_startup()

  def api_update_global_config(self, config):
    import time
    time.sleep(3)
    print(config)

  def query_question(self, question):
    personal_settings = cache.get("PERSONAL_SETTING", None)
    temperature = cache.get("IMAGINATION", 1)
    top_p = cache.get("TOP_P", 1)
    
    if personal_settings:
      messages = [
        {
          "role": "system",
          "content": personal_settings
        },
        {
          "role": "user",
          "content": question
        }
      ]
    else:
      messages = [
        {
          "role": "user",
          "content": question
        }
      ]

    completion = openai.ChatCompletion.create(
      model="default-model",
      temperature=temperature,
      top_p=top_p,
      messages=messages
    )
    respond = completion.choices
    return respond[0]["message"]["content"]

  def test_alert(self, msg):
    print(msg)

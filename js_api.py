import base64
import builtins
import re
from urllib.parse import unquote

from chatglm_cpp_serve import chatglm_server
from db import SQLiteDatabase
from utils import cache

import openai
import requests

openai.api_key = ""
openai.api_base = "http://127.0.0.1:9000/v1"

headers = {
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}


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
  

class RequestJSAPI(object):

  def api_magnet_search(self, keyword: str, page: int = 1):
    url = f"http://clg6.icu/search?word={keyword}&p={page}"
    response = requests.get(url, headers=headers, timeout=60)
    encoder = re.search(r"window\.atob\(\"(.*?)\"\)", response.text, re.S)
    if not encoder:
      return {"ok": False, "list": []}
    
    encoder_text = encoder.group(1)
    encoded = base64.b64decode(encoder_text)
    deocded = unquote(encoded.decode("utf-8"), encoding="utf-8")

    titles = re.findall(r"class=\"SearchListTitle_result_title\">(.*?)</a>", deocded, re.S)
    links = re.findall(r"<a style=\"border-bottom:none;\" href=\"(.*?)\"", deocded, re.S)
    infos = re.findall(r"<i class=\"iconfont icon-citie Search_icon_citie\"></i>(.*?)</div>", deocded, re.S)

    content = [{"title": title, "link": link, "info": info} for title, link, info in zip(titles, links, infos)]
    return {"ok": True, "list": content}
  
  def api_magnet_info(self, link):
    url = f"http://clg6.icu{link}"
    response = requests.get(url, headers=headers, timeout=60)
    encoder = re.search(r"window\.atob\(\"(.*?)\"\)", response.text, re.S)
    if not encoder:
      return {"ok": False, "info": {}}
    
    encoder_text = encoder.group(1)
    encoded = base64.b64decode(encoder_text)
    deocded = unquote(encoded.decode("utf-8"), encoding="utf-8")

    magnet_url = re.search(r"id=\"down-url\">(.*?)</a>", deocded, re.S)
    if not magnet_url:
      return {"ok": False, "info": {}}
    
    down_url = magnet_url.group(1)

    metas = re.findall(r"<div class=\"File_list_info\">(.*?)<div class=\"File_btn\">(.*?)</div>", deocded, re.S)
    meta_data = [{"title": title, "size": size} for title, size in metas]

    return {"ok": True, "info": {"down_url": down_url, "meta": meta_data}}


class JSAPI(Sqlite3JSAPI, RequestJSAPI):

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

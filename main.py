import builtins

import cache
from js_api import JSAPI
from db import SQLiteDatabase
from utils import check_chatglm_cpp, cache

import webview

localization = {
  "global.quitConfirmation": u'确定关闭吗?'
}


def have_runtime() -> bool:
  # check exist? webview2 runtime
  from webview.platforms.winforms import _is_chromium
  return _is_chromium()


def install_runtime() -> None:
  # install webview2 runtime
  # https://go.microsoft.com/fwlink/p/?LinkId=2124703
  import os
  import subprocess
  from urllib import request
  url = "https://go.microsoft.com/fwlink/p/?LinkId=2124703"
  path = os.getcwd() + "\\webview2runtimesetup.exe"
  unit = request.urlopen(url).read()
  with open(path, "wb") as file:
    file.write(unit)
  process = subprocess.Popen(path, shell=True)
  return_code = process.wait() # wait child thread end
  os.remove(path)
  return return_code


def created() -> None:
  if not have_runtime():
    install_runtime()

  builtins.__dict__["__sqlite__"] = db = SQLiteDatabase()
  if db.is_exist():
    db.open_connection()
    rows = db.select_configuration()
    for row in rows:
      cache[row["key"]] = row["value"]


class WebView(object):

  def __init__(self,debug: bool = False):
    self.debug = debug
    self.window = None

  def create(self):
    self.window = webview.create_window(
      title="Chat Baby", url='http://localhost:8080/', js_api=JSAPI(), width=1920, height=1080,
      background_color='#2c3e50', confirm_close=True
    )
    builtins.__dict__["__webview__"] = self

  def __call__(self):
    self.create()
    cache.STATE = check_chatglm_cpp()
    webview.start(created, localization=localization, debug=self.debug)

  def alert(self, message):
    self.window.evaluate_js(f"alert({message})")


def main() -> None:
  view = WebView(debug=False)
  view()


if __name__ == '__main__':
  main()

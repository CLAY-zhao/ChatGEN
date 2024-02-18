import builtins
from cachetools import Cache
import socket

cache = Cache(maxsize=128)


def get_webview():
  return builtins.__dict__.get("__webview__", None)


def check_chatglm_cpp():
  from chatglm_cpp_serve import chatglm_server

  host = chatglm_server.host
  # port = chatglm_server.port
  port = 10000

  try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
  except (socket.timeout, ConnectionRefusedError):
    return False
  finally:
    sock.close()

  return True

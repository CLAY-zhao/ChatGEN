import os
from typing import Union
from threading import Thread

from utils import get_webview

import uvicorn


class ChatGLMServer(object):

  def __init__(self) -> None:
    self.host = "127.0.0.1"
    self.port = 9000
    self.enable = False
    self.chatglm_cpp_startup()
    self.enable = True

  def chatglm_cpp_startup(self) -> None:
    if not self.enable:
      os.environ["MODEL"] = "chatglm3-ggml.bin"
      serve = lambda: uvicorn.run(
        "chatglm_cpp.openai_api:app", host=self.host, port=self.port, log_level="info"
      )
      chatglm_thread = Thread(target=serve)
      chatglm_thread.daemon = True
      chatglm_thread.start()
    self.enable = True

  @property
  def host(self) -> str:
    return self.__host
  
  @host.setter
  def host(self, host: str):
    self.__host = host

  @property
  def port(self) -> Union[int, str]:
    return self.__port
  
  @port.setter
  def port(self, port: int):
    if isinstance(port, str):
      if not port.isdigit():
        raise ValueError("Invalid port number!")
    self.__port = int(port)


chatglm_server = ChatGLMServer()

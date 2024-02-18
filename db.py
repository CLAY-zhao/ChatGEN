import sqlite3
import os


def create_table(cursor, table_name: str, columns: str) -> None:
  cursor.execute(f"CREATE TABLE {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})")


class SQLiteDatabase(object):

  def __init__(self, database_path: str = "chatgen.db"):
    self.__database_path = database_path
    self.connect = None
    self.cursor = None
    # self.open_connection()

  def initialize_database(self):
    if not os.path.exists(self.database_path):
      try:
        self.connect = sqlite3.connect(self.database_path, check_same_thread=False)
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()
      
        create_table(
          self.cursor,
          'configuration',
          'key TEXT, value TEXT, desc TEXT'
        )
        self.insert_configuration('PERSONAL_SETTING', "我希望你是一个老师的角色, 回答我时可以温柔一点, 带点凶凶的, 说话干净利索")
        self.insert_configuration('IMAGINATION', 1.0)
        self.insert_configuration('TOP_P', 1.0)

        self.connect.commit()
      except sqlite3.Error:
        return False
    
    return True
  
  def select_configuration(self):
    try:
      self.cursor.execute(
        'SELECT key, value FROM configuration'
      )
      return self.cursor.fetchall()
    except (sqlite3.OperationalError, AttributeError):
      return {}
  
  def insert_configuration(self, key, value, desc=""):
    self.cursor.execute(
      'INSERT INTO configuration (key, value, desc) VALUES (?, ?, ?)',
      (key, value, desc)
    )
    self.connect.commit()

  def update_configuration(self, key, value):
    self.open_connection()
    self.cursor.execute(
      f'UPDATE configuration SET value = ? WHERE key = ?',
      (value, key)
    )
    self.connect.commit()

  def open_connection(self):
    if self.connect is None:
      self.connect = sqlite3.connect(self.database_path, check_same_thread=False)
      self.connect.row_factory = sqlite3.Row
      self.cursor = self.connect.cursor()
  
  def close_connection(self):
    if self.connect:
      self.connect.close()
      self.connect = None
      self.cursor = None

  def clear_database(self):
    if os.path.exists(self.database_path):
      self.close_connection()
      try:
        os.remove(self.database_path)
      except FileNotFoundError:
        return None

    return self.initialize_database()

  def is_exist(self):
    return os.path.exists(self.database_path)

  @property
  def database_path(self):
    return self.__database_path
  
  @database_path.setter
  def database_path(self, database_path: str):
    if not isinstance(database_path, str):
      self.__database_path = "chatgen.db"
    self.__database_path = database_path

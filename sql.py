import pymysql
import json

class mysql:

    def __init__(self, user, dbname,config_path="/web/config"):
        self.__sql = None
        self.__user = user
        self.__dbname = dbname

        self.link(config_path)
    
    def __read_config(self, config_path):
        with open(config_path, "r") as config:
            return json.loads(config.read())[self.__user]
        
    def link(self, config_path):
        passwd = self.__read_config(config_path)
        self.__sql = pymysql.Connect(host="127.0.0.1", user=self.__user, passwd=passwd, db=self.__dbname)
    
    def _exec(self, mode, sql_comm, data=[]):
        with self.__sql.cursor() as cursor:
            if mode == "read":
                sql_return = []
                cursor.execute(sql_comm)
                sql_return = cursor.fetchall()
            
            if mode == "write":
                sql_return = cursor.executemany(sql_comm, data)
        
        return sql_return
    
    def exec(self, sql_comm):
        with self.__sql.cursor() as cursor:
            cursor.execute(sql_comm)
            self.__sql.commit()
    
    def read(self, table, where=""):
        if where == "":
            sql_comm = f"SELECT * FROM `{table}`"
        else:
            sql_comm = f"SELECT * FROM `{table}` WHERE {where}"

        return self._exec("read", sql_comm)
    
    def write(self, table, key_list, data):
        key_str, val_str = "", ""
        if len(key_list) != 1:
            for key_in in range(0, len(key_list)):
                if key_in >= len(key_list) -1:
                    key_str += "`%s`" % key_list[key_in]
                    val_str += "%s"
                    break

                key_str += "`%s`, " % key_list[key_in]
                val_str += "%s, "
        else:
            key_str += "`%s`" % key_list[0]
            val_str += "%s"

        sql_comm = f"INSERT INTO `{table}` ({key_str}) VALUES ({val_str})"
        return self._exec("write", sql_comm, data)
    
    def __enter__(self):
        return self
    
    def __exit__(self, type, val, tra):
        self.__sql.commit()
        self.__sql.close()
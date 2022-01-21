import os
import time


class Log:

    def __init__(self, log_path):
        log_file_name = time.strftime("%Y_%m_%d.log", time.localtime())
        self.__log_path = os.path.join(log_path, log_file_name)

        if not os.path.isdir(log_path):
            os.makedirs(log_path)
        
        self.__log = open(self.__log_path, "a")
    
    def __set_log(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
    
    def write(self, log):
        self.__log.write("[%s] %s\n" % (self.__set_log(), log))
        self.__log.flush()

    def close(self):
        self.__log.close()
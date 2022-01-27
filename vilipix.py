import pymysql
from img.vilipix_api import Img
from sql import mysql
from info.log import Log
import time
    

time.sleep(1)
log = Log("/var/log/py")

# http://img3.vilipix.com
ORIGINAL_IMG = "{img_data}/picture/pages/original"
ADD_TABLE = "CREATE TABLE `%s`.`%s` ( `id` TEXT NOT NULL , `url` TEXT NOT NULL , `tag` TEXT NOT NULL ) ENGINE = InnoDB"
dbname = "vilipix"

stime = time.strftime("%Y %m %d %w", time.localtime())
y, m, d, w = stime.split(" ")

img = Img(time.strftime("%Y%m%d", time.localtime(time.time() - 86400 * 2)))
img.daily()
log.write("准备爬取每日榜单")
img.weekly()
log.write("准备爬取每周榜单")
img.monthly()
log.write("准备爬取每月榜单")


with mysql("api", dbname) as sql:

    def save_data(mode, data, dtime):
        table = "%s" % (dtime)
        add_table_comm = ADD_TABLE % (dbname, dtime)
        try:
            sql.exec(add_table_comm)
            log.write("添加数据表: %s" % table)
        except pymysql.err.OperationalError:
            pass
        
        add_data, add_id = [], []
        for img in data:
            in_img = sql.read("img_id", "id = %s" % img["id"])
            if in_img == ():
                img_data = ORIGINAL_IMG.format(img_data=img["regular_url"].split("/picture")[0])
                try:
                    day_url = img["regular_url"].split("regular")[1].split(img["id"])[0]
                    img_file_name = "%s_p0.%s" % (img["id"], img["regular_url"].split(".")[-1])
                    url = img_data + day_url + img_file_name
                except  IndexError:
                    url = img["regular_url"]
                add_data.append([img["id"], url, img["tags"]])
                add_id.append(img["id"])
        
        add_img = sql.write(table, ["id", "url", "tag"], add_data)
        if add_img != None:
            log.write("%s数据表 成功添加 %s 条数据" % (table, add_img))

            add_img = sql.write("img_id", ["id"], add_id)
            log.write("img_id 成功添加 %s 条数据" % add_img)

    log.write("开始爬取")
    img.run_task(save_data)

log.write("执行完毕!")
log.close()

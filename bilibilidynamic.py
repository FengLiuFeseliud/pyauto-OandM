import requests
import json
from sql import mysql
from info.log import Log


log = Log("/var/log/py")


get_user_uid_list = [
    "233114659",
    "205889201"
]

API = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={uid}"


log.write("开始自动爬取动态...")

dynamic_data = []
with mysql("api", "api") as sql:
    for uid in get_user_uid_list:
        in_ = False
        for link in range(1, 4):
            log.write("开始爬取 uid:%s 动态..." % uid)
            with requests.get(API.format(uid=uid)) as req:
                data = req.json()
                if data["code"] != 0:
                    log.write("爬取 uid:%s 动态失败 重试%s次..." % (uid, link))
                    continue
                
                in_ = True
                for data_card in data["data"]["cards"]:
                    json_data = json.loads(data_card["card"])
                    if data_card["desc"]["type"] == 64:
                        id = json_data["id"]
                        dynamic_url = "https://www.bilibili.com/read/cv%s" % id
                    else:
                        dynamic_url = "https://t.bilibili.com/%s" % data_card["desc"]["dynamic_id_str"]

                    sql_read_data = sql.read("blhx_dynamic", "url = '%s'" % dynamic_url)
                    if sql_read_data != ():
                        continue

                    dynamic_data.append([dynamic_url, json_data])

                log.write("爬取 uid:%s 动态 成功! 已经爬取 %s条" % (uid, len(dynamic_data)))
                break
        
        if not in_:
            log.write("爬取 uid:%s 动态失败!" % uid)

if len(dynamic_data) == 0:
    log.write("没有数据更新...")
    exit()


log.write("开始保存数据...")

save_data = []
for data in dynamic_data:

    img_list = []
    try:
        text = data[1]["item"]["description"]
        time = data[1]["item"]["upload_time"]
        time = data[1]["item"]["upload_time"]
        user = data[1]["user"]["name"]
        user_head = data[1]["user"]["head_url"]
        url = data[0]

    except KeyError:
        try:
            text = data[1]["item"]["content"]
            time = data[1]["item"]["timestamp"]
            user = data[1]["user"]["uname"]
            user_head = data[1]["user"]["face"]
            url = data[0]
            log.write("下载动态完成!")
            save_data.append([user, text, user_head, ",".join(img_list), url, time])
            continue
            
        except KeyError:
            text = data[1]["title"] + "\n" + data[1]["summary"]
            time = data[1]["publish_time"]
            user = data[1]["author"]["name"]
            user_head = data[1]["author"]["face"]
            url = data[0]

    log.write("下载动态图片...")

    if "item" in data[1]:
        img_url_list = data[1]["item"]["pictures"]
    else:
        img_url_list = data[1]["image_urls"]

    for img in img_url_list:
        if "img_src" in img:
            img_name = img["img_src"].rsplit("/", maxsplit=1)[-1]
            img_url = img["img_src"]
        else:
            img_name = img.rsplit("/", maxsplit=1)[-1]
            img_url = img

        with requests.get(img_url) as req:
            with open("/web/img/dynamic/blhx/%s" % img_name, "wb") as file:
                file.write(req.content)
                img_list.append("https://img.sakuratools.top/dynamic/blhx/%s@0x0x0x80" % img_name)
    log.write("下载动态完成!")
    
    save_data.append([user, text, user_head, ",".join(img_list), url, time])

count = 0
log.write("数据写入数据库...")
with mysql("api", "api") as sql:
    sql.write("blhx_dynamic", ["user", "text", "user_head", "img", "url", "time"], save_data)
    count += 1

log.write("数据库写入%s条数据!" % count)
log.write("执行完毕!")
log.close()
    

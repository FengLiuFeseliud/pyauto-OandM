import requests
from info.log import Log

log = Log("/var/log/py")

for link in range(0, 3):
    with requests.get("http://wthrcdn.etouch.cn/weather_mini?city=%E4%B8%8A%E6%B5%B7") as req:
        data = req.json()
        if data["status"] != 1000:
            log.write("更新天气失败 重试...")
            continue

        data = data["data"]["forecast"][0]
        fengli = data["fengli"].split("[")[-1].split("]")[0]
        wthrcdn = "%s %s %s %s%s" % (
            data["high"], data["low"], data["type"], data["fengxiang"], fengli)

        with open("wthrcdn.txt", "w") as file:
            file.write(wthrcdn)

        log.write("更新天气完成!")
        log.close()
        exit()

log.write("更新天气三次重试全部失败 请检查网络...")
log.close()
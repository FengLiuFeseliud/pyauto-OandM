# pyauto-OandM

运行于 sakuratools.top 的 python 自动化运维脚本

仅在本机运行测试 （环境：Linux Debian 11，python 3.9）

全部脚本需 root 运行

使用 crontab 命令进行定时运行

以下是我的配置，` crontab -e` 设置定时任务， `crontab -l` 查看定时任务

```bash
# 每天12点整自动抓取 vilipix 榜单
0 0 * * * python3 /web/py/vilipix.py
# 每小时获取一次指定地区天气保存在 wthrcdn.txt (这里的数据我是准备放在主页的)
0 */1 * * * python3 /web/py/wthrcdn.py
# 每小时更新一次 github hosts 保存至 hosts 文件
0 */1 * * * python3 /web/py/autohosts.py
# 每天3点30分自动备份指定目录, mysql数据库
30 3 * * * python3 /web/py/autobackup.py
```

统一保存同一天日志文件，默认日志目录`/var/log/py`

脚本会不定时更新添加！

## 脚本目录

> ### vilipix.py 自动抓取 vilipix 三榜
>
> ### wthrcdn.py 自动获取一次指定地区天气
>
> ### autohosts.py 自动更新 github hosts 保存至 hosts 文件
>
> ### autobackup.py 自动备份指定目录, mysql数据库
>
> 




import requests
import os
from info.log import Log

log = Log("/var/log/py")
log.write("准备自动更新 github hosts")

# 默认 hosts
hosts = """
127.0.0.1       localhost
127.0.1.1       sakura-linux

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters

""".split("\n")

# hosts 文件路径
hosts_path = "/etc/hosts"

log.write("获取 github hosts")
write_in = False


for link in range(1, 4):

    # github hosts 源自 https://github.com/521xueweihan/GitHub520
    with requests.get("https://raw.hellogithub.com/hosts") as req:
        with open("/etc/hosts", "w") as hosts_file:
            if req.status_code != 200:
                log.write("无法获取 github hosts 重试%s次" % link)
                continue
            
            log.write("获取 github hosts 成功! 进行写入")
            for host in hosts:
                hosts_file.write(host + "\n")
            
            hosts_file.write(req.text)

            log.write("写入 hosts 文件完成!")
            write_in = True
            break


if not write_in:
    log.write("未成功写入 hosts ...")
    exit()


# 一般直接生效, 这里避免意外刷新 hosts
log.write("刷新激活生效 hosts")
for reset in range(0, 2):
    code = os.system("systemctl restart nscd")
    if code != 0:
        log.write("无法刷新 hosts 尝试安装 nscd")
        # apt 为 debain 包管理器, 其他 Linux 发行版注意修改
        code = os.system("apt -y install nscd")
        continue

    log.write("刷新激活生效 hosts 成功!")
    exit()

log.write("未成功刷新激活生效 hosts ...")
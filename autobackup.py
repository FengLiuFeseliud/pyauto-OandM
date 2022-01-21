import os
import time
from sys_api.io import io
from info.log import Log

log = Log("/var/log/py")

backup_dir_list = [
    "/etc",
    "/web",
    "/var/log/mysql",
    "/var/log/nginx",
    "/home",
    "/root",
]

backup_mysql_dbnaem_list = [
    "api",
    "vilipix",
]

backup_save_sdb = "/dev/sdb"
backup_sdb_mount_path = "/mnt/sdb"
backup_save_path = "/mnt/sdb/auto-backup"
cache_path = "/data/autobackup_cache"

log.write("进行自动备份...")
backup_mysql_dir = cache_path + "/mysql_dbname"

log.write("备份 mysql 数据库, 创建文件夹: %s" % backup_mysql_dir)
os.makedirs(backup_mysql_dir)

log.write("开始备份数据库...")
os.system("mysqlhotcopy %s %s" % (
    " ".join(["'%s'" % dbnaem for dbnaem in backup_mysql_dbnaem_list]),
    backup_mysql_dir
))

log.write("mysql 备份完成!")

log.write("挂载存储硬盘 %s 至: %s" % (backup_save_sdb, backup_sdb_mount_path))
with io(backup_save_sdb , backup_sdb_mount_path, cache_path) as io_:
    for backup_div in backup_dir_list:
        code = io_.cp(os.path.abspath(backup_div))
        if code != 0:
            log.write("无法复制目标备份目录 %s %s" % (backup_div, code))
            continue
        
        log.write("复制 %s..." % backup_div)

    if len(os.listdir(cache_path)) - 1 != len(backup_dir_list):
        log.write("无法复制所有备份目录...")
    else:
        log.write("全部复制成功!")


    log.write("准备打包 cache_path !")

    io_.set_save_path(backup_save_path)
    code = io_.compress_dir(cache_path, time.strftime("%Y%m%d_backup", time.localtime()))
    if code != 0:
        log.write("严重错误 无法打包备份目录!!!")
        exit()
    
    log.write("卸载存储硬盘 %s ..." % backup_save_sdb)


log.write("成功自动备份以下目录")
log.write(",".join(backup_dir_list))

code = os.system(f"rm -rf '{cache_path}'")
if code != 0:
    log.write("无法删除打包缓存目录... code: %s" % code)
    exit()
    
log.write("删除打包缓存目录!")
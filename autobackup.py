import os
import time
from sys_api.io import io
from info.log import Log

log = Log("/var/log/py")

# 需备份的目录
backup_dir_list = [
    "/etc",
    "/web",
    "/var/log/mysql",
    "/var/log/nginx",
    "/home",
    "/root",
]

# 需备份的mysql 数据库
backup_mysql_dbnaem_list = [
    "api",
    "vilipix",
]

# 存储硬盘设备
backup_save_sdb = "/dev/sdb"
# 存储硬盘挂载目录
backup_sdb_mount_path = "/mnt/sdb"
# 备份包保存目录
backup_save_path = "/mnt/sdb/auto-backup"
# 备份包有效时间 天
backup_save_day_count = 7
# 打包缓存目录
cache_path = "/data/autobackup_cache"
# mysql 数据库备份文件夹名
backup_mysql_dir = cache_path + "/mysql_dbname"


log.write("进行自动备份...")
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

    backup_list = os.listdir(backup_save_path)
    if len(backup_list) != 0:
        backup_last_day = min([int(backup_day.split("_")[0]) for backup_day in backup_list])
        log.write("最后一天备份包为: %s" % backup_last_day)

    if int(time.strftime("%Y%m%d", time.localtime())) - backup_save_day_count >  backup_last_day:
            backup_last_name = os.path.join(backup_save_path, "%s_backup.tar.gz" % backup_last_day)
            log.write("备份包 %s 超出有效时间准备删除..." % backup_last_name)

            os.remove(backup_last_name)
            log.write("备份包 %s 删除成功!" % backup_last_name)

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
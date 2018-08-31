import os
import redis
import time

import config
from sendMail.sendMail import Sendmail

pool = redis.ConnectionPool(host=config.redis_host, port=config.redis_port)
db_redis = redis.Redis(connection_pool=pool, encoding='utf-8')

start_time = int(time.time())

while True:
    org_list_length = db_redis.llen("org_list")
    if not org_list_length:
        break
    cmd = "python begin.py"
    print(cmd)
    os.system(cmd)

end_time = int(time.time())
duration = (end_time - start_time)

# 构造邮件内容
msg = 'crawl mooc task done,'
msg = msg + '耗时%d秒,' % duration
msg = msg + "共成功处理了%d个item," % (db_redis.llen("course_list"))
msg += "\n以下item处理失败:\n"
failed_course_item_num = db_redis.llen("failed_course_item")
for i in range(0, failed_course_item_num):
    failed_course_item = db_redis.lindex("failed_course_item", i).decode("utf8")
    msg += (failed_course_item + "\n")

mail = Sendmail(config.mail_host, config.mail_user, config.mail_pwd, config.mail_sender)
mail.sendMail(["GSXxg5201314@outlook.com"], msg, "crawl mooc task reminder", "plain")

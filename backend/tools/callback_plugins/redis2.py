#!/opt/pyenv/versions/SA2/bin/python
#coding:utf-8
#__time__: 2020/4/2 13:31
#__author__ = 'ren_mcc'

import redis, json, datetime
from ansible.plugins.callback import CallbackBase
# 指定 redis 相关信息
REDIS_ADDR = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PD = ''    # redis 密码，这里为空，
ansible_result_redis_db = 2    # 存入 redis db10 中

class CallbackModule(CallbackBase):
    """
    这个插件会将执行结果保存到 redis
    """
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'redis2'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.id = 'ansible_execs_%s' % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.r = redis.Redis(host=REDIS_ADDR, port=REDIS_PORT, password=REDIS_PD, db=ansible_result_redis_db)

    def _write_to_save(self, data):  # 写入 redis ，调用 rpush 进行 redis 的 list 操作
        msg = json.dumps(data, ensure_ascii=False)
        self.r.rpush(self.id, msg)
        # 为了方便查看，我们 print 写入 redis 的字符串的前 50 个字符
        # print("\33[34m写入RedisKey：%s\33[0m" % self.id)

    def v2_playbook_on_play_start(self, play):
        name = play.get_name().strip()
        if not name:
            msg = u"PLAY"
        else:
            msg = u"PLAY [%s]" % name
        print(msg)

    def v2_runner_on_ok(self, result, **kwargs):
        "处理成功任务，跳过 setup 模块的结果"
        host = result._host
        if "ansible_facts" in result._result.keys():    # 我们忽略 setup 操作的结果
            print("\33[32mSetUp 操作，不Save结果\33[0m")
        else:
            self._write_to_save({
                "host": host.name,
                "result": result._result,
                "task": result.task_name,
                "status": "success"
            })
    def v2_runner_on_failed(self, result, ignore_errors=False, **kwargs):
        "处理执行失败的任务，有些任务失败会被忽略，所有有两种状态"
        host = result._host
        if ignore_errors:
            status = "ignoring"
        else:
            status = 'failed'
        self._write_to_save({
                "host": host.name,
                "result": result._result,
                "task": result.task_name,
                "status": status
            })
    def v2_runner_on_skipped(self, result, *args, **kwargs):
        "处理跳过的任务"
        host = result._host
        self._write_to_save({
                "host": host.name,
                "result": result._result,
                "task": result.task_name,
                "status": "skipped"
            })
    def v2_runner_on_unreachable(self, result, **kwargs):
        "处理主机不可达的任务"
        host = result._host
        self._write_to_save({
                "host": host.name,
                "result": result._result,
                "task": result.task_name,
                "status": "unreachable"
            })
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.utils.ssh_functions import check_for_controlpersist
import ansible.constants as C
import redis
import datetime


class ResultCallback(CallbackBase):
    "Ansible Api 和 Ansible Playbook V2 api 调用该CallBack"
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'stdout'

    def __init__(self, *args, **kwargs):     # 初始化时要求传入任务 id
        super(ResultCallback, self).__init__()
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        self.task_ok[result._host.get_name()]  = result._result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        self.task_failed[result._host.get_name()] = result._result

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result._result

    def v2_runner_on_skipped(self, result):
        self.task_ok[result._host.get_name()]  = result._result

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
               "ok":t['ok'],
               "changed" : t['changed'],
               "unreachable":t['unreachable'],
               "skipped":t['skipped'],
               "failed":t['failures']
            }


class MyTaskQueueManager(TaskQueueManager):
    def load_callbacks(self):   # 截断callback，只保留 api 自定义
        pass

class MyPlaybookExecutor(PlaybookExecutor):
    def __init__(self, playbooks, inventory, variable_manager, loader, options, passwords, callback):
        super(MyPlaybookExecutor, self).__init__(playbooks, inventory, variable_manager, loader, options, passwords)
        if options.listhosts or options.listtasks or options.listtags or options.syntax:
            self._tqm = None
        else:
            # MyTaskQueueManager 执行自定义的任务队列，过滤掉系统自己的callback
            self._tqm = MyTaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=self.passwords,
                    stdout_callback=callback
                )
        check_for_controlpersist(C.ANSIBLE_SSH_EXECUTABLE)


class ANSRunner(object):

    def __init__(self, *args, **kwargs):
        self.callback = ResultCallback()
        self.resource = '/data/github/SA/tools/hosts'
        self.redisobj = redis.Redis(host='127.0.0.1', port=6379, password='', db=10)
        self.__initializeData()

    def _write_to_save(self, rediskey, data):  # 写入 redis
        msg = json.dumps(data, ensure_ascii=False)
        try:
            self.redisobj.rpush(rediskey, msg)
            #print("\33[32m写入Redis：%s\33[0m" % msg)
        except Exception as e:
            print("\33[31m写入Redis：%s\33[0m" % e)

    def __initializeData(self):
        Options = namedtuple('Options', [
            'remote_user',
            'connection',
            'module_path',
            'forks',
            'become',
            'become_method',
            'become_user',
            'check',
            'diff',
            'listhosts',
            'listtasks',
            'listtags',
            'syntax',
        ])
        self.options = Options(
            remote_user='root',
            connection='paramiko',
            module_path=['/to/mymodules'],
            forks=10,
            become=None,
            become_method=None,
            become_user=None,
            check=False,
            diff=False,
            listhosts=None,
            listtasks=None,
            listtags=None,
            syntax=None
        )
        self.loader = DataLoader()

    def run_playbook(self, rediskey, playbooks, extra_vars={}):

        passwords = dict(vault_pass='secret')
        inventory = InventoryManager(loader=self.loader, sources=self.resource)
        variable_manager = VariableManager(loader=self.loader, inventory=inventory)
        variable_manager.extra_vars = extra_vars
        pb = MyPlaybookExecutor(
                                playbooks=playbooks,
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=self.loader,
                                options=self.options,
                                passwords=passwords,
                                callback=self.callback
        )
        pb.run()

        # 写入redis
        self._write_to_save(rediskey, self.get_result())

    def runner(self, rediskey, hosts, tasks, extra_vars={}):
        passwords = dict(vault_pass='secret')
        inventory = InventoryManager(loader=self.loader, sources=self.resource)
        variable_manager = VariableManager(loader=self.loader, inventory=inventory)
        variable_manager.extra_vars = extra_vars
        play_source = dict(name="Ansible Play", hosts=hosts, gather_facts='no', tasks=tasks)
        play = Play().load(play_source, variable_manager=variable_manager, loader=self.loader)
        tqm = None
        try:
            tqm = MyTaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=passwords,
                stdout_callback=self.callback
            )
            tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

        # 写入redis
        self._write_to_save(rediskey, self.get_result())

    def get_result(self):
        self.results_raw = {'ok':{},'skipped':{}, 'failed':{},'unreachable':{},"status":{}}
        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result

        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result
        return self.results_raw

if __name__ == '__main__':
    extra_vars = {'content': '这个参数从外部传入'}
    playbookkey = "run_playbook_%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    runnerkey = "runner_%s" % datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    playbooks = ['/data/github/SA/tools/playbooks/redis_opt.yml', ]
    sources = '/data/github/SA/tools/hosts'
    tasks = []
    # tasks.append(dict(action=dict(module='debug', args=dict(msg='{{ content }}'))))
    tasks.append(dict(action=dict(module='shell', args='du -sh *'), register='shell_out'))
    #tasks.append(dict(action=dict(module='ping', )))


    #实例化对象
    obj = ANSRunner()

    # obj.run_playbook(playbookkey, playbooks)
    # ret = obj.get_playbook_result()
    # print(ret)

    obj.runner(runnerkey, 'all', tasks,extra_vars={})
    ret = obj.get_result()
    print(ret)
# 运维中后台

[![license](https://img.shields.io/badge/license-mit-brightgreen.svg?style=flat)](https://github.com/renmcc/SA2/blob/master/LICENSE)
[![Release Version](https://img.shields.io/badge/release-master-brightgreen)](https://github.com/renmcc/SA2/releases)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/renmcc/SA2/pulls)

> 根据工作经历制作的一款游戏运维自动化运维后台，项目项目尚未完成，有志同道合的小伙伴可以加入进来，共同进步。

## 项目架构
##### 项目采用前后端分离技术
* 前端vue框架基于花裤衩大佬写的vue-element-admin为模板
* 后端基于django-rest-framework框架
* 任务执行基于ansibleApi和shell脚本
* 任务调度基于celery框架异步执行
* 消息推送基于websocket技术栈

## 快速体验
```sh
git clone https://github.com/renmcc/Dockerfile.git
cd Dockerfile
docker-compose up -d
用户名：admin
密码：admin
```

## 开发进度
* 已完成
- [x] 基于RBAC的用户权限管理
- [x] 基于项目的资产主机分配
- [x] 基于ansible资产信息扫描更新
- [x] 基于项目的异步任务调度


## 项目截图
![1.png](https://github.com/renmcc/SA2/blob/master/screenshot/login.png)
![3.png](https://github.com/renmcc/SA2/blob/master/screenshot/project.png)
![4.png](https://github.com/renmcc/SA2/blob/master/screenshot/cmdb.png)
![5.png](https://github.com/renmcc/SA2/blob/master/screenshot/tasks.png)
![6.png](https://github.com/renmcc/SA2/blob/master/screenshot/taskdialog.png)
![8.png](https://github.com/renmcc/SA2/blob/master/screenshot/djangoadmin.png)

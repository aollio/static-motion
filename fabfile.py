# fabfile.py
import os, re
from datetime import datetime

# 导入Fabric API:
from fabric.api import *
from os import environ as options

# 服务器登录用户名:
env.user = 'root'
# env.password = options['password']
env.password = 'password'
# sudo用户为root:
# env.sudo_user = 'root'
# 服务器地址，可以有多个，依次部署:
env.hosts = ['106.14.190.186']

_TAR_FILE = 'dist-blog.tar.gz'


def build():
    local('rm -f dist/%s' % _TAR_FILE)
    cmd = ['tar', '-czvf', 'dist/%s' % _TAR_FILE, 'site/*']
    local(' '.join(cmd))


_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/root/blog'


def deploy():
    build()
    newdir = 'site-%s' % datetime.now().strftime('%y-%m-%d_%H.%M.%S')
    # 删除已有的tar文件:
    run('rm -f %s' % _REMOTE_TMP_TAR)
    # 上传新的tar文件:
    put(os.path.join(os.path.abspath('..'), 'dist', _TAR_FILE), _REMOTE_TMP_TAR)
    # 创建新目录:
    with cd(_REMOTE_BASE_DIR):
        run('mkdir %s' % newdir)
    # 解压到新目录:
    with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
        run('tar -xzvf %s' % _REMOTE_TMP_TAR)
    # 重置软链接:
    with cd(_REMOTE_BASE_DIR):
        run('rm -f site')
        run('ln -s %s site' % newdir)
        # 重启Python服务和nginx服务器:
        # with settings(warn_only=True):
        # sudo('supervisorctl stop awesome')
        # sudo('supervisorctl start awesome')
        # sudo('nginx -s reload')

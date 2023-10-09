#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
import datetime
from fabric.api import *

env.hosts = ["54.90.32.25", "100.25.222.248"]


def do_clean(number=0):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    if number == 0 or number == 1:
        number = 1
    if type(number) is str:
        number = int(number)
    num = number + 1
    num = str(num)
    with lcd ('versions/'):
        local('ls -t | tail -n +{} | xargs rm -f'.format(num))
    with cd('/data/web_static/releases/'):
        sudo('ls -t | tail -n +{} | xargs rm -rf'.format(num))

def do_deploy(archive_path):
    ''' that distributes an archive to your web servers '''
    if not os.path.exists(archive_path):
        return False
    try:
        args = archive_path.split("/")
        filename = args[-1]
        put(archive_path, "/tmp/{}".format(filename))
        token = filename.split('.')
        file = "/data/web_static/releases/{}".format(token[0])
        sudo('mkdir -p {}'.format(file))
        sudo("tar -xzf /tmp/{} -C {}".format(filename, file))
        sudo('rm /tmp/{}'.format(filename))
        sudo('mv {}/web_static/* {}'.format(file, file))
        sudo('rm -rf {}/web_static/'.format(file))
        link = "/data/web_static/current"
        sudo('rm -rf {}'.format(link))
        sudo('ln -s {} {}'.format(file, link))
        return True
    except Exception:
        return False


def do_pack():
    ''' generates a .tgz archive from the contents
        of the web_static folder of your AirBnB Clone repo
    '''
    now_time = datetime.datetime.now()
    filename = now_time.strftime("%Y%m%d%H%M%S")

    local('mkdir -p versions')
    res = local('tar -cvzf versions/web_static_{}.tgz web_static'
                .format(filename))
    if res.succeeded:
        return "versions/web_static_{}.tgz".format(filename)
    else:
        return None


def deploy():
    ''' creates and distributes an archive to your web servers '''
    res = do_pack()
    if res:
        return do_deploy(res)
    else:
        return False

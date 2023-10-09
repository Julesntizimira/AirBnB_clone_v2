#!/usr/bin/python3
''' define do_deploy() '''
from fabric.api import *
import datetime
import os


env.hosts = ["54.90.32.25", "100.25.222.248"]


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

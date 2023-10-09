#!/usr/bin/python3
''' define do_deploy() '''
from fabric.api import *
import os


env.hosts = ["ubuntu@54.90.32.25", "ubuntu@100.25.222.248"]


def do_deploy(archive_path):
    ''' that distributes an archive to your web servers '''
    if not os.path.exists(archive_path):
        return False
    args = archive_path.split("/")
    filename = args[-1]
    res = put(archive_path, "/tmp/{}".format(filename))
    if not res.succeeded:
        return False
    res = sudo("tar -xzvf /tmp/{} -C /data/web_static/releases/"
               .format(filename))
    if not res.succeeded:
        return False
    res = sudo('rm /tmp/*.tgz')
    if not res.succeeded:
        return False
    file = "/data/web_static/releases/web_static/"
    link = "/data/web_static/current"
    res = sudo('ln -sfn {} {}'.format(file, link))
    if not res.succeeded:
        return False
    return True

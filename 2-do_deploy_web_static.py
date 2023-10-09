#!/usr/bin/python3
''' define do_deploy() '''
from fabric.api import *
import os


env.hosts = ["54.90.32.25", "100.25.222.248"]


def do_deploy(archive_path):
    ''' that distributes an archive to your web servers '''
    if not os.path.exists(archive_path):
        return False
    args = archive_path.split("/")
    filename = args[-1]
    res = put(archive_path, "/tmp/{}".format(filename))
    if not res.succeeded:
        return False
    token = filename.split('.')
    file = "/data/web_static/releases/{}".format(token[0])
    res = sudo('mkdir -p {}'.format(file))
    if not res.succeeded:
        return False
    res = sudo("tar -xzf /tmp/{} -C {}".format(filename, file))
    if not res.succeeded:
        return False
    res = sudo('rm /tmp/{}'.format(filename))
    if not res.succeeded:
        return False
    res = sudo('mv {}/web_static/* {}'.format(file, file))
    link = "/data/web_static/current"
    res = sudo('ln -sfn {} {}'.format(file, link))
    if not res.succeeded:
        return False
    return True

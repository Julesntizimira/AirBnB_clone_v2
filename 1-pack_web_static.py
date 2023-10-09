#!/usr/bin/python3
''' define def do_pack() function '''
from fabric.api import *
import datetime

def do_pack():
    ''' generates a .tgz archive from the contents
        of the web_static folder of your AirBnB Clone repo
    '''
    now_time = datetime.datetime.now()
    filename = now_time.strftime("%Y%m%d%H%M%S")

    local('mkdir -p versions')
    res = local('tar -cvzf versions/web_static_{}.tgz web_static'.format(filename))
    if res.succeeded:
        return "versions/web_static_{}.tgz".format(filename)
    else:
        return None

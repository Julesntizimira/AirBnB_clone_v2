#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
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

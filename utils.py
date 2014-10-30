"""
@file utils.py
@author Josh M. <cyrex562@gmail.com>
@brief utility functions
"""
DEBUG = 'debug'
INFO = 'info'
WARNING = 'warning'
ERROR = 'error'


def log_msg(level, msg):
    """
    login
    :param level:
    :param msg:
    :return:
    """
    print '{0}, {1}'.format(level, msg)

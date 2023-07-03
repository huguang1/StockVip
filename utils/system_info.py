"""
@author: 技术-小明
@time: 2019-04-08 11:38:43
@file: get_ip.py
@desc:
"""

import socket
import platform
import distro

from django.utils import timezone


def get_system_info(request):
    """
    查询本机ip地址
    :return: ip
    """
    try:
        fd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fd.connect(('8.8.8.8', 80))
        ip = fd.getsockname()[0]
    finally:
        fd.close()

    server = platform.platform()
    port = 80
    system_version = ' '.join(distro.linux_distribution(full_distribution_name=False))
    date_time = timezone.now()
    host = request.META['HTTP_HOST']
    data = {'ip': ip, 'server': server, 'port': port, 'version': system_version, 'date_time': date_time, 'host': host}

    return data


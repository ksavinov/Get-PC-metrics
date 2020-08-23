# /usr/bin/python3
# -*- coding: utf-8 -*-
""" Downloading files from server, using SFTP """
import os
import paramiko
import configparser
from datetime import datetime

# configs
# using RawConfigParser to prevent errors if special symbols in config.ini
config = configparser.RawConfigParser()
config.read('config.ini')
host = config.get('server', 'host')
port = int(config.get('server', 'port'))
user = config.get('server', 'user')
password = config.get('server', 'password')

files = ['metrics.csv', 'system_data.txt']
remote_path = config.get('server', 'path')
local_path = os.getcwd()


def download_reports():
    try:
        # connect via ssh, sftp
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(
                    paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, port=port, username=user, password=password)
        sftp = ssh.open_sftp()

        now = datetime.now()
        print(now.strftime("%H:%M:%S"))

        # download files
        for file in files:
            file_remote = remote_path + file    # e.g. /root/
            file_local = local_path + "/" + file

            print(file_remote + ' >>> ' + file_local)

            sftp.get(file_remote, file_local)
        print("\n")
    except Exception as e:
        print("Exception! %s" % e)
        ssh.close()
        sftp.close()

    # close connection
    ssh.close()
    sftp.close()


if __name__ == "__main__":
    download_reports()

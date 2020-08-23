#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Execution commands on server by ssh """
import paramiko
import configparser

# using RawConfigParser to prevent errors if special symbols in config.ini
config = configparser.RawConfigParser()

# configs
config.read('config.ini')
host = config.get('server', 'host')
port = config.get('server', 'port')
user = config.get('server', 'user')
password = config.get('server', 'password')
command1 = config.get('commands', 'command1')
command2 = config.get('commands', 'command2')

try:
    # establish connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    client.connect(host, port, user, password, timeout=10)
    print("Connect to {}:{} successful!".format(host, port))

    # execute command
    print("Executing command on the server: {}".format(command1))
    stdin, stdout, stderr = client.exec_command(command1)
    errors = stderr.read()
    output = stdout.read()
    if output:
        print("Out: {}".format(output))
    else:
        print("ERROR: {}".format(errors))

    # execute command
    print("Executing command on the server: {}".format(command2))
    stdin, stdout, stderr = client.exec_command(command2)
    errors = stderr.read()
    output = stdout.read()
    if output:
        print("Out: {}".format(output))
    else:
        print("ERROR: {}".format(errors))
except Exception as e:
    print("Exception! %s" % e)
    client.close()

# close connection
client.close()

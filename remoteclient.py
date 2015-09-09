#!/usr/bin/python

import paramiko
import glob

paramiko.util.log_to_file('/tmp/paramiko.log')


class RemoteClient():
    """ Paramiko remote client to connect, run, copy"""

    def __init__(self):
        self.hosts = []
        self.connections = []

    def add_host(self, args):
        """add_host
        Add list for hosts to the hosts list """
        if args:
            self.hosts.append(args.split(','))
        else:
            print "usage: add_host('127.0.0.1,user,password') "

    def connect(self, timeout=10):
        """Connect to all hosts in the hosts list"""
        # maintains duplicate copy of original host
        host_pool = self.hosts[:]
        for host in self.hosts:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            try:
                if len(host[2]) == 0:
                    client.connect(host[0], username=host[1], timeout=timeout)
                else:
                    client.connect(host[0],
                                   username=host[1],
                                   password=host[2],
                                   timeout=timeout)
                self.connections.append(client)
            except Exception as e:
                print 'Unable to connect to ', host[0]
                # Removes invalid hosts
                host_pool.remove(host)
        self.hosts = host_pool

    def run(self, command):
        """run
        Execute this command on all hosts in the list"""
        if command:
            for host, conn in zip(self.hosts, self.connections):
                stdin, stdout, stderr = conn.exec_command(command)
                stdin.close()
                for line in stdout.read().splitlines():
                    print 'host: %s: %s' % (host[0], line)
        else:
            print "usage: run('uptime') "

    def copy(self, file_path, to_path):
        """copy
        Copies file to all hosts in the list"""
        if glob.glob(file_path):
            for host, conn in zip(self.hosts, self.connections):
                print "Copying to [{0}] ==> [{1}] ".format(host[0], to_path)
                ftp = conn.open_sftp()
                ftp.put(file_path, to_path)
                ftp.close()
        else:
            print "usage: copy('hello.txt', '/tmp/hello.txt')"

    def close(self):
        for conn in self.connections:
            conn.close()
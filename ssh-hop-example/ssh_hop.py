#!/usr/bin/python

import paramiko as ssh
import time
import re

class ssh_hop(object):
    def __init__(self, host, user, auth,
                 via=None, via_user=None, via_auth=None):
        if via:
            #print "Logging into %s (user %s) via %s (user %s)" % (host, user, via, via_user)
            t0 = ssh.Transport(via)
            t0.start_client()
            t0.auth_password(via_user, via_auth)
            # setup forwarding from 127.0.0.1:<free_random_port> to |host|
            channel = t0.open_channel('direct-tcpip', host, ('127.0.0.1', 0))
            self.transport = ssh.Transport(channel)
        else:
            #print "Logging into %s (user %s)" % (host, user)
            self.transport = ssh.Transport(host)
        client = self.transport.start_client()
        self.transport.auth_password(user, auth)
        self.sftp=None

    def run(self, cmd):
        ch = self.transport.open_session()
        ch.set_combine_stderr(True)
        ch.exec_command(cmd)
        retcode = ch.recv_exit_status()
        buf,prev = '',' '
        while ch.recv_ready() or len(prev) != 0:
            prev = ch.recv(1024)
            buf += prev
        return (buf, retcode)

    def Send(self, cmd):
        ch = self.transport.open_session()
        ch.set_combine_stderr(True)
        ch.invoke_shell()

        ch.sendall(cmd+'\n')

        ch.sendall("echo $?;exit\n")
        rc = ch.exit_status_ready()
        while not rc:
            time.sleep(1)
            rc = ch.exit_status_ready()

        buf =''
        while ch.recv_ready():
            rsp = ch.recv(1024)
            buf += rsp

        ch.close()
        
        rc=0
        out=buf
        #print out
        m  = re.search( r'^(.*)(\d+)\n$', buf)
        if m:
            out = m.group(1)
            rc = m.group(2)

        return (out,rc)


    def get_sftp(self):
        self.sftp = ssh.SFTPClient.from_transport(self.transport)
        return self.sftp
    def Close(self):
        if self.sftp:
            self.sftp.close()
            self.sftp = None
        if self.transport:
            self.transport.close()
            self.transport=None
    def __del__(self):
        self.Close()



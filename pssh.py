#!/usr/bin/python
#coding:utf8
import os
import sys
import pexpect
import termios
import struct, fcntl, os, sys, signal
from sys import argv


def sigwinch_passthrough (sig, data):
    winsize = getwinsize()
    global p
    p.setwinsize(winsize[0],winsize[1])

def getwinsize():
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

passwdfile = "%s/.psshwd" % os.path.expanduser("~")
if os.path.isfile(passwdfile) == False:
    os.system("touch %s" % passwdfile)

def password(account,host,p):
    ah = "%s@%s" % (account,host)
    passwd = None
    if os.path.isfile(passwdfile):
        with open(passwdfile,"r") as f:
            lines = f.readlines()
            for l in lines:
                splits = l.split()
                sah,pwd = splits[0],splits[1]
                if sah == ah:
                    passwd = pwd
                    break

    if passwd == None:
        while True:
            print "new host found,please input passwod for %s:" % ah
            passwd = sys.stdin.readline().rstrip()
            print "receive password:%s" % passwd
            if passwd:
                with open(passwdfile,"a") as f:
                    f.write("%s %s\n" % (ah,passwd))
                break
            else:
                continue
    p.sendline(passwd)

    ws = getwinsize()
    p.setwinsize(ws[0],ws[1])
    p.interact()

                 
    

if __name__ == "__main__":
    account = argv[1]
    host = argv[2]

    p = pexpect.spawn("/usr/bin/ssh %s@%s" % (account,host))
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)
    i = p.expect(["The authenticity of host.*",".*password:",pexpect.TIMEOUT])
    if i == 0:
        p.sendline("yes")
        p.expect(".*password:")
        password(account,host,p)
    elif i == 1:
        password(account,host,p)
    else:
        print "timeout"
        p.close()


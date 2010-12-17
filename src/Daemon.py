'''
Created on 25/10/2010

@author: Pedro Andrade
'''
from signal import SIGTERM
from threading import Thread
import io
import os
import sys
import time
class Daemon(Thread):
    '''
    Start daemon
    '''
    
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        
    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                    # exit first parent
                    sys.exit(0)
        except OSError:
                sys.exit(1)
        
        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)
        
        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError:
            print("erro ao carregar o fork 2.. exit daemon")
            sys.exit(1)
        
        # redirect standard file descriptors
        sys.stdout.flush()
        sys.stderr.flush()
        
        # write pidfile
        pid = str(os.getpid())
        file = io.open(self.pidfile, mode="w")
        file.write("%s\n" % pid)
        file.close()
        if not file:
            print("error na hora de excrever o daemon")
        print("escreveu o daemon: ", os.getpid())
            
    def start(self):
        """
        Start the daemon
        """
        # Check for a pidfile to see if the daemon already runs
        pid = None
        try:
                pf = io.open(self.pidfile, mode="r")
                pid = int(pf.read().strip())
                pf.close()
        except IOError as ioError:
                pid = None
                print("Daemon is not running... running now.")
        except Exception as ex:
            print("unknow error: ", ex)
            
        if pid:
                message = "pidfile %s already exist. Daemon already running?\n" % (self.pidfile)
                sys.stderr.write(message)
                sys.exit(1)
       
        # Start the daemon
        self.daemonize()
        self.run()
            
    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidfile
        try:
                pf = io.open(self.pidfile, "r")
                pid = int(pf.read().strip())
                pf.close()
        except IOError:
                pid = None
        except Exception:
                pid = None
        if not pid:
                message = "pidfile %s does not exist. Daemon not running?\n" % (self.pidfile)
                sys.stderr.write(message)
                return
        print("passou do pid")
        # Try killing the daemon process       
        try:
            while True:
                    os.remove(self.pidfile)
                    print("arquivo removido... matando processo...")
                    os.kill(pid, SIGTERM)
                    time.sleep(1)
        except OSError as boom:
                print("removendo arquivo pidFile: ", boom)
                os.remove(self.pidfile)
        
    def run(self):
        print("running")

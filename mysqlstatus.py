#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import threading
import MySQLdb as Database
import time
import curses
from datetime import datetime


__title__ = 'mysqlstatus'
__version__ = '0.1.0-DEV'
__author__ = 'Shoma Suzuki'
__license__ = 'MIT'
__copyright__ = 'Copyright 2012 Shoma Suzuki'


import logging
if not os.path.isdir("logs"):
    os.mkdir("logs")
logging.basicConfig(
    format='%(asctime)s - %(message)s in %(funcName)s() at %(filename)s : %(lineno)s',
    level=logging.DEBUG,
    filename="logs/debug.log",
    filemode='w',
)


def get_args_parser():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-h", "--host",
        default="localhost",
        nargs='?',
        type=str,
        help="Connect to host.")
    parser.add_argument("-p", "--port",
        default=3306,
        nargs='?',
        type=int,
        help="Port number to use for connection.")
    parser.add_argument("-u", "--user",
        default=None,
        nargs='?',
        type=str,
        help="User for login if not current user.")
    parser.add_argument("-P", "--password",
        default='',
        nargs='?',
        type=str,
        help="Password to use when connecting to server.")
    parser.add_argument("-i", "--interval",
        default=1,
        nargs='?',
        type=int,
        help="Interval second of monitoring.")
    parser.add_argument("-o", "--outfile",
        default=sys.stdout,
        nargs='?',
        type=argparse.FileType('w'),
        help="Output result file. avairable for non-interactive.")
    parser.add_argument("-n", "--nonint",
        default=False,
        action='store_true',
        help="Non-interactive.")
    parser.add_argument("--help",
        default=False,
        action='store_true',
        help="show this help message and exit.")
    return parser


class QueryThread(threading.Thread):
    def __init__(self, **kwargs):
        self.stop = False
        self.update = False

        self.mysql_variables = None
        self.mysql_status = None
        self.mysql_last_status = None

        self.db = kwargs.get('db')
        self.cursor = self.db.cursor()
        self.interval = kwargs.get('interval', 1)

        self.lock = threading.Lock()

        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        while self.stop == False:
            self.get_status()
            time.sleep(self.interval)
        self.cleanup_mysql()

    def cleanup_mysql(self):
        self.cursor.close()

    def query(self, sql):
        result = {}
        try:
            self.lock.acquire()
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.lock.release()
        except Exception, e:
            logging.error(e)
        return dict(result)

    def get_variables(self):
        """SHOW VARIABLES"""
        if self.mysql_variables is not None:
            return self.mysql_variables
        result = self.query("SHOW VARIABLES")
        self.mysql_variables = result
        return self.mysql_variables

    def get_status(self):
        """ SHOW GLOBAL STATUS """
        if self.mysql_status is not None:
            self.mysql_last_status = self.mysql_status
        self.mysql_status = self.query("SHOW GLOBAL STATUS")
        logging.debug(self.mysql_status)
        self.get_query_per_second()
        self.update = True
        return self.mysql_status

    def get_query_per_second(self):
        if self.mysql_status is None:
            return 0.0
        if self.mysql_last_status is not None:
            [current, last] = map(lambda x: float(x),
                (self.mysql_status.get('Uptime'),
                 self.mysql_last_status.get('Uptime')))
            elapsed_time = last - current

            [current, last] = map(lambda x: float(x),
                (self.mysql_status.get('Questions', 0),
                self.mysql_last_status.get('Questions', 0)))
            inc_query = last - current
        else:
            [elapsed_time, inc_query] = map(lambda x: float(x),
                (self.mysql_status.get('Uptime', 0),
                self.mysql_status.get('Questions', 0)))
        try:
            qps = inc_query / elapsed_time
        except:
            qps = 0.0
        self.mysql_status.update({'QPS': "%0.2f" % qps})
        return qps


class MySQLStatus:
    keywords = (
        "QPS",
        "Aborted_connects",
        "Binlog_cache_disk_use",
        "Bytes_received",
        "Bytes_sent",
        "Connections",
        "Created_tmp_disk_tables",
        "Created_tmp_files",
        "Created_tmp_tables",
        "Handler_delete",
        "Handler_read_first",
        "Handler_read_rnd",
        "Handler_read_rnd_next",
        "Handler_update",
        "Handler_write",
        "Key_read_requests",
        "Key_reads",
        "Max_used_connections",
        "Open_files",
        "Opened_table_definitions",
        "Opened_tables",
        "Opened_tables",
        "Qcache_free_memory",
        "Qcache_hits",
        "Qcache_queries_in_cache",
        "Questions",
        "Select_full_join",
        "Select_full_range_join",
        "Select_range",
        "Select_range_check",
        "Select_scan",
        "Slave_running",
        "Slow_queries",
        "Sort_merge_passes",
        "Sort_scan",
        "Table_locks_immediate",
        "Table_locks_waited",
        "Threads_connected",
        "Threads_created",
        "Threads_running",
        "Uptime",
    )

    def __init__(self, options):
        self.options = options
        if self.options.user is None:
            self.options.user = os.getenv('USERNAME')

        try:
            db = Database.connect(
                host=self.options.host,
                user=self.options.user,
                port=self.options.port,
                passwd=self.options.password)
        except Exception, err:
            print err
            sys.exit()

        self.qthread = QueryThread(
            db=db,
            interval=options.interval,
        )
        self.qthread.start()


class IntractiveMode(MySQLStatus):
    def run(self):
        self.window = curses.initscr()
        self.window.nodelay(1)
        (self.window_max_x, self.window_max_y) = self.window.getmaxyx()
        curses.noecho()
        curses.cbreak()

        try:
            self.mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.cleanup()
        except Exception, err:
            self.cleanup()
            print err
        finally:
            self.cleanup()

    def mainloop(self):
        self.show_header()
        while True:
            c = self.window.getch()
            if c == ord('q'):
                break
            elif c == ord('h') or c == ord('?'):
                self.show_help()

            if self.qthread.update == True:
                self.show_update_status()
            time.sleep(0.1)

    def show_header(self):
        variables = self.qthread.get_variables()
        data = {
            'hostname': variables.get('hostname'),
            'currenttime': datetime.now().isoformat(),
            'mysql_version': variables.get('version'),
        }
        data = "%(hostname)s, %(currenttime)s, %(mysql_version)s" % data
        self.window.addstr(0, 0, data)
        self.window.addstr(1, 0, "-" * 70)

    def show_update_status(self):
        status = self.qthread.mysql_status
        self.qthread.update = False
        x = 2
        for k in self.keywords:
            data = "%-25s: %12s" % (k, status.get(k))
            if x +1 < self.window_max_x:
                self.window.addstr(x, 0, data)

            x = x + 1
        if len(self.keywords)+1 > self.window_max_x:
            omits = len(self.keywords)+1 - self.window_max_x
            self.window.addstr(self.window_max_x -1, 0, "[%d items were truncated.]" % omits)

    def cleanup(self):
        self.window.erase()
        curses.nocbreak()
        self.window.keypad(0)
        curses.echo()
        curses.endwin()
        self.qthread.stop = True

        while self.qthread.isAlive():
            # wait for stop QueryThread
            pass

    def show_help(self):
        help_text = """
        h or ? show this help message
        q      quit

        [Press any key to continue]
        """
        self.window.erase()
        self.window.addstr(1, 0, help_text)
        self.window.nodelay(0)
        self.window.getch()

        self.window.erase()
        self.window.nodelay(1)
        self.show_header()

class CliMode(MySQLStatus):
    def run(self):
        self.output = self.options.outfile
        try:
            self.mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.cleanup()
        except Exception, err:
            self.cleanup()
            print err
        finally:
            self.cleanup()

    def mainloop(self):
        while True:
            if self.qthread.update == True:
                self.show_update_status()
                time.sleep(0.1)

    def show_update_status(self):
        status = self.qthread.mysql_status
        self.qthread.update = False
        self.output.write(str(status))

    def cleanup(self):
        self.qthread.stop = True
        while self.qthread.isAlive():
            pass

if __name__ == '__main__':
    parser = get_args_parser()
    options = parser.parse_args()
    if options.help:
        parser.print_help()
        parser.exit()

    if(options.nonint):
        monitor = CliMode(options)
    else:
        monitor = IntractiveMode(options)
    monitor.run()

# vim: fenc=utf8 et sw=4 ts=4

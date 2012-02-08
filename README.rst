MySQL Monitor
=============

MySQL Monitor is a command set to monitoring MySQL server status.

REQUIREMENTS
------------

 - python2.7
 - MySQLdb

mysqlstaus.py
-------------

show status by *SHOW GLOBAL STATUS;* statement.

see `MySQL :: MySQL 5.1 Reference Manual :: 12.7.5.37 SHOW STATUS Syntax <http://dev.mysql.com/doc/refman/5.1/en/show-status.html>`_

::

    usage: mysqlstatus.py [-h [HOST]] [-p [PORT]] [-u [USER]] [-P [PASSWORD]]
                          [-i [INTERVAL]] [-o [OUTFILE]] [-n] [--help]
    
    optional arguments:
      -h [HOST], --host [HOST]
                        Connect to host.
      -p [PORT], --port [PORT]
                            Port number to use for connection.
      -u [USER], --user [USER]
                            User for login if not current user.
      -P [PASSWORD], --password [PASSWORD]
                            Password to use when connecting to server.
      -i [INTERVAL], --interval [INTERVAL]
                            Interval second of monitoring.
      -o [OUTFILE], --outfile [OUTFILE]
                            Output result file. avairable for non-interactive.
      -n, --nonint          Non-interactive.
      -m [{status,process}], --mode [{status,process}]
                                monitoring Mode
      --debug               Debug log enable.
      --help                show this help message and exit.

LICENSE
-------
MIT LICENSE

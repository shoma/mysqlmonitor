MySQL Monitor
=============

MySQL Monitor is a console-based (non-gui) tool for monitoring MySQL server.

MySQL Monitor is inspired by [innotop](https://code.google.com/p/innotop/) and [mytop](http://jeremy.zawodny.com/mysql/mytop/).

STATUS
------
*Work in process*

REQUIREMENTS
------------

- python2.7
- MySQLdb

mysqlstaus.py
-------------
show status by `SHOW GLOBAL STATUS;` statement.
see [MySQL :: MySQL 5.7 Reference Manual :: 13.7.5.34 SHOW STATUS Syntax](http://dev.mysql.com/doc/refman/5.7/en/show-status.html)

```
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

```

LICENSE
-------
MIT LICENSE

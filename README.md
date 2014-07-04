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

Example of output
-----------------

```
localhost, 2014-07-04 23:07:41, 5.6.17
----------------------------------------------------------------------
QPS                      :         1.00
Aborted_connects         :            0
Binlog_cache_disk_use    :            0
Bytes_received           :          962
Bytes_sent               :       251485
Connections              :            3
Created_tmp_disk_tables  :            0
Created_tmp_files        :            5
Created_tmp_tables       :           27
Handler_delete           :            0
Handler_read_first       :            3
Handler_read_rnd         :            0
Handler_read_rnd_next    :         9141
Handler_update           :            0
Handler_write            :         9098
Key_read_requests        :            0
Key_reads                :            0
Max_used_connections     :            1
Open_files               :           16
Opened_table_definitions :           32
Opened_tables            :           32
Opened_tables            :           32
Qcache_free_memory       :      1031336
Qcache_hits              :            0
Qcache_queries_in_cache  :            0
Questions                :           30
Select_full_join         :            0
Select_full_range_join   :            0
Select_range             :            0
Select_range_check       :            0
Select_scan              :           27
Slave_running            :          OFF
Slow_queries             :            0
Sort_merge_passes        :            0
Sort_scan                :            0
Table_locks_immediate    :           35
Table_locks_waited       :            0
Threads_connected        :            1
Threads_created          :            1
Threads_running          :            1
Uptime                   :         1907
```
LICENSE
-------
MIT LICENSE

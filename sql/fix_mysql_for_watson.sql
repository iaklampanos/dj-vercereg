-- http://www.dangtrinh.com/2013/08/django-error-caused-by-mariadbmysqls.html
-- http://dba.stackexchange.com/questions/6150/what-is-the-safest-way-to-switch-the-binlog-format-at-runtime
FLUSH TABLES WITH READ LOCK;
FLUSH LOGS;
SET GLOBAL binlog_format = 'MIXED';
FLUSH LOGS;
UNLOCK TABLES;


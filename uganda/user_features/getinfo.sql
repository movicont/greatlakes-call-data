CREATE TABLE CDR 
( sender int,
receiver varchar(255),
calldate varchar(255),
calltime varchar(255),
duration int,
cost int,
tower varchar(255),
region varchar(255));

.separator ","

.import "C:\Users\yian\code\research\uganda\applab_6.csv" CDR
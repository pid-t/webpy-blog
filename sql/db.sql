create database blog;

create table article
(
	id int not null auto_increment,
	comment int not null default 0,
	title varchar(255) not null,
	date datetime,
	content text not null,
	usrid int not null default 1,
	author varchar(255) default '',
	tag varchar(32) default '',
	primary key(id)
)engine=innodb,charset=utf8;

create table comment
(
	id int not null auto_increment,
	content varchar(255) not null,
	author varchar(255) not null,
	email  varchar(512) not null,
	homepage varchar(512) not null default '',
	usrid int not null default 0,
	articleid int not null,
	date datetime not null,
	primary key(id)
)engine=innodb,charset=utf8;

create table user
(
	id int not null auto_increment,
	password char(32) not null,
	user varchar(255) not null unique,
	primary key(id)
)engine=innodb,charset=utf8;

create table msg
(
    id int not null auto_increment,
	content varchar(255) not null,
	author varchar(255) not null,
	email  varchar(512) not null,
	homepage varchar(512) not null default '',
	usrid int not null default 0,
	date datetime not null,
	primary key(id)
)engine=innodb,charset=utf8;

use Hainan;
create table users (
	id int auto_increment primary key,
	login varchar(20) not null,
    password varchar(50) not null,
    first_name varchar(20) not null,
	phone_number varchar(11) not null,
    role enum('admin', 'teacher') not null
);
use Hainan;
create table clients (
	id int auto_increment primary key,
	first_name varchar(20) not null,
	phone_number varchar(11) not null,
    role enum('classes', 'trips') not null
);

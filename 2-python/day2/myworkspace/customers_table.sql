create table customers(
    id integer primary key auto_increment, -- this is the primary key
    name varchar(50) not null,
    email varchar(50) unique,
    phone varchar(50) unique,
    city varchar(50) default 'Bangalore'
)
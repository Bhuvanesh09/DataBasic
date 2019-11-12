create database CALENDAR;
use CALENDAR; 
create table student (
    user_id varchar(10) unique not null,
    user_name varchar(30) not null,
    DOB DATE not null,
    gender varchar(6) not null,
    hostel varchar(30) not null,
    year_of_admission YEAR not null,
    program_name varchar(5) not null,
    PRIMARY KEY(user_id)
);

create table administrator (
    user_id varchar(10) unique not null,
    user_name varchar(30) not null,
    DOB DATE not null,
    gender varchar(6) not null,
    designation varchar(20),
    PRIMARY KEY(user_id)
);

create table user_group (
    group_id varchar(10) unique not null,
    name varchar(20) unique not null,
    type varchar(20),
    PRIMARY KEY(group_id)
);

create table course(
    course_id varchar(10) unique not null,
    course_name varchar(50) unique not null,
    department_id varchar(10) not null,
    PRIMARY KEY(course_id),
    FOREIGN KEY(department_id) references user_group(group_id) 
);

create table building(
    building_name varchar(30) unique not null,
    no_of_rooms int,
    PRIMARY KEY (building_name)
);


create table location(
    building_name varchar(30) not null,
    room_number int not null,
    room_name varchar(30),
    PRIMARY KEY(building_name, room_number),
    FOREIGN KEY(building_name) references building(building_name)
);

create table event(
    event_name varchar(50) not null,
    building_name varchar(30) not null,
    room_number int not null,
    group_id varchar(10) not null,
    start_time time not null,
    end_time time not null,
    event_date DATE not null,
    PRIMARY KEY(building_name, room_number, start_time, event_date),
    FOREIGN KEY(building_name, room_number) references location(building_name, room_number),
    FOREIGN KEY(group_id) references user_group(group_id)
);

create table club_co(
    group_id varchar(10) not null,
    user_id varchar(10) not null,
    PRIMARY KEY(user_id, group_id),
    FOREIGN KEY(user_id) references student(user_id),
    FOREIGN KEY(group_id) references user_group(group_id)
);

create table group_members(
    user_id varchar(10) not null,
    group_id varchar(10) not null,
    PRIMARY KEY (user_id, group_id),
    FOREIGN KEY (user_id) references student(user_id),
    FOREIGN KEY (group_id) references user_group(group_id) 
);


insert into student values(21130, 'Ankit Roy', '1998-10-13', 'Male', 'Bakul', 2019, 'CND');
insert into student values(21140, 'Ankita Ray', '1998-10-21', 'Female', 'Parijaat', 2018, 'ECE');

insert into administrator values(51120,'Mahant Parekh', '1992-01-22', 'Male', 'Senior Administrator');

insert into user_group values ('C101', 'Music', 'Club');
insert into user_group values ('O121', 'NLPStudents', NULL);
insert into user_group values ('D110', 'Mathematics', 'Department');

insert into building values ('Nilgiri', 10);
insert into building values ('Himalaya', 15);

insert into course values ('M12430','Math-I','D110');

insert into location values('Nilgiri', 105, 'BODH');
insert into location values('Himalaya', 203, NULL);

insert into group_members values (21130, 'O121');
insert into group_members values (21130, 'C101');
insert into group_members values (21140, 'C101');

insert into club_co values ('C101', 21140);

insert into event values('Guitar Workshop', 'Nilgiri', '105', 'C101', '13:00:00', '16:00:00', '2019-12-21');
insert into event values('Tabla Workshop', 'Nilgiri', '105', 'C101', '13:00:00', '16:00:00', '2019-12-30');
insert into event values('Language Inference', 'Himalaya', '203', 'O121', '13:00:00', '16:00:00', '2019-12-30');


-- Report Generation queries

-- 1> Events on a given date:

-- select * from event where date = 'YYYY-MM-DD'

-- 2> check if location is free during time slot
-- select * from event 
-- where building_name='location-building' and room_number='location-room' and event_date = 'time slot date' and 
-- ( 
--  (start_time between 'time slot end' and 'time slot end' or end_time between 'time slot begin' and 'time slot end')
--  OR
--  (start_time < 'time slot start' and end_time > 'time slot end' )
-- );


-- if this returns empty set, then time slot is free, otherwise not free.

-- 3> check if a particular user group (provided group name) is invited to a particular event (provided event name)
-- select name,event_name from user_group 
-- join event on user_group.group_id = event.group_id 
-- where event_name = 'given event name' and user_group.name = 'given group name';


-- if this returns empty, not invited, if it returns non null, then yes, group is invited.


-- 4>show all of a user's events arranged according to time
-- select event_name, event_date, event_ from event 
-- join group_members on group_members.group_id = event.group_id 
-- where group_members.user_id = given user id
-- order by event_date;
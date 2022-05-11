-- Создание таблиц 

create table post(
	IDpost int unique not null,
	descr varchar(50) not null
);


create table price(
	IDserv int unique  not null,
	IDqual int not null,
	descr varchar (50),
	price decimal not null
);

create table shedule_tab(
	id_sch serial primary key,
	work_day int,
	weekend_day int
);


create table servicelist(
	IDdoc int not null,
	IDserv int not null,
	foreign key (IDserv) references price (IDserv),
	foreign key (IDdoc) references stafflist_new (IDdoc)
);


create table cab_list(
	id_cab serial primary key,
	num_cab int not null
); 

create table quallist(
	IDqual int unique not null,
	descr  varchar (50)
);


create table plotlist(
	IDplt int unique not null,
	descr varchar (50)
);

create table schedule_doc(
	id_time serial primary key,
	date_pr date,
	time_pr time,
	id_cab int,
	id_doc int,
	id_sch int,
	busy int,
	id_pat int,
	
	foreign key(id_doc) references stafflist_new (iddoc) on  delete cascade,
	foreign key (id_cab) references cab_list (id_cab) on  delete cascade,
	foreign key (id_sch) references shedule_tab (id_sch) on  delete cascade
	);



create table stafflist_new(
	IDpost int not null,
	IDqual int not null,
	IDdoc int unique not null,
	lastname varchar (50) not null,
	firstname varchar (50) not null,
	patronymic varchar (50),
	begoffers date not null,
	workexp double precision,
	IDplt int,
	foreign key (IDpost) references post(IDpost),
	foreign key (IDqual) REFERENCES quallist (IDqual),
	FOREIGN KEY (IDplt) REFERENCES plotlist(IDplt)
);


-- создание триггера для подсчёта стажа 

create or replace function fun_calc_exp_new() 
returns trigger as
$body$
begin
	update stafflist_new
	set workexp = date_part('day', (now() - begoffers));
	return new;
end;
$body$
LANGUAGE plpgsql volatile

create trigger trig_calc_exp_new
after insert 
on stafflist_new
for each statement 
execute procedure fun_calc_exp_new();

-- заполнение данных в таблицы

insert into post (idpost, descr)
values (1, 'Эндокринолог'),
(2, 'Дерматолог'),
(3, 'Гинеколог'),
(4, 'Уролог'),
(5, 'Медсестра/медбрат'),
(6, 'ЛОР'),
(7, 'Офтальмолог'),
(8, 'Терапевт'),
(9, 'Венеролог'),
(10, 'Стоматолог'),
(11, 'Ортопед'),
(12, 'Хирург'),
(13, 'Кардиоло'),
(14, 'Аллерголог')

insert into quallist (idqual, descr)
values (1, 'практикант'),
(2, 'специалист'),
(3, 'вторая'),
(4, 'первая'),
(5, 'высшая')

insert into price (idserv, idqual, descr, price)
values (1, 2, 'Первичный приём спец.', 1500),
(2, 3, 'Первичный приём врач 2 квал', 2000),
(3, 4, 'Первичный приём врач 1 квал', 2500),
(4, 5, 'Первичный приём высш. квал.', 3000),
(5, 1, 'Расшифровка анализов', 500),
(6, 2, 'Расшифровка анализов', 500),
(7, 3, 'Расшифровка анализов', 500),
(8, 4, 'Расшифровка анализов', 500),
(9, 5, 'Расшифровка анализов', 500),
(10, 1, 'Сбор крови', 0)

insert into plotlist (idplt, descr)
values (1, 'Гагаринский р-н'),
(2, 'Академический р-н'),
(3, 'р-н Якиманка'),
(4, 'р-н Алтуфьево'),
(5, 'р-н Бибирево'),
(6, 'р-н Отрадное'),
(7, 'р-н Беляево'),
(8, 'Мытищи'),
(9, 'Химки'),
(10, 'Басманный р-н')

insert into servicelist (iddoc, idserv)
values (1, 1),
(2, 5),
(3, 2),
(4, 9), 
(5, 10),
(6, 1)


insert into stafflist_new (idpost, idqual, iddoc, lastname, firstname, patronymic, begoffers, idplt)
values (1, 2, 1, 'Иванов', 'Иван', 'Иванович', '01-01-2020', 1),
(2, 1, 2, 'Иванова', 'Мария', 'Петрова', '02-01-2022', 2),
(3, 3, 3, 'Кузнецова', 'Галина', 'Леонидовна', '01-07-2003', 3),
(4, 5, 4, 'Рыбкина', 'Наталья', 'Владимировна', '08-21-2011', 4),
(5, 1, 5, 'Сухилин', 'Александр', 'Владиславович', '02-12-2015', 6),
(6, 2, 6, 'Будейко', 'Валентин', 'Ярославович', '02-02-2021', 5)


insert into schedule_doc (date_pr, time_pr, id_cab, id_doc, id_sch, id_pat, busy)
values 
--('2022-05-10', '12:00', 3, 6, 78, 1),
('2022-05-10', '12:15', 3, 6, 78, 1),
('2022-05-10', '12:30', 3, 6, 78, 1),
('2022-05-10', '12:45', 3, 6, 78, 1),
('2022-05-10', '13:00', 3, 6, 78, 1)

-- Создадим свободные временные слоты

insert into schedule_doc (date_pr, time_pr, id_cab, id_doc, id_sch, busy)
values 
('2022-05-11', '12:00', 3, 6, 0),
('2022-05-11', '12:15', 3, 6, 0),
('2022-05-11', '12:30', 3, 6, 0),
('2022-05-11', '12:45', 3, 6, 0),
('2022-05-11', '13:00', 3, 6, 0)


--Функция для получения свободных слотов врача 
create or replace function get_free_slots(name_spec text)
returns table (
	code_visit int,
	date_visit date,
	time_visit char,
	lastname_doc varchar(50),
	firstname_doc varchar (50),
	patronymic_doc varchar (50)
)
as
$body$ 
	select id_time as Код_записи, date_pr as Дата, to_char(time_pr, 'HH24:MI') as Время_записи, sn.lastname as Фамилия, sn.firstname as Имя, sn.patronymic as Отчество from schedule_doc as sd 
	join stafflist_new as sn on sd.id_doc = sn.iddoc 
	join post as p on sn.idpost = p.idpost 
	where p.descr = name_spec and busy = 0 
	order by date_pr 
$body$ 
language 'sql' volatile 

-- Проверка
select * from get_free_slots ('ЛОР')

-- Запись пациента на свободный слот

select * from schedule_doc sd 

create or replace function add_new_patient_visit(id_time_visit int, id_pat_visit int)
returns void 
as
$body$ 
	update schedule_doc 
	set busy = 1,
	id_pat = id_pat_visit 
	where id_time = id_time_visit 
$body$ 
language 'sql' volatile 

-- id пациента получаем в док. бд 
select add_new_patient_visit (11, 78)
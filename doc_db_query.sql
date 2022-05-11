
select * from patient_test pt 
where data_pat ->> 'years' >= '25'

create table patient_test(
	id serial primary key,
	data_pat jsonb
)


select * from patient_test


-- Скрипт для создания нового пациента
insert into patient_test (data_pat) values
(
	'{"name": "Минаева Алёна Сергеевна"
	}'
)

-- Обновление данных пациента
update patient_test 
set data_pat = jsonb_set(data_pat, '{years}', '21') 
where data_pat ->> 'name' = 'Минаева Алёна Сергеевна'


-- Добавление адреса пациента
update patient_test 
set data_pat = jsonb_set(data_pat, '{address}', '"г. Москва м. Альтуфьево"') 
where data_pat ->> 'name' = 'Минаева Алёна Сергеевна'

-- Через функцию

create or replace function add_new_patient_info(name_pat text , path_col text[], new_info jsonb)
returns void as
$body$ 
	update patient_test 
	set data_pat = jsonb_set(data_pat, path_col, new_info) 
	where data_pat ->> 'name' = name_pat 
$body$ 
language 'sql' volatile 

select add_new_patient_info ('Иванов Иван Иванович', '{address}', '"Тюмень"')


-- Получение id пациента через его номер телефона и ФИО

select id from patient_test pt 
where data_pat ->> 'phone_number' = '799965453' and data_pat ->> 'name' = 'Минаева Алёна Сергеевна'

-- Создание функции для получения id пациента через его номер телефона и ФИО
-- Запись идёт в реляционной бд

 create or replace function get_id_patient(name_pat text, phonе_pat text)
 returns table
 (
 	id_pat int
 )
 as
$body$
	select id from patient_test pt 
	where data_pat ->> 'phone_number' = phonе_pat and data_pat ->> 'name' = name_pat 
$body$ 
language 'sql' volatile


select * from get_id_patient ('Минаева Алёна Сергеевна', '799965453')

-- Функция, которая получает данные о пациенте через его номер телефона и ФИО

create or replace function get_info_pat(name_pat text, phonе_pat text)
returns table
(
	name varchar(50),
	address varchar(50),
	years text,
	phonе varchar(50)
)
as
$body$
		select data_pat ->'name', data_pat->'address', data_pat->'years', data_pat -> 'phone_number' from patient_test pt 
		where data_pat ->> 'phone_number' = phonе_pat and data_pat ->> 'name' = name_pat 
$body$
language 'sql' volatile 

select * from patient_test pt 

select * from get_info_pat('Воронин Константин Николаевич', '79254445599')

select id from patient_test pt 
where data_pat ->> 'phone_number' = '79254445599' and data_pat ->> 'name' = 'Воронин Константин Николаевич'

delete from patient_test 
where data_pat ->> 'name' = 'Трунин Данила Алексеевич'

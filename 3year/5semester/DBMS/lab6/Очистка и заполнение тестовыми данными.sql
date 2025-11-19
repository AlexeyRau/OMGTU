-- Очистка и перезаполнение данных
TRUNCATE TABLE Interviews, Responses, Vacancies, Resumes, Employers, Staff, Categories, VacancyStatuses, ResponseStatuses RESTART IDENTITY CASCADE;

INSERT INTO VacancyStatuses (status_id, status_name) VALUES 
(1, 'активна'),
(2, 'закрыта'), 
(3, 'на паузе');

INSERT INTO ResponseStatuses (status_id, status_name) VALUES
(1, 'отправлено'),
(2, 'принято'),
(3, 'отклонено');

INSERT INTO Categories (cat_id, cat_name, cat_parent_id) VALUES
(1, 'IT', NULL),
(2, 'Продажи', NULL),
(3, 'Маркетинг', NULL),
(4, 'Финансы', NULL),
(5, 'Программирование', 1),
(6, 'Системное администрирование', 1),
(7, 'Веб-разработка', 5),
(8, 'Мобильная разработка', 5);

INSERT INTO Employers (emp_id, emp_company_name, emp_contact_person, emp_contacts, emp_address) VALUES
(1, 'ООО "ТехноПрофи"', 'Петров Иван Сергеевич', '+7-900-123-45-67, hr@technoprofi.ru', 'Москва, ул. Ленина, 15'),
(2, 'АО "БизнесСофт"', 'Сидорова Мария Владимировна', '+7-901-234-56-78, career@bizsoft.ru', 'Санкт-Петербург, Невский пр., 25'),
(3, 'ИП "ВебСтудия"', 'Козлов Алексей Дмитриевич', '+7-902-345-67-89, info@webstudio.ru', 'Омск, ул. Маркса, 10'),
(4, 'ЗАО "ФинАналитика"', 'Волкова Елена Петровна', '+7-903-456-78-90, hr@finanalytics.ru', 'Москва, ул. Тверская, 30'),
(5, 'ООО "ТоргУспех"', 'Никитин Сергей Владимирович', '+7-904-567-89-01, info@torguspeh.ru', 'Екатеринбург, ул. Мира, 8');

INSERT INTO Staff (staff_id, staff_name, staff_position) VALUES
(1, 'Иванова Елена Викторовна', 'менеджер по трудоустройству'),
(2, 'Смирнов Дмитрий Петрович', 'старший менеджер'),
(3, 'Кузнецова Ольга Сергеевна', 'менеджер по работе с работодателями');

INSERT INTO Resumes (res_id, res_full_name, res_contacts, res_birth_date, res_education, res_experience, res_cat_id) VALUES
(1, 'Соколов Андрей Николаевич', '+7-910-111-22-33, sokolov@mail.ru', '1990-05-15', 'высшее техническое', 5, 7),
(2, 'Орлова Марина Игоревна', '+7-911-222-33-44, orlova@gmail.com', '1988-12-20', 'высшее экономическое', 7, 2),
(3, 'Федоров Павел Александрович', '+7-912-333-44-55, fedorov@yandex.ru', '1995-08-10', 'среднее специальное', 2, 6),
(4, 'Ковалева Анна Сергеевна', '+7-913-444-55-66, kovaleva@mail.ru', '1992-03-25', 'высшее техническое', 1, 7),
(5, 'Григорьев Иван Петрович', '+7-914-555-66-77, grigoriev@gmail.com', '1985-11-08', 'высшее техническое', 10, 6),
(6, 'Морозова Дарья Олеговна', '+7-915-666-77-88, morozova@yandex.ru', '1998-07-14', 'неоконченное высшее', 0, 3);

INSERT INTO Vacancies (vac_position, vac_description, vac_requirements, vac_salary, vac_emp_id, vac_cat_id, vac_status_id) VALUES
('Frontend-разработчик', 'Разработка пользовательских интерфейсов', 'Опыт работы с React, JavaScript', 120000, 1, 7, 1),
('Менеджер по продажам', 'Работа с корпоративными клиентами', 'Опыт продаж от 3 лет', 80000, 2, 2, 1),
('Системный администратор', 'Обслуживание IT-инфраструктуры', 'Знание Linux, Windows Server', 90000, 3, 6, 1),
('Senior Backend-разработчик', 'Разработка серверной части приложений', 'Опыт работы с Python/Django от 5 лет', 180000, 4, 5, 1),
('Маркетолог', 'Продвижение продуктов компании', 'Опыт в digital-маркетинге', 70000, 5, 3, 2),
('Менеджер по работе с клиентами', 'Обслуживание существующих клиентов', 'Коммуникабельность, стрессоустойчивость', 75000, 5, 2, 3),
('Junior QA Engineer', 'Тестирование веб-приложений', 'Базовые знания тестирования', 60000, 1, 5, 1);

INSERT INTO Responses (resp_id, resp_vacancy_id, resp_resume_id, resp_date, resp_status_id, resp_staff_id) VALUES
(1, 1, 1, CURRENT_DATE - INTERVAL '5 days', 1, 1),
(2, 2, 2, CURRENT_DATE - INTERVAL '4 days', 1, 2),
(3, 3, 3, CURRENT_DATE - INTERVAL '3 days', 2, 1),
(4, 4, 4, CURRENT_DATE - INTERVAL '2 days', 3, 2),
(5, 4, 5, CURRENT_DATE - INTERVAL '1 day', 1, 1);

-- ИСПРАВЛЕННАЯ ЧАСТЬ: даты собеседований в БУДУЩЕМ
INSERT INTO Interviews (int_id, int_response_id, int_date_time, int_location, int_result) VALUES
(1, 3, CURRENT_DATE + INTERVAL '5 days', 'Омск, ул. Маркса, 10, офис 305', 'запланировано');
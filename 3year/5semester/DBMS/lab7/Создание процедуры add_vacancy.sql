CREATE OR REPLACE PROCEDURE add_vacancy(
    vac_position_text text,
    description text,
    requirements text,
    salary numeric,
    employer_id integer,
    category_id integer,
    status_id integer
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO vacancies (
        vac_position, vac_description, vac_requirements, 
        vac_salary, vac_emp_id, vac_cat_id, vac_status_id
    ) VALUES (
        vac_position_text, description, requirements, 
        salary, employer_id, category_id, status_id
    );
END;
$$;

TRUNCATE TABLE vacancies RESTART IDENTITY CASCADE;

INSERT INTO Vacancies (vac_position, vac_description, vac_requirements, vac_salary, vac_emp_id, vac_cat_id, vac_status_id)
VALUES
('Frontend-разработчик', 'Разработка пользовательских интерфейсов', 'Опыт работы с React, JavaScript', 120000, 1, 7, 1),
('Менеджер по продажам', 'Работа с корпоративными клиентами', 'Опыт продаж от 3 лет', 80000, 2, 2, 1),
('Системный администратор', 'Обслуживание IT-инфраструктуры', 'Знание Linux, Windows Server', 90000, 3, 6, 1);

SELECT * FROM vacancies ORDER BY vac_id;

-- Запрос 1: Удаляем триггеры событий (если есть)
DROP EVENT TRIGGER IF EXISTS log_function_trigger;
DROP EVENT TRIGGER IF EXISTS protect_functions_trigger;

-- Запрос 2: Удаляем триггеры данных
DROP TRIGGER IF EXISTS vacancies_audit_trigger ON Vacancies;
DROP TRIGGER IF EXISTS validate_salary_trigger ON Vacancies;
DROP TRIGGER IF EXISTS update_response_date_trigger ON Responses;

-- Запрос 3: Удаляем функции
DROP FUNCTION IF EXISTS audit_vacancies_changes();
DROP FUNCTION IF EXISTS validate_vacancy_salary();
DROP FUNCTION IF EXISTS update_modified_date();
DROP FUNCTION IF EXISTS log_function_operations();
DROP FUNCTION IF EXISTS protect_important_functions();

-- Запрос 4: Удаляем таблицу аудита
DROP TABLE IF EXISTS vacancies_audit;

CREATE TABLE vacancies_audit (
    audit_id SERIAL PRIMARY KEY,
    operation CHAR(1) NOT NULL,
    audit_timestamp TIMESTAMP NOT NULL,
    user_name TEXT NOT NULL,
    vac_id INTEGER,
    old_position TEXT,
    new_position TEXT,
    old_salary INTEGER,
    new_salary INTEGER
);

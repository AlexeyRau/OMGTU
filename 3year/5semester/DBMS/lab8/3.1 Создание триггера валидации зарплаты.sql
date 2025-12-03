CREATE OR REPLACE FUNCTION validate_vacancy_salary()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.vac_salary <= 0 THEN
        RAISE EXCEPTION 'Зарплата должна быть положительным числом. Получено: %', NEW.vac_salary;
    END IF;
    
    IF NEW.vac_salary > 1000000 THEN
        RAISE EXCEPTION 'Зарплата % слишком высокая. Максимально допустимая: 1,000,000', NEW.vac_salary;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER validate_salary_trigger
BEFORE INSERT OR UPDATE ON Vacancies
FOR EACH ROW EXECUTE FUNCTION validate_vacancy_salary();
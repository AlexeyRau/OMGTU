CREATE OR REPLACE FUNCTION audit_vacancies_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO vacancies_audit (operation, audit_timestamp, user_name, vac_id, new_position, new_salary)
        VALUES ('I', NOW(), current_user, NEW.vac_id, NEW.vac_position, NEW.vac_salary);
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO vacancies_audit (operation, audit_timestamp, user_name, vac_id, old_position, new_position, old_salary, new_salary)
        VALUES ('U', NOW(), current_user, NEW.vac_id, OLD.vac_position, NEW.vac_position, OLD.vac_salary, NEW.vac_salary);
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO vacancies_audit (operation, audit_timestamp, user_name, vac_id, old_position, old_salary)
        VALUES ('D', NOW(), current_user, OLD.vac_id, OLD.vac_position, OLD.vac_salary);
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER vacancies_audit_trigger
AFTER INSERT OR UPDATE OR DELETE ON Vacancies
FOR EACH ROW EXECUTE FUNCTION audit_vacancies_changes();
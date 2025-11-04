CREATE TABLE work_schedules (
    schedule_id integer NOT NULL,
    schedule_staff_id integer NOT NULL,
    work_days integer[],
    CONSTRAINT work_schedules_PK PRIMARY KEY (schedule_id)
);

ALTER TABLE work_schedules
ADD CONSTRAINT work_schedules_FK FOREIGN KEY (schedule_staff_id)
REFERENCES staff (staff_id)
ON DELETE CASCADE
ON UPDATE CASCADE;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
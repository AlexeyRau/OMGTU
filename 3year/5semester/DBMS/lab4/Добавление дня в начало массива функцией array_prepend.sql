UPDATE work_schedules
SET work_days = array_prepend(1, work_days)
WHERE schedule_id = 3;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
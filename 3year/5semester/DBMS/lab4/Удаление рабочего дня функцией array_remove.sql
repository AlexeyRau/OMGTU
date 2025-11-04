UPDATE work_schedules
SET work_days = array_remove(work_days, 6)
WHERE schedule_id = 2;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
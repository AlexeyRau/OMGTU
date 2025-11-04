UPDATE work_schedules
SET work_days = array_append(work_days, 4)
WHERE schedule_id = 3;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
UPDATE work_schedules
SET work_days[2] = 3, work_days[3] = 4
WHERE schedule_id = 1;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
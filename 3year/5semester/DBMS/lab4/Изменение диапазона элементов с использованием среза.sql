UPDATE work_schedules
SET work_days[1:2] = ARRAY[2, 3]
WHERE schedule_id = 2;

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
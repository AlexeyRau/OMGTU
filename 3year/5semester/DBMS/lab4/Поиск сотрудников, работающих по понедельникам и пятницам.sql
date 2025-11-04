SELECT st.staff_name, s.work_days
FROM work_schedules s
JOIN staff st ON s.schedule_staff_id = st.staff_id
WHERE s.work_days @> ARRAY[1, 5];
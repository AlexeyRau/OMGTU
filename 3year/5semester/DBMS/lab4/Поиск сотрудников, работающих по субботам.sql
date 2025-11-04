SELECT st.staff_name, s.work_days
FROM work_schedules s
JOIN staff st ON s.schedule_staff_id = st.staff_id
WHERE array_position(s.work_days, 6) IS NOT NULL;
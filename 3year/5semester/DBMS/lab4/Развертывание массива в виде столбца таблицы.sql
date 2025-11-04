SELECT st.staff_name, unnest(s.work_days) AS рабочий_день
FROM work_schedules s
JOIN staff st ON s.schedule_staff_id = st.staff_id
WHERE s.schedule_id = 2
ORDER BY рабочий_день;
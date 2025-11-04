INSERT INTO work_schedules VALUES
(1, 1, '{1, 3, 5, 6}'::integer[]),
(2, 2, '{1, 2, 4, 5, 6}'::integer[]),
(3, 3, '{2, 3, 5, 7}'::integer[]);

SELECT s.schedule_id, st.staff_name, s.work_days
FROM work_schedules s 
JOIN staff st ON s.schedule_staff_id = st.staff_id;
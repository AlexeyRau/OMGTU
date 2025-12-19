SELECT * 
FROM meter_readings
WHERE current_value > 50 
  AND consumption < 5
  AND meter_id = 2;
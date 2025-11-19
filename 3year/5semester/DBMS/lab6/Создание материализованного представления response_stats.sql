CREATE MATERIALIZED VIEW response_stats AS
SELECT 
    r.resp_status_id,
    rs.status_name,
    COUNT(*) AS total_responses
FROM responses r
JOIN responsestatuses rs ON r.resp_status_id = rs.status_id
GROUP BY r.resp_status_id, rs.status_name;

SELECT * FROM response_stats;
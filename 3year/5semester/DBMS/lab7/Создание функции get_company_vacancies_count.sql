CREATE OR REPLACE FUNCTION get_candidate_stats_by_category(p_category_id INTEGER)
RETURNS TABLE(
    total_candidates BIGINT,
    avg_experience NUMERIC,
    min_experience INTEGER,
    max_experience INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*) AS total_candidates,
        AVG(r.res_experience) AS avg_experience,
        MIN(r.res_experience) AS min_experience,
        MAX(r.res_experience) AS max_experience
    FROM Resumes r
    WHERE r.res_cat_id = p_category_id;
END;
$$;

SELECT * FROM Resumes WHERE res_cat_id = 7;  -- Соискатели в веб-разработке
SELECT * FROM get_candidate_stats_by_category(7);
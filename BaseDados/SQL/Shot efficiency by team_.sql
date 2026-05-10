WITH TeamShots AS (
    SELECT
        [team1] AS Team,
        [number_of_goals_team1] AS Goals,
        [total_attempts_team1] AS TotalAttempts,
        [on_target_attempts_team1] AS OnTargetAttempts
    FROM [Fifa_world_cup_matches (2)]
 
    UNION ALL
 
    SELECT
        [team2] AS Team,
        [number_of_goals_team2] AS Goals,
        [total_attempts_team2] AS TotalAttempts,
        [on_target_attempts_team2]  AS OnTargetAttempts
    FROM [Fifa_world_cup_matches (2)]
)
SELECT
    Team,
    SUM(Goals) AS Goals,
    SUM(TotalAttempts) AS TotalAttempts,
    SUM(OnTargetAttempts) AS OnTargetAttempts,
    CAST(100.0 * SUM(OnTargetAttempts) / NULLIF(SUM(TotalAttempts), 0) AS DECIMAL(10,2)) AS ShotAccuracyPct,
    CAST(100.0 * SUM(Goals) / NULLIF(SUM(TotalAttempts), 0) AS DECIMAL(10,2)) AS GoalConversionPct
FROM TeamShots
GROUP BY Team
ORDER BY GoalConversionPct DESC;

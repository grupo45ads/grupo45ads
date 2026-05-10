WITH TeamPossession AS (
    SELECT
        [team1] AS Team,
        TRY_CAST(REPLACE([possession_team1], '%', '') AS DECIMAL(10,2)) AS PossessionPct,
        [number_of_goals_team1] AS Goals
    FROM [Fifa_world_cup_matches (2)]
 
    UNION ALL
 
    SELECT
        [team2] AS Team,
        TRY_CAST(REPLACE([possession_team2], '%', '') AS DECIMAL(10,2)) AS PossessionPct,
        [number_of_goals_team2] AS Goals
    FROM [Fifa_world_cup_matches (2)]
)
SELECT
    Team,
    CAST(AVG(PossessionPct) AS DECIMAL(10,2)) AS AvgPossessionPct,
    SUM(Goals) AS TotalGoals,
    COUNT(*) AS MatchesPlayed
FROM TeamPossession
GROUP BY Team
ORDER BY AvgPossessionPct DESC;

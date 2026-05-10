WITH TeamStats AS (
    SELECT 
        team1 AS Team,
        [number_of_goals_team1] AS Goals
    FROM [dbo].[Fifa_world_cup_matches (2)]

    UNION ALL

    SELECT 
        [team2] AS Team,
        [number_of_goals_team2] AS Goals
    FROM [dbo].[Fifa_world_cup_matches (2)]
)
SELECT 
    Team,
    SUM(Goals) AS TotalGoals
FROM TeamStats
GROUP BY Team
ORDER BY TotalGoals DESC;
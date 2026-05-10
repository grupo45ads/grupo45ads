WITH TeamResults AS (
    SELECT
        [team1] AS Team,
        CASE
            WHEN [number_of_goals_team1] > [number_of_goals_team2] THEN 'Win'
            WHEN [number_of_goals_team1] = [number_of_goals_team2] THEN 'Draw'
            ELSE 'Loss'
        END AS Result
    FROM [dbo].[Fifa_world_cup_matches (2)]

    UNION ALL

    SELECT
        [team2] AS Team,
        CASE
            WHEN [number_of_goals_team2] > [number_of_goals_team1] THEN 'Win'
            WHEN [number_of_goals_team2] = [number_of_goals_team1] THEN 'Draw'
            ELSE 'Loss'
        END AS Result
    FROM [dbo].[Fifa_world_cup_matches (2)]
)
SELECT
    Team,
    SUM(CASE WHEN Result = 'Win' THEN 1 ELSE 0 END) AS Wins,
    SUM(CASE WHEN Result = 'Draw' THEN 1 ELSE 0 END) AS Draws,
    SUM(CASE WHEN Result = 'Loss' THEN 1 ELSE 0 END) AS Losses,
    COUNT(*) AS MatchesPlayed
FROM TeamResults
GROUP BY Team
ORDER BY Wins DESC, Draws DESC, Losses ASC;
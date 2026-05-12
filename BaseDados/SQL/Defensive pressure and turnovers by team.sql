WITH TeamDefense AS ( 
    SELECT 
        [team1] AS Team, 
        [forced_turnovers_team1] AS ForcedTurnovers, 
        [defensive_pressures_applied_team1] AS DefensivePressures, 
        [goal_preventions_team1] AS GoalPreventions, 
        [conceded_team1] AS GoalsConceded 
    FROM [dbo].[Fifa_world_cup_matches (2)] 
  
    UNION ALL 
  
    SELECT 
        [team1] AS Team, 
        [forced_turnovers_team2] AS ForcedTurnovers, 
        [defensive_pressures_applied_team2] AS DefensivePressures, 
        [goal_preventions_team2] AS GoalPreventions, 
        [conceded_team2] AS GoalsConceded 
    FROM [dbo].[Fifa_world_cup_matches (2)] 
) 
SELECT 
    Team, 
    SUM(ForcedTurnovers) AS ForcedTurnovers, 
    SUM(DefensivePressures) AS DefensivePressures, 
    SUM(GoalPreventions) AS GoalPreventions, 
    SUM(GoalsConceded) AS GoalsConceded, 
    CAST(1.0 * SUM(DefensivePressures) / NULLIF (COUNT(*), 0) AS 
DECIMAL (10,2)) AS AvgDefensivePressuresPerMatch 
FROM TeamDefense 
GROUP BY Team 
ORDER BY DefensivePressures DESC; 
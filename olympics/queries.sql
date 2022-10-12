SELECT abbreviation from nocs
ORDER BY abbreviation;


SELECT given_name, surname
FROM athletes
INNER JOIN game_event_athlete_results
ON athletes.id = game_event_athlete_results.athlete_id
INNER JOIN nocs
ON game_event_athlete_results.noc_id = nocs.id
WHERE nocs.name = 'Jamaica'
ORDER BY athletes.surname;


SELECT athletes.given_name, athletes.surname, olympic_games.year,
    olympic_games.season, events.name, game_event_athlete_results.medal
FROM game_event_athlete_results
INNER JOIN athletes
ON athletes.id = game_event_athlete_results.athlete_id
INNER JOIN olympic_games
ON olympic_games.id = game_event_athlete_results.game_id
INNER JOIN events
ON events.id = game_event_athlete_results.event_id
WHERE athletes.surname LIKE '%Louganis%'
AND game_event_athlete_results.medal IS NOT NULL;



SELECT nocs.name, COUNT(game_event_athlete_results.medal)
FROM nocs
INNER JOIN game_event_athlete_results
ON nocs.id = game_event_athlete_results.noc_id
WHERE game_event_athlete_results.medal = 'Gold'
GROUP BY nocs.name
ORDER BY COUNT(game_event_athlete_results.medal)
DESC;
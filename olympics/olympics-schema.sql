CREATE TABLE athletes (
    id integer,
    given_name text,
    surname text
);

CREATE TABLE olympic_games (
    id integer,
    year integer,
    season text,
    city text
);

CREATE TABLE nocs (
    id integer,
    abbreviation text,
    name text
);

CREATE TABLE events (
    id integer,
    name text
);

CREATE TABLE game_event_athlete_results (
    game_id integer,
    event_id integer,
    athlete_id integer,
    medal text,
    athlete_height integer,
    athlete_weight integer
);
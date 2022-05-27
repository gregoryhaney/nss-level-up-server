SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_event;

DELETE FROM levelupapi_game WHERE id=2

INSERT INTO levelupapi_game VALUES(2, "Pac Man", "ColecoVision", 2, 4, 3, 1);
INSERT INTO levelupapi_game VALUES(3, "Asteroids", "Konami", 1, 1, 2, 1);

SELECT 
    g.title AS GameTitle,
    g.maker AS GameMaker,
    u.first_name || " " || 
    u.last_name AS Name,
    u.id AS ID
FROM levelupapi_game AS g
JOIN levelupapi_gamer AS r
    ON g.gamer_id = r.id
JOIN auth_user AS u
    ON r.id = u.id


SELECT
    g.title,
    e.organizer_id,
    e.game_id,
    r.id AS GamerId,
    r.user_id,
    u.first_name || " " || 
    u.last_name AS Name,
    u.id AS ID
FROM levelupapi_game AS g
JOIN levelupapi_event as e
    ON g.id = e.game_id
JOIN levelupapi_gamer AS r
    ON e.organizer_id = r.id
JOIN auth_user AS u
    ON r.id = u.id

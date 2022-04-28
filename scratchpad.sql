SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;
SELECT * FROM levelupapi_event;

DELETE FROM levelupapi_game WHERE id=2

INSERT INTO levelupapi_game VALUES(2, "Pac Man", "ColecoVision", 2, 4, 3, 1);
INSERT INTO levelupapi_game VALUES(3, "Asteroids", "Konami", 1, 1, 2, 1);


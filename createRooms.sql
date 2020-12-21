CREATE TABLE dictionary (
    id   INTEGER      PRIMARY KEY AUTOINCREMENT
                      NOT NULL
                      UNIQUE,
    word VARCHAR (20) UNIQUE
                      NOT NULL
);

CREATE TABLE rooms (
    room_code        INTEGER       PRIMARY KEY AUTOINCREMENT
                                   UNIQUE
                                   NOT NULL,
    word_ids         VARCHAR (255) NOT NULL,
    red_ids          VARCHAR (50)  NOT NULL,
    blue_ids         VARCHAR (50)  NOT NULL,
    assassin_ids     VARCHAR (10)  NOT NULL,
    red_guessed      VARCHAR (50),
    blue_guessed     VARCHAR (50),
    assassin_guessed VARCHAR (5),
    neutral_guessed  VARCHAR (20),
    team_guessing    VARCHAR (5)   DEFAULT ('red'),
    guess_count      INTEGER
);


SELECT * FROM rooms;

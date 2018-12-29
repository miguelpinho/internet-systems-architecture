DROP TABLE IF EXISTS moves_user;
DROP TABLE IF EXISTS message_building;
DROP TABLE IF EXISTS message_user;
DROP TABLE IF EXISTS bot;
DROP TABLE IF EXISTS ist_user;
DROP TABLE IF EXISTS building;

CREATE TABLE building (
    id INTEGER,
    name VARCHAR(100) UNIQUE NOT NULL,
    latitude NUMERIC(6, 3) NOT NULL,
    longitude NUMERIC(6, 3) NOT NULL,
    radius NUMERIC(6, 3) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ist_user (
    ist_ID VARCHAR(20),
    latitude NUMERIC(6, 3),
    longitude NUMERIC(6, 3),
    cur_building INTEGER,
    PRIMARY KEY (ist_ID),
    FOREIGN KEY (cur_building) REFERENCES building(id)
);

CREATE TABLE bot (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY,
    token VARCHAR(20) UNIQUE NOT NULL,
    building INTEGER
    /* FOREIGN KEY (building) REFERENCES building(id) */
);

CREATE TABLE message_user (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY AUTOINCREMENT, /* always a bigger id */
    ist_ID VARCHAR(20),
    message TEXT
    /* not a good idea impose that user must exist: */
    /* FOREIGN KEY (ist_ID) REFERENCES ist_user(ist_ID) */
);

CREATE TABLE message_building (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY AUTOINCREMENT, /* always a bigger id */
    building INTEGER,
    message TEXT,
    FOREIGN KEY (building) REFERENCES building(id)
);

CREATE TABLE moves_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building INTEGER NOT NULL,
    state VARCHAR(5) NOT NULL
);
/* TODO: make state enum */


/* auto update user building */
CREATE TRIGGER set_building AFTER INSERT
ON ist_user
FOR EACH ROW
BEGIN
    UPDATE ist_user SET cur_building =
    (
        SELECT MIN(B.id) FROM building AS B
        WHERE ABS(B.latitude - NEW.latitude) <= B.radius
        AND ABS(B.longitude - NEW.longitude) <= B.radius
    )
    WHERE ist_ID = NEW.ist_ID;
END;


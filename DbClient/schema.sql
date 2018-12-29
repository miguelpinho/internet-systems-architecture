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
    /* radius NUMERIC(6, 3), */
    cur_building INTEGER,
    PRIMARY KEY (ist_ID),
    FOREIGN KEY (cur_building) REFERENCES building(id)
);

CREATE TABLE bot (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY,
    token VARCHAR(20) UNIQUE NOT NULL,
    building INTEGER,
    /* PRIMARY KEY (id), */
    FOREIGN KEY (building) REFERENCES building(id)
);

CREATE TABLE message_user (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ist_ID VARCHAR(20),
    message TEXT,
    /* PRIMARY KEY (id), */
    FOREIGN KEY (ist_ID) REFERENCES ist_user(ist_ID)
);

CREATE TABLE message_building (
    /* id INTEGER NOT NULL AUTO_INCREMENT, */
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    building INTEGER,
    message TEXT,
    /* PRIMARY KEY (id), */
    FOREIGN KEY (building) REFERENCES building(id)
);


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


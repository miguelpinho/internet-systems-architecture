DROP TABLE IF EXISTS ist_user;
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS robot;

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
    radius NUMERIC(6, 3),
    cur_building INTEGER,
    PRIMARY KEY (ist_ID),
    FOREIGN KEY (cur_building) REFERENCES building(id)
);

CREATE TABLE bot (
    id INTEGER NOT NULL AUTO_INCREMENT,
    token VARCHAR(20) UNIQUE NOT NULL,
    building INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (building) REFERENCES building(id)
);

CREATE TABLE message_user (
    id INTEGER NOT NULL AUTO_INCREMENT,
    ist_ID VARCHAR(20),
    message TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (ist_ID) REFERENCES ist_user(ist_ID)
);

CREATE TABLE message_building (
    id INTEGER NOT NULL AUTO_INCREMENT,
    building INTEGER,
    message TEXT,
    PRIMARY KEY (id),
    FOREIGN KEY (building) REFERENCES building(id)
);

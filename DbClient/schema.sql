DROP TABLE IF EXISTS ist_user;
DROP TABLE IF EXISTS building;
DROP TABLE IF EXISTS robot;

CREATE TABLE building (
    id INTEGER,
    name VARCHAR(100) UNIQUE NOT NULL,
    latitude NUMERIC(6, 3) NOT NULL,
    latitude NUMERIC(6, 3) NOT NULL,
    radius NUMERIC(6, 3) NOT NULL,
    PRIMARY KEY (id)
);

create TABLE ist_user (
    ist_ID VARCHAR(20),
    token VARCHAR(20) UNIQUE,
    latitude NUMERIC(6, 3),
    longitude NUMERIC(6, 3),
    radius NUMERIC(6, 3),
    cur_building id,
    PRIMARY KEY (ist_ID),
    FOREIGN KEY (cur_building) REFERENCES building(id)
);

create TABLE robot (
    id INTEGER,
    token VARCHAR(20) UNIQUE NOT NULL,
    building INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY (building) REFERENCES building(id)
);

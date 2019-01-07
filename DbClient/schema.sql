DROP TABLE IF EXISTS moves_user;
DROP TABLE IF EXISTS message_building;
DROP TABLE IF EXISTS message_user;
DROP TABLE IF EXISTS bot;
DROP TABLE IF EXISTS ist_user;
DROP TABLE IF EXISTS building;

CREATE TABLE building (
    id INTEGER,
    name VARCHAR(100) UNIQUE NOT NULL,
    latitude NUMERIC(12, 8) NOT NULL,
    longitude NUMERIC(12, 8) NOT NULL,
    radius NUMERIC(12, 8) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ist_user (
    ist_ID VARCHAR(20),
    latitude NUMERIC(12, 8),
    longitude NUMERIC(12, 8),
    cur_building INTEGER,
    PRIMARY KEY (ist_ID)
);

CREATE TABLE bot (
    id INTEGER NOT NULL AUTO_INCREMENT,
    token VARCHAR(40) UNIQUE NOT NULL,
    building INTEGER,
    PRIMARY KEY (id)
);

CREATE TABLE message_user (
    id INTEGER NOT NULL AUTO_INCREMENT,
    ist_ID VARCHAR(20),
    message TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE message_building (
    id INTEGER NOT NULL AUTO_INCREMENT,
    building INTEGER,
    message TEXT,
    PRIMARY KEY (id)
);

CREATE TABLE moves_user (
    id INTEGER NOT NULL AUTO_INCREMENT,
    ist_ID VARCHAR(20) NOT NULL,
    building INTEGER NOT NULL,
    state ENUM('in', 'out'),
    PRIMARY KEY (id)
);


delimiter $$

CREATE TRIGGER set_building_ins
BEFORE INSERT
    ON ist_user FOR EACH ROW
BEGIN
    IF NEW.latitude IS NULL OR NEW.longitude IS NULL THEN
        SET NEW.cur_building = NULL;
    ELSE
        SET NEW.cur_building =
        (
            SELECT MIN(B.id)
            FROM building AS B
            WHERE ABS(B.latitude - NEW.latitude) <= B.radius
            AND ABS(B.longitude - NEW.longitude) <= B.radius
        );
    END IF;
END; $$

CREATE TRIGGER log_move_ins
AFTER INSERT
    ON ist_user FOR EACH ROW
BEGIN
    IF NEW.cur_building IS NOT NULL THEN
        INSERT INTO moves_user (ist_ID, building, state) VALUES (NEW.ist_ID, NEW.cur_building, 'in');
    END IF;
END; $$

CREATE TRIGGER set_building_upd
BEFORE UPDATE
    ON ist_user FOR EACH ROW
BEGIN
    IF NEW.latitude IS NULL OR NEW.longitude IS NULL THEN
        SET NEW.cur_building = NULL;
    ELSE
        SET NEW.cur_building =
        (
            SELECT MIN(B.id)
            FROM building AS B
            WHERE ABS(B.latitude - NEW.latitude) <= B.radius
            AND ABS(B.longitude - NEW.longitude) <= B.radius
        );
    END IF;
END; $$

CREATE TRIGGER log_move_upd
AFTER UPDATE
    ON ist_user FOR EACH ROW
BEGIN
    IF NEW.cur_building IS NULL AND OLD.cur_building IS NOT NULL THEN
        INSERT INTO moves_user (ist_ID, building, state) VALUES (OLD.ist_ID, OLD.cur_building, 'out');
    ELSEIF NEW.cur_building IS NOT NULL AND OLD.cur_building IS NULL THEN
        INSERT INTO moves_user (ist_ID, building, state) VALUES (NEW.ist_ID, NEW.cur_building, 'in');
    ELSEIF NEW.cur_building IS NOT NULL AND OLD.cur_building IS NOT NULL AND NEW.cur_building <> OLD.cur_building THEN
        BEGIN
            INSERT INTO moves_user (ist_ID, building, state) VALUES (NEW.ist_ID, OLD.cur_building, 'out');
            INSERT INTO moves_user (ist_ID, building, state) VALUES (NEW.ist_ID, NEW.cur_building, 'in');
        END;
    END IF;
END; $$

delimiter ;

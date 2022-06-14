CREATE TABLE farms_id (
    farm_id   STRING PRIMARY KEY ON CONFLICT ABORT,
    farm_name STRING
);

CREATE TABLE hive2 (
    rig_id         STRING   UNIQUE ON CONFLICT ABORT,
    rig_name       STRING,
    rig_online     BOOLEAN,
    time           DATETIME,
    rig_status     STRING,
    rozetka_id     STRING,
    rozetka_key    STRING,
    is_watchdog    BOOLEAN,
    rozetka_exists BOOLEAN,
    sw_name        STRING,
    has_problems   BOOLEAN
);

CREATE TABLE pref (
    name  STRING UNIQUE ON CONFLICT ABORT,
    value STRING
);


INSERT INTO pref (name, value) VALUES ('pause', 'unpause');

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

CREATE TABLE powerman (
    id       STRING  PRIMARY KEY,
    [action] INTEGER
);

CREATE TABLE notify_pool (
    rig_id    STRING,
    notify_id STRING
);


CREATE TABLE comparison (
    status_id   STRING PRIMARY KEY ON CONFLICT ABORT,
    status_text STRING
);

INSERT INTO pref (name, value) VALUES ('pause', 'unpause');

INSERT INTO comparison (status_id, status_text) VALUES ('self_heal', '🌱 Риг выздоровел самостоятельно');
INSERT INTO comparison (status_id, status_text) VALUES ('socket_healed', '☘️ Розеточка помогла! перезагрузился!');
INSERT INTO comparison (status_id, status_text) VALUES ('heal_from_emergency', '🍀 Риг восстановлен из аварийных');
INSERT INTO comparison (status_id, status_text) VALUES ('silent', '🤐 Риг молчит, подождём, может обновляется или перезагружается');
INSERT INTO comparison (status_id, status_text) VALUES ('no_socket', '🚫 Нет розетки! Сразу перевожу в аварийный статус');
INSERT INTO comparison (status_id, status_text) VALUES ('no_watchdog', '🪱 настройте watchdog на риге');
INSERT INTO comparison (status_id, status_text) VALUES ('overheat', '🥵 Перегрев');
INSERT INTO comparison (status_id, status_text) VALUES ('missed_unit', '🫥 Карта отсутствует');
INSERT INTO comparison (status_id, status_text) VALUES ('no_hashrate', '💤 Нет хешрейта на риге');
INSERT INTO comparison (status_id, status_text) VALUES ('missed_temp', '🌡 Нет данных температуры на карте');
INSERT INTO comparison (status_id, status_text) VALUES ('missed_hashrate', '😴 Нет хешрейта на карте');
INSERT INTO comparison (status_id, status_text) VALUES ('clean_string', '#️⃣ Содержит в имени знак решётки, лучше переименовать');
INSERT INTO comparison (status_id, status_text) VALUES ('too_long_silent_reboot', '♻️ Риг долго молчит — перезагружаем...');
INSERT INTO comparison (status_id, status_text) VALUES ('has_problem_reboot', '🖲 Есть проблемы — перезагружаем...');
INSERT INTO comparison (status_id, status_text) VALUES ('is_emergency', '🆘️ Авария!!! Риг не перезагрузился, отключаю питание, приезжайте разбирайтесь!');
INSERT INTO comparison (status_id, status_text) VALUES ('heal_try', '🐣 Попытаюсь восстановить из аварийных');
INSERT INTO comparison (status_id, status_text) VALUES ('rig_ignored', '🛠 Риг на обслуживании игнорирую');

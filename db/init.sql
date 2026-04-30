-- Nuclear safety SQLite schema

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS nuclear_safety
(
    id                         INTEGER PRIMARY KEY AUTOINCREMENT,
    year                       INTEGER NOT NULL,
    quarter                    INTEGER NOT NULL CHECK (quarter BETWEEN 1 AND 4),
    station                    TEXT    NOT NULL,

    irg                        REAL,
    irg_index                  REAL,
    iodine_radionuclides       REAL,
    iodine_radionuclides_index REAL,
    stable_radionuclides       REAL,
    stable_radionuclides_index REAL,

    cs_137_emission            REAL,
    co_60_emission             REAL,
    cs_137_dump                REAL,
    co_60_dump                 REAL,
    volume                     REAL,

    radioactive_release_index  REAL,
    dump_index                 REAL,

    created_at                 TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (year, quarter, station)
);

CREATE INDEX IF NOT EXISTS idx_nuclear_safety_period
    ON nuclear_safety (year, quarter);

CREATE INDEX IF NOT EXISTS idx_nuclear_safety_station
    ON nuclear_safety (station);

DROP TABLE IF EXISTS data_load_log;

CREATE TABLE data_load_log
(
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    operation     TEXT    NOT NULL,
    records_count INTEGER NOT NULL DEFAULT 0,
    status        TEXT    NOT NULL CHECK (status IN ('success', 'failed', 'partial')),
    error_message TEXT,
    created_at    TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_data_load_log_created_at
    ON data_load_log (created_at);

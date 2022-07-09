DROP DATABASE IF EXISTS verificaciones;
CREATE DATABASE verificaciones;
use verificaciones;

-- ---------- verificados ----------
CREATE TABLE verificados (
    id VARCHAR(255) NOT NULL,
    username VARCHAR(255) NOT NULL,
    uuid VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

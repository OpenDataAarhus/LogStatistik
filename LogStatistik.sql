--
-- File generated with SQLiteStudio v3.0.3 on ti nov 17 12:27:06 2015
--
-- Text encoding used: windows-1252
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: Resources
CREATE TABLE Resources (resource_id VARCHAR, name VARCHAR)

-- Table: Download
CREATE TABLE Download (resource_id TEXT, logDate DATE)

-- Table: APICall
CREATE TABLE APICall (resource_id TEXT, logDate DATE, command TEXT)

COMMIT TRANSACTION;

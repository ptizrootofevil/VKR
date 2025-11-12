CREATE DATABASE IF NOT EXISTS test_database;
CREATE TABLE test_database.test_table (
    id UInt32,
    name String
) ENGINE = MergeTree()
ORDER BY id;
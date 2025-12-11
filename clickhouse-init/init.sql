CREATE DATABASE IF NOT EXISTS default;

create table if not exists default.test_table
(
    id Int64,
    name String
)
ENGINE = MergeTree()
ORDER BY id;
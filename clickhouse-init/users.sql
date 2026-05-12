create table if not exists Uses 
(
    id                UUID DEFAULT generateUUIDv4(),
    first_name        String,
    second_name       String,
    surname           String,
    login             String,
    password          String,
    comment           String,
    creation_datetime DateTime
)
ENGINE = MergeTree()
ORDER BY id;


INSERT INTO Users (first_name, second_name, surname, login, password, comment, creation_date)
SELECT 'Иван', 'Иванов', 'Иванович', 'admin', 'admin', 'пользователь администратор', now()
WHERE NOT EXISTS (
    SELECT 1 FROM users LIMIT 1
);
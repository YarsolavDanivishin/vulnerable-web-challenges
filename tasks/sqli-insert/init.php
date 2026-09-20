<?php

function generateFlag(): string
{
    $configured = getenv('FLAG');

    return $configured !== false && $configured !== ''
        ? $configured
        : hash('sha256', random_bytes(32));
}

$db = new PDO('sqlite:/tmp/challenge.db');
$db->exec(
    'CREATE TABLE IF NOT EXISTS users (username TEXT,email TEXT,password TEXT); '
    . 'CREATE TABLE IF NOT EXISTS secret_flag (flag TEXT); '
    . 'DELETE FROM secret_flag'
);

$query = $db->prepare('INSERT INTO secret_flag VALUES (?)');
$query->execute([generateFlag()]);
$db->exec("INSERT INTO users VALUES ('alice','alice@example.test','password')");

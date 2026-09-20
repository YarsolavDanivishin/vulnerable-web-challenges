const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const app = express();
const db = new sqlite3.Database('/tmp/challenge.db');
const flag = process.env.FLAG || 'vladilk{local-error-based}';
db.serialize(() => { db.run('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, email TEXT)'); db.run('CREATE TABLE IF NOT EXISTS secret_flag (flag TEXT)'); db.run('DELETE FROM secret_flag'); db.run('INSERT INTO secret_flag VALUES (?)', flag); db.run("INSERT INTO users VALUES (1, 'alice', 'alice@example.test')"); });
app.get('/', (req, res) => { const id = req.query.id || '1'; const sql = `SELECT id,name,email FROM users WHERE id=(${id})`; db.all(sql, (err, rows) => { let body = `<h1>Error-based SQLi</h1><p>Try <code>?id=...</code>. Query: <code>${escape(sql)}</code></p>`; if (err) body += `<pre>SQLite error: ${escape(err.message)}</pre>`; else body += `<pre>${escape(JSON.stringify(rows))}</pre>`; res.send(body); }); });
function escape(value) { return String(value).replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c])); }
app.listen(80, () => console.log('error-based listening on 80'));

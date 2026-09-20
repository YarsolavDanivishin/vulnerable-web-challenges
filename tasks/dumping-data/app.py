import os, sqlite3
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
app=FastAPI(); DB='/tmp/challenge.db'
db=sqlite3.connect(DB); db.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER,name TEXT,email TEXT); CREATE TABLE IF NOT EXISTS secret_flag(flag TEXT); DELETE FROM secret_flag; INSERT INTO users VALUES (1,\'alice\',\'a@example.test\');'); db.execute('INSERT INTO secret_flag VALUES (?)',(os.getenv('FLAG','vladilk{local-dumping-data}'),)); db.commit(); db.close()
@app.get('/',response_class=HTMLResponse)
def index(id: str=Query('1'), file: str=Query('')):
    sql=f"SELECT id,name,email FROM users WHERE id='{id}'"; conn=sqlite3.connect(DB)
    try: rows=conn.execute(sql).fetchall(); output=str(rows)
    except sqlite3.Error as exc: output=f'SQLite error: {exc}'
    if file:
        try: output += '\nFILE: '+open(file).read()
        except OSError as exc: output += f'\nFile error: {exc}'
    conn.close(); return f'<h1>Dumping-data SQLi</h1><p>Query: <code>{sql}</code></p><pre>{output}</pre>'

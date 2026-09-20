import os, sqlite3
from flask import Flask, request
app=Flask(__name__); DB='/tmp/challenge.db'
def setup():
    db=sqlite3.connect(DB); db.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER); CREATE TABLE IF NOT EXISTS secret_flag(flag TEXT); DELETE FROM secret_flag; INSERT INTO users VALUES (1);'); db.execute('INSERT INTO secret_flag VALUES (?)',(os.getenv('FLAG','vladilk{local-boolean-blind}'),)); db.commit(); db.close()
setup()
@app.get('/')
def index():
    value=request.args.get('id','1'); sql=f"SELECT id FROM users WHERE id={value}"
    try: exists=bool(sqlite3.connect(DB).execute(sql).fetchone())
    except sqlite3.Error: exists=False
    return f'<h1>Boolean-blind SQLi</h1><p>Only the boolean oracle is shown.</p><p>{"User exists" if exists else "User not found"}</p>'
app.run(host='0.0.0.0',port=80)

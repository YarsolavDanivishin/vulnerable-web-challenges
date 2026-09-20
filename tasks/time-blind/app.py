import os, sqlite3, time
from flask import Flask, request
app=Flask(__name__); DB='/tmp/challenge.db'
def pause(seconds): time.sleep(float(seconds)); return 0
db=sqlite3.connect(DB); db.create_function('SLEEP',1,pause); db.executescript('CREATE TABLE IF NOT EXISTS users(id INTEGER); CREATE TABLE IF NOT EXISTS secret_flag(flag TEXT); DELETE FROM secret_flag; INSERT INTO users VALUES (1);'); db.execute('INSERT INTO secret_flag VALUES (?)',(os.getenv('FLAG','vladilk{local-time-blind}'),)); db.commit(); db.close()
@app.get('/')
def index():
    value=request.args.get('id','1'); sql=f"SELECT id FROM users WHERE id='{value}'"
    start=time.monotonic(); conn=sqlite3.connect(DB); conn.create_function('SLEEP',1,pause)
    try: conn.execute(sql).fetchone()
    except sqlite3.Error: pass
    elapsed=time.monotonic()-start; conn.close()
    return f'<h1>Time-blind SQLi</h1><p>Request processed.</p><p>Elapsed: {elapsed:.2f}s</p>'
app.run(host='0.0.0.0',port=80)
